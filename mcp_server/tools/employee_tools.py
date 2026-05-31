"""
FastAPI route handlers for the Employee Agent tools.

Tools:
  POST /tools/get_my_signals        — Personal workload signal dashboard
  POST /tools/get_policy_info       — Foundry IQ policy retrieval stub
  POST /tools/draft_workload_email  — Workload email draft generator stub

Security:
  All endpoints require ``X-Mock-User-Id`` authentication.
  ``get_my_signals`` enforces strict identity matching —
  current_user.user_id MUST equal request.employee_id (403 on mismatch).
"""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Employee, EmployeePreference, PreComputedScore, RoleBaseline
from mcp_server.auth import CurrentUser, get_current_user
from mcp_server.schemas.signals import (
    GetMySignalsRequest,
    GetMySignalsResponse,
    PersonalSignalItem,
)
from mcp_server.schemas.employee import (
    GetPolicyInfoRequest,
    GetPolicyInfoResponse,
    PolicyBlock,
    DraftWorkloadEmailRequest,
    DraftWorkloadEmailResponse,
)

router = APIRouter(prefix="/tools", tags=["Employee Tools"])


# ---------------------------------------------------------------------------
# Hardcoded policy blocks — placeholder until Foundry IQ is integrated.
# ---------------------------------------------------------------------------
POLICY_BLOCKS: list[PolicyBlock] = [
    PolicyBlock(
        title="Employee Assistance Programme (EAP)",
        content=(
            "All employees are entitled to up to 6 confidential counselling "
            "sessions per calendar year through the company's EAP provider. "
            "Sessions can be booked directly without manager approval. "
            "Topics include stress management, work-life balance, financial "
            "wellbeing, and family support."
        ),
        section_reference="\u00a74.1",
        source_id="HR-POL-EAP-2025",
    ),
    PolicyBlock(
        title="Flexible Working Arrangements",
        content=(
            "Employees may request flexible start/end times, compressed "
            "work weeks, or temporary remote-work arrangements. Requests "
            "should be submitted via the HR portal and will be reviewed "
            "within 5 business days. Approval is based on role requirements "
            "and team coverage needs."
        ),
        section_reference="\u00a72.3",
        source_id="HR-POL-FLEX-2025",
    ),
    PolicyBlock(
        title="Mental Health Days",
        content=(
            "Employees may take up to 3 dedicated mental health days per "
            "quarter without requiring a medical certificate. These are "
            "separate from standard sick leave and do not require manager "
            "justification beyond a self-service booking in the HR system."
        ),
        section_reference="\u00a75.2",
        source_id="HR-POL-WELLBEING-2025",
    ),
    PolicyBlock(
        title="Workload Escalation Process",
        content=(
            "If workload concerns persist beyond 2 consecutive weeks, "
            "employees are encouraged to escalate through their direct "
            "manager or the HR Business Partner. The escalation triggers "
            "a formal workload review within 10 business days."
        ),
        section_reference="\u00a73.7",
        source_id="HR-POL-ESCALATION-2025",
    ),
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _derive_optimization_tips(
    signal_summary: dict,
    baseline: RoleBaseline | None,
) -> list[str]:
    """Generate personalised workload optimisation tips from signal data."""
    tips: list[str] = []
    meeting_hrs = signal_summary.get("meeting_hrs", 0)
    focus_hrs = signal_summary.get("focus_hrs", 0)
    after_hours = signal_summary.get("after_hours_days", 0)

    if baseline:
        if meeting_hrs > baseline.expected_meeting_hrs:
            excess = meeting_hrs - baseline.expected_meeting_hrs
            tips.append(
                f"Your meeting hours exceed the role baseline by {excess}h. "
                "Consider declining or delegating low-priority recurring meetings."
            )
        if focus_hrs < baseline.focus_time_min_hrs:
            deficit = baseline.focus_time_min_hrs - focus_hrs
            tips.append(
                f"You're {deficit}h below the recommended focus time. "
                "Try blocking 2-hour focus slots on your calendar each morning."
            )

    if after_hours > 2:
        tips.append(
            f"You worked after hours on {after_hours} days this week. "
            "Consider setting firm end-of-day boundaries and using "
            "delayed message sending."
        )

    if not tips:
        tips.append(
            "Your workload signals are within healthy ranges. Keep it up!"
        )

    return tips


# ---------------------------------------------------------------------------
# POST /tools/get_my_signals   (DB Read — Identity-Enforced)
# ---------------------------------------------------------------------------


@router.post(
    "/get_my_signals",
    response_model=GetMySignalsResponse,
    summary="Retrieve personal workload signal dashboard",
    description=(
        "Returns the employee's own workload metrics and baseline comparison. "
        "Enforces strict identity matching — the authenticated user can only "
        "view their own signals."
    ),
)
def get_my_signals(
    request: GetMySignalsRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GetMySignalsResponse:
    # CRITICAL: Consent-first identity enforcement
    if current_user.user_id != request.employee_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: You can only access your own signals.",
        )

    # Opt-in consent verification
    preference = (
        db.query(EmployeePreference)
        .filter(EmployeePreference.member_id == request.employee_id)
        .first()
    )
    if preference is None or not preference.opted_in:
        raise HTTPException(
            status_code=403,
            detail="Signal access requires opt-in consent.",
        )

    # Query latest pre-computed score
    score_row = (
        db.query(PreComputedScore)
        .filter(PreComputedScore.member_id == request.employee_id)
        .order_by(PreComputedScore.computed_at.desc())
        .first()
    )

    if score_row is None:
        raise HTTPException(
            status_code=404,
            detail="No signals found for this employee.",
        )

    # Look up employee record and role baseline
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

    # Build current PersonalSignalItem from signal_summary JSON
    summary = score_row.signal_summary or {}
    computed_date = score_row.computed_at.date()
    week_start = computed_date - timedelta(days=computed_date.weekday())

    tips = _derive_optimization_tips(summary, baseline)

    current = PersonalSignalItem(
        week_starting=week_start,
        meeting_hours=float(summary.get("meeting_hrs", 0)),
        message_count=int(summary.get("message_count", 0)),
        focus_hours=float(summary.get("focus_hrs", 0)),
        optimization_tips=tips,
    )

    # Build baseline PersonalSignalItem from RoleBaseline (if exists)
    baseline_item = None
    if baseline:
        baseline_item = PersonalSignalItem(
            week_starting=week_start,
            meeting_hours=float(baseline.expected_meeting_hrs),
            message_count=0,  # No baseline for message count
            focus_hours=float(baseline.focus_time_min_hrs),
            optimization_tips=[],
        )

    return GetMySignalsResponse(
        employee_id=request.employee_id,
        current=current,
        baseline=baseline_item,
    )


# ---------------------------------------------------------------------------
# POST /tools/get_policy_info   (API Stub)
# ---------------------------------------------------------------------------


@router.post(
    "/get_policy_info",
    response_model=GetPolicyInfoResponse,
    summary="Retrieve corporate policy information",
    description=(
        "Stub endpoint — returns hardcoded policy blocks from the "
        "HR Policy Library. In production, this will query the "
        "Foundry IQ document store with semantic matching."
    ),
)
def get_policy_info(
    request: GetPolicyInfoRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> GetPolicyInfoResponse:
    # TODO: Replace with real Foundry IQ semantic search using
    #       request.query_string for document retrieval.
    #
    # Stub: return all policy blocks regardless of query.
    # A real implementation would filter by semantic relevance.
    return GetPolicyInfoResponse(results=POLICY_BLOCKS)


# ---------------------------------------------------------------------------
# POST /tools/draft_workload_email   (API Stub)
# ---------------------------------------------------------------------------


@router.post(
    "/draft_workload_email",
    response_model=DraftWorkloadEmailResponse,
    summary="Generate a workload adjustment email draft",
    description=(
        "Generates a structured email draft for the employee to review "
        "and manually send to their manager. Direct system-automated "
        "mailing is strictly forbidden."
    ),
)
def draft_workload_email(
    request: DraftWorkloadEmailRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> DraftWorkloadEmailResponse:
    focus_list = "\n".join(f"- {area.replace('_', ' ').title()}" for area in request.focus_areas)

    body = (
        f"Hi,\n\n"
        f"I'd like to schedule a brief conversation to discuss some workload "
        f"adjustments based on my recent work patterns. The following areas "
        f"have been identified through my personal LumenHR dashboard:\n\n"
        f"{focus_list}\n\n"
        f"I believe a short discussion could help us find adjustments that "
        f"improve both my productivity and wellbeing. I'm happy to work "
        f"around your schedule.\n\n"
        f"Best regards,\n"
        f"{current_user.user_id}"
    )

    return DraftWorkloadEmailResponse(
        subject="Request: Workload Adjustment Discussion",
        body_markdown=body,
        disclaimer=(
            "IMPORTANT: This is a draft only. It has NOT been sent. "
            "You must review the content, make any desired changes, "
            "and send it manually. Direct system-automated mailing "
            "actions are strictly forbidden by company policy."
        ),
    )
