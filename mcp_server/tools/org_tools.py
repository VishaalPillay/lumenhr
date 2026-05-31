"""
FastAPI route handler for the Org-level risk mapping tool.

Tools:
  POST /tools/get_org_risk_map  — Department-level burnout friction map

Security:
  Requires ``X-Mock-User-Id`` authentication.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Employee, PreComputedScore, RoleBaseline
from mcp_server.auth import CurrentUser, get_current_user
from mcp_server.schemas.signals import (
    GetOrgRiskMapRequest,
    GetOrgRiskMapResponse,
    DepartmentRiskSummary,
)

router = APIRouter(prefix="/tools", tags=["Org Tools"])


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _dominant_risk_tier(tiers: list[str]) -> str:
    """Return the most frequent risk tier (mode). Ties break to higher risk."""
    if not tiers:
        return "LOW"

    tier_priority = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    counter = Counter(tiers)
    max_count = max(counter.values())
    # Among tiers sharing the max count, pick the highest-risk (lowest priority number)
    candidates = [t for t, c in counter.items() if c == max_count]
    candidates.sort(key=lambda t: tier_priority.get(t, 99))
    return candidates[0]


def _dominant_friction(
    avg_meeting_hrs: float,
    avg_focus_hrs: float,
    avg_baseline_meeting_hrs: float,
    avg_baseline_focus_hrs: float,
) -> str:
    """Derive the primary operational friction source for a department."""
    if avg_baseline_meeting_hrs > 0 and avg_meeting_hrs > avg_baseline_meeting_hrs:
        return "cross-team meeting overhead"
    if avg_baseline_focus_hrs > 0 and avg_focus_hrs < avg_baseline_focus_hrs:
        return "focus time erosion"
    return "workload distribution"


# ---------------------------------------------------------------------------
# POST /tools/get_org_risk_map   (DB Read — Single-Query Optimized)
# ---------------------------------------------------------------------------


@router.post(
    "/get_org_risk_map",
    response_model=GetOrgRiskMapResponse,
    summary="Retrieve department-level organisational risk map",
    description=(
        "Returns a friction-zone map across all departments within the "
        "specified org unit. Uses an optimized single-query join to avoid "
        "N+1 database access patterns."
    ),
)
def get_org_risk_map(
    request: GetOrgRiskMapRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetOrgRiskMapResponse:
    # ── Step 1: Subquery — latest PreComputedScore per employee ────────────
    latest_score_sq = (
        db.query(
            PreComputedScore.member_id,
            func.max(PreComputedScore.computed_at).label("max_computed"),
        )
        .group_by(PreComputedScore.member_id)
        .subquery()
    )

    # ── Step 2: Single joined query ───────────────────────────────────────
    #   Employee ⟕ (latest score subquery + PreComputedScore) ⟕ RoleBaseline
    rows = (
        db.query(Employee, PreComputedScore, RoleBaseline)
        .outerjoin(
            latest_score_sq,
            Employee.member_id == latest_score_sq.c.member_id,
        )
        .outerjoin(
            PreComputedScore,
            and_(
                PreComputedScore.member_id == latest_score_sq.c.member_id,
                PreComputedScore.computed_at == latest_score_sq.c.max_computed,
            ),
        )
        .outerjoin(
            RoleBaseline,
            and_(
                RoleBaseline.role_type == Employee.role_type,
                RoleBaseline.department == Employee.department,
            ),
        )
        .filter(or_(Employee.is_active.is_(True), Employee.is_active.is_(None)))
        .all()
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No active employees found in the organisation.",
        )

    # ── Step 3: Group by department in Python ─────────────────────────────
    dept_groups: dict[str, list[tuple]] = defaultdict(list)
    for emp, score, baseline in rows:
        dept_groups[emp.department].append((emp, score, baseline))

    # ── Step 4: Aggregate per department ──────────────────────────────────
    departments: list[DepartmentRiskSummary] = []

    for dept_name, members in sorted(dept_groups.items()):
        headcount = len(members)
        tiers: list[str] = []

        total_meeting_hrs = 0.0
        total_focus_hrs = 0.0
        total_baseline_meeting_hrs = 0.0
        total_baseline_focus_hrs = 0.0
        members_with_signals = 0

        for _emp, score, baseline in members:
            if score is not None:
                tiers.append(score.risk_tier.upper())
                summary = score.signal_summary or {}
                total_meeting_hrs += float(summary.get("meeting_hrs", 0))
                total_focus_hrs += float(summary.get("focus_hrs", 0))
                members_with_signals += 1

            if baseline is not None:
                total_baseline_meeting_hrs += float(baseline.expected_meeting_hrs)
                total_baseline_focus_hrs += float(baseline.focus_time_min_hrs)

        # Averages (safe against division by zero)
        n = max(members_with_signals, 1)
        avg_meeting = total_meeting_hrs / n
        avg_focus = total_focus_hrs / n
        avg_bl_meeting = total_baseline_meeting_hrs / max(headcount, 1)
        avg_bl_focus = total_baseline_focus_hrs / max(headcount, 1)

        departments.append(
            DepartmentRiskSummary(
                department=dept_name,
                aggregate_risk_tier=_dominant_risk_tier(tiers),
                dominant_friction=_dominant_friction(
                    avg_meeting, avg_focus, avg_bl_meeting, avg_bl_focus,
                ),
                headcount=headcount,
            )
        )

    return GetOrgRiskMapResponse(
        org_unit_id=request.org_unit_id,
        departments=departments,
    )
