"""
FastAPI route handlers for HR & Manager Agent READ tools.

Tools:
  POST /tools/get_team_signals         — Team-wide anonymised burnout signals
  POST /tools/get_member_trend         — 4-week individual burnout trend
  POST /tools/recommend_task_assignment — Skill + capacity ranked candidates
"""

from __future__ import annotations

import string
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Employee, PreComputedScore, RoleBaseline
from mcp_server.auth import CurrentUser, get_current_user
from mcp_server.schemas.signals import (
    GetTeamSignalsRequest,
    GetTeamSignalsResponse,
    MemberSignalSummary,
    TeamSummaryMetrics,
    GetMemberTrendRequest,
    GetMemberTrendResponse,
    WeeklyTrendPoint,
)
from mcp_server.schemas.scores import (
    RecommendTaskAssignmentRequest,
    RecommendTaskAssignmentResponse,
    CandidateMatch,
)

router = APIRouter(prefix="/tools", tags=["HR Read Tools"])

# ---------------------------------------------------------------------------
# Stub skill map — placeholder until a dedicated skills table is added.
# Maps role_type → default skill tags for Jaccard similarity matching.
# ---------------------------------------------------------------------------
ROLE_SKILL_MAP: dict[str, list[str]] = {
    "ENGINEERING_MANAGER": [
        "project-management", "system-design", "python", "leadership",
    ],
    "SENIOR_ENGINEER": [
        "python", "data-engineering", "system-design", "code-review",
    ],
    "JUNIOR_ENGINEER": [
        "python", "testing", "documentation",
    ],
    "SALES_EXECUTIVE": [
        "client-relations", "crm", "presentation", "negotiation",
    ],
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _derive_primary_signals(
    signal_summary: dict | None,
    baseline: RoleBaseline | None,
) -> list[str]:
    """Compare signal_summary JSON against RoleBaseline to produce signal tags.

    Uses ``.get()`` with safe defaults to avoid KeyErrors on sparse data.
    """
    if not signal_summary:
        return []

    signals: list[str] = []
    meeting_hrs = signal_summary.get("meeting_hrs", 0)
    focus_hrs = signal_summary.get("focus_hrs", 0)
    after_hours_days = signal_summary.get("after_hours_days", 0)

    if baseline:
        if meeting_hrs > baseline.expected_meeting_hrs:
            signals.append("meeting_overload")
        if focus_hrs < baseline.focus_time_min_hrs:
            signals.append("focus_deficit")

    if after_hours_days > 2:
        signals.append("after_hours_work")

    return signals


def _jaccard_similarity(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity coefficient: |A ∩ B| / |A ∪ B|."""
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


# ---------------------------------------------------------------------------
# POST /tools/get_team_signals
# ---------------------------------------------------------------------------


@router.post(
    "/get_team_signals",
    response_model=GetTeamSignalsResponse,
    summary="Retrieve team-wide aggregated burnout signals",
    description=(
        "Returns anonymised, privacy-safe burnout indicators for all "
        "direct reports of the requesting manager."
    ),
)
def get_team_signals(
    request: GetTeamSignalsRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetTeamSignalsResponse:
    manager_id = current_user.user_id

    # 1. Fetch direct reports (deterministic sort for stable anonymisation)
    query = db.query(Employee).filter(
        Employee.manager_id == manager_id,
        or_(Employee.is_active.is_(True), Employee.is_active.is_(None)),
    )
    if request.department_id:
        query = query.filter(Employee.department == request.department_id)

    team_members = query.order_by(Employee.member_id).all()

    if not team_members:
        raise HTTPException(
            status_code=404,
            detail=f"No active team members found for manager '{manager_id}'.",
        )

    # 2. Build anonymised member signal summaries
    members: list[MemberSignalSummary] = []
    tier_counts = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "CRITICAL": 0}
    latest_computed_at = None

    for idx, emp in enumerate(team_members):
        # Latest pre-computed score
        score_row = (
            db.query(PreComputedScore)
            .filter(PreComputedScore.member_id == emp.member_id)
            .order_by(PreComputedScore.computed_at.desc())
            .first()
        )

        if score_row is None:
            continue  # skip members without computed scores

        # Role baseline for signal tag derivation
        baseline = (
            db.query(RoleBaseline)
            .filter(
                RoleBaseline.role_type == emp.role_type,
                RoleBaseline.department == emp.department,
            )
            .first()
        )

        # Track the most recent computation timestamp
        if latest_computed_at is None or score_row.computed_at > latest_computed_at:
            latest_computed_at = score_row.computed_at

        # Count risk tiers for the summary
        tier = score_row.risk_tier.upper()
        if tier in tier_counts:
            tier_counts[tier] += 1

        # Derive primary signal tags from baseline comparison
        primary_signals = _derive_primary_signals(
            score_row.signal_summary, baseline,
        )

        # Anonymise: MEMBER-A, MEMBER-B, ... (stable across calls)
        label = string.ascii_uppercase[idx % 26]
        if idx >= 26:
            label = f"{string.ascii_uppercase[idx // 26 - 1]}{label}"

        members.append(
            MemberSignalSummary(
                member_ref=f"MEMBER-{label}",
                risk_tier=tier,
                score=score_row.score,
                trend=score_row.trend_direction or "stable",
                trend_delta=score_row.trend_delta or 0,
                primary_signals=primary_signals,
            )
        )

    if not members:
        raise HTTPException(
            status_code=404,
            detail="No computed scores available for this team.",
        )

    return GetTeamSignalsResponse(
        last_updated=latest_computed_at,
        team_summary=TeamSummaryMetrics(
            low_risk=tier_counts["LOW"],
            moderate_risk=tier_counts["MODERATE"],
            high_risk=tier_counts["HIGH"],
            critical_risk=tier_counts["CRITICAL"],
        ),
        members=members,
    )


# ---------------------------------------------------------------------------
# POST /tools/get_member_trend
# ---------------------------------------------------------------------------


@router.post(
    "/get_member_trend",
    response_model=GetMemberTrendResponse,
    summary="Retrieve 4-week burnout trend for a team member",
    description=(
        "Returns a chronological vector of weekly risk data points "
        "for the specified employee."
    ),
)
def get_member_trend(
    request: GetMemberTrendRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetMemberTrendResponse:
    # Fetch up to 4 most recent score rows
    score_rows = (
        db.query(PreComputedScore)
        .filter(PreComputedScore.member_id == request.employee_id)
        .order_by(PreComputedScore.computed_at.desc())
        .limit(4)
        .all()
    )

    if not score_rows:
        raise HTTPException(
            status_code=404,
            detail=f"No computed scores found for employee '{request.employee_id}'.",
        )

    # Look up role baseline for focus deficit calculation
    employee = (
        db.query(Employee)
        .filter(Employee.member_id == request.employee_id)
        .first()
    )

    baseline = None
    if employee:
        baseline = (
            db.query(RoleBaseline)
            .filter(
                RoleBaseline.role_type == employee.role_type,
                RoleBaseline.department == employee.department,
            )
            .first()
        )

    baseline_focus_hrs = baseline.focus_time_min_hrs if baseline else 0

    # Build weekly trend points (reverse to chronological order)
    trend: list[WeeklyTrendPoint] = []
    for score in reversed(score_rows):
        # Calculate Monday of the score's week
        computed_date = score.computed_at.date()
        week_start = computed_date - timedelta(days=computed_date.weekday())

        # Focus deficit: baseline expectation minus actual hours
        summary = score.signal_summary or {}
        actual_focus = summary.get("focus_hrs", 0)
        focus_deficit = max(0.0, float(baseline_focus_hrs) - float(actual_focus))

        trend.append(
            WeeklyTrendPoint(
                week_starting=week_start,
                cognitive_load_index=score.score,
                focus_time_deficit_hours=round(focus_deficit, 1),
                burnout_risk_tier=score.risk_tier,
            )
        )

    return GetMemberTrendResponse(
        employee_id=request.employee_id,
        trend=trend,
    )


# ---------------------------------------------------------------------------
# POST /tools/recommend_task_assignment
# ---------------------------------------------------------------------------


@router.post(
    "/recommend_task_assignment",
    response_model=RecommendTaskAssignmentResponse,
    summary="Recommend team members for task assignment",
    description=(
        "Cross-analyses employee skills and cognitive load to produce "
        "a prioritised candidate list for task assignment."
    ),
)
def recommend_task_assignment(
    request: RecommendTaskAssignmentRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendTaskAssignmentResponse:
    required = set(s.lower().strip() for s in request.required_skills)

    # Fetch all active non-manager employees (manager_id IS NOT NULL)
    employees = (
        db.query(Employee)
        .filter(
            Employee.manager_id.isnot(None),
            or_(Employee.is_active.is_(True), Employee.is_active.is_(None)),
        )
        .all()
    )

    candidates: list[CandidateMatch] = []

    for emp in employees:
        # Latest pre-computed score
        score_row = (
            db.query(PreComputedScore)
            .filter(PreComputedScore.member_id == emp.member_id)
            .order_by(PreComputedScore.computed_at.desc())
            .first()
        )

        current_score = score_row.score if score_row else 0
        risk_tier = score_row.risk_tier if score_row else "UNKNOWN"

        # Skill compatibility via Jaccard similarity (stub from ROLE_SKILL_MAP)
        emp_skills = set(
            s.lower() for s in ROLE_SKILL_MAP.get(emp.role_type, [])
        )
        compatibility = _jaccard_similarity(required, emp_skills)

        # Available capacity: normalised against a 40-hour work week
        # Score 0 → 40 hrs free, Score 100 → 0 hrs free
        available_capacity = max(0.0, (100 - current_score) / 100.0 * 40.0)

        candidates.append(
            CandidateMatch(
                employee_id=emp.member_id,
                display_name=emp.display_name,
                skill_compatibility_index=round(compatibility, 2),
                current_cognitive_load=current_score,
                risk_tier=risk_tier,
                available_capacity_hours=round(available_capacity, 1),
            )
        )

    # Sort: highest skill match first, then lowest cognitive load
    candidates.sort(
        key=lambda c: (-c.skill_compatibility_index, c.current_cognitive_load),
    )

    return RecommendTaskAssignmentResponse(candidates=candidates)
