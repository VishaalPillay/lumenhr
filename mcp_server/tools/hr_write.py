"""
FastAPI route handlers for HR & Manager Agent WRITE / ACTION tools.

Tools:
  POST /tools/log_intervention           — Audit trail DB write
  POST /tools/escalate_to_hr             — HR escalation DB write
  POST /tools/create_checkin_event       — Outlook calendar stub
  POST /tools/get_intervention_playbook  — Foundry IQ policy stub
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import InterventionLog
from mcp_server.auth import CurrentUser, get_current_user
from mcp_server.schemas.interventions import (
    LogInterventionRequest,
    LogInterventionResponse,
    EscalateToHrRequest,
    EscalateToHrResponse,
    CreateCheckinEventRequest,
    CreateCheckinEventResponse,
    GetInterventionPlaybookRequest,
    GetInterventionPlaybookResponse,
    PlaybookAction,
)

router = APIRouter(prefix="/tools", tags=["HR Write Tools"])


# ---------------------------------------------------------------------------
# Hardcoded playbook actions — placeholder until Foundry IQ is integrated.
# Keyed by risk tier; each tier returns a curated list of PlaybookAction
# objects citing the corporate Manager Handbook.
# ---------------------------------------------------------------------------
PLAYBOOK_ACTIONS: dict[str, list[PlaybookAction]] = {
    "LOW": [
        PlaybookAction(
            action_title="Continue Monitoring",
            description=(
                "No immediate action required. Continue observing team "
                "signals through the weekly LumenHR dashboard and flag "
                "any sustained upward trend."
            ),
            policy_citation="Manager Handbook \u00a72.1 \u2014 Preventive Monitoring",
            source_document="Manager Handbook v3.2",
        ),
    ],
    "MODERATE": [
        PlaybookAction(
            action_title="Schedule 1:1 Welfare Check-in",
            description=(
                "Book a 30-minute non-evaluative welfare check-in with "
                "the affected team member within 48 hours. Focus on "
                "workload distribution and blockers, not performance."
            ),
            policy_citation="Manager Handbook \u00a73.4 \u2014 Proactive Welfare Conversations",
            source_document="Manager Handbook v3.2",
        ),
        PlaybookAction(
            action_title="Review Meeting Load",
            description=(
                "Audit the team member's recurring meeting commitments "
                "and cancel or delegate at least two low-priority "
                "recurring meetings to restore focus time."
            ),
            policy_citation="Manager Handbook \u00a73.6 \u2014 Meeting Hygiene",
            source_document="Manager Handbook v3.2",
        ),
    ],
    "HIGH": [
        PlaybookAction(
            action_title="Immediate Workload Rebalance",
            description=(
                "Redistribute at least 20% of the team member's active "
                "tasks to peers with available capacity. Document the "
                "rebalance in the team's project tracker."
            ),
            policy_citation="Manager Handbook \u00a74.2 \u2014 Workload Redistribution Protocol",
            source_document="Manager Handbook v3.2",
        ),
        PlaybookAction(
            action_title="Engage Employee Assistance Programme",
            description=(
                "Share EAP contact details with the team member and "
                "confirm awareness of available support channels. "
                "Do not probe personal circumstances."
            ),
            policy_citation="Employee Assistance Policy \u00a74",
            source_document="HR Policy Library \u2014 EAP Guidelines",
        ),
    ],
    "CRITICAL": [
        PlaybookAction(
            action_title="Escalate to HR Business Partner",
            description=(
                "File a formal escalation with the HR Business Partner "
                "within 24 hours. Include anonymised signal data and "
                "the team's 4-week trend summary."
            ),
            policy_citation="Manager Handbook \u00a75.1 \u2014 Critical Escalation Path",
            source_document="Manager Handbook v3.2",
        ),
        PlaybookAction(
            action_title="Temporary Protective Measures",
            description=(
                "Implement temporary measures: no new project assignments, "
                "meeting-free afternoons, and flexible start times for "
                "the affected team member until the HR review is complete."
            ),
            policy_citation="Manager Handbook \u00a75.3 \u2014 Interim Protective Actions",
            source_document="Manager Handbook v3.2",
        ),
    ],
}


# ---------------------------------------------------------------------------
# POST /tools/log_intervention   (DB Write)
# ---------------------------------------------------------------------------


@router.post(
    "/log_intervention",
    response_model=LogInterventionResponse,
    summary="Log a managerial intervention to the audit trail",
    description=(
        "Appends an immutable record to the intervention_log table "
        "capturing the manager's action for compliance and tracking."
    ),
)
def log_intervention(
    request: LogInterventionRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LogInterventionResponse:
    entry = InterventionLog(
        manager_id=current_user.user_id,
        action_type=request.action_taken,
        context_summary=f"Target: {request.employee_id} | Notes: {request.notes or 'N/A'}",
    )
    try:
        db.add(entry)
        db.commit()
        db.refresh(entry)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log intervention: {exc}",
        ) from exc

    return LogInterventionResponse(
        intervention_id=str(entry.id),
        created_at=entry.created_at,
        status="recorded",
    )


# ---------------------------------------------------------------------------
# POST /tools/escalate_to_hr   (DB Write)
# ---------------------------------------------------------------------------


@router.post(
    "/escalate_to_hr",
    response_model=EscalateToHrResponse,
    summary="Escalate systemic team pressure to HR",
    description=(
        "Generates an anonymised escalation record in the audit trail "
        "when structural team pressures require HR-level review."
    ),
)
def escalate_to_hr(
    request: EscalateToHrRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> EscalateToHrResponse:
    context_summary = (
        f"Team: {request.origin_team_id}\n"
        f"Risk Factors: {', '.join(request.risk_factors)}\n"
        f"Summary: {request.incident_summary}"
    )
    entry = InterventionLog(
        manager_id=current_user.user_id,
        action_type="ESCALATION",
        risk_tier="CRITICAL",
        context_summary=context_summary,
    )
    try:
        db.add(entry)
        db.commit()
        db.refresh(entry)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create escalation: {exc}",
        ) from exc

    return EscalateToHrResponse(
        ticket_id=f"ESC-{str(entry.id)[:8].upper()}",
        status="escalated",
        created_at=entry.created_at,
    )


# ---------------------------------------------------------------------------
# POST /tools/create_checkin_event   (API Stub)
# ---------------------------------------------------------------------------


@router.post(
    "/create_checkin_event",
    response_model=CreateCheckinEventResponse,
    summary="Schedule a 1:1 welfare check-in event",
    description=(
        "Stub endpoint — returns a hardcoded success response. "
        "In production, this will invoke the Microsoft Graph API "
        "to create an Outlook calendar event."
    ),
)
def create_checkin_event(
    request: CreateCheckinEventRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> CreateCheckinEventResponse:
    # TODO: Replace with real Microsoft Graph API call via ``msgraph-sdk``.
    #       POST /users/{manager_id}/events with the calendar payload.
    fake_event_id = str(uuid.uuid4())
    return CreateCheckinEventResponse(
        event_id=fake_event_id,
        status="created",
        location=f"https://teams.microsoft.com/l/meetup/{fake_event_id}",
    )


# ---------------------------------------------------------------------------
# POST /tools/get_intervention_playbook   (API Stub)
# ---------------------------------------------------------------------------


@router.post(
    "/get_intervention_playbook",
    response_model=GetInterventionPlaybookResponse,
    summary="Retrieve cited intervention playbook actions",
    description=(
        "Stub endpoint — returns hardcoded playbook actions from the "
        "Manager Handbook keyed by risk tier. In production, this will "
        "query the Foundry IQ policy document store."
    ),
)
def get_intervention_playbook(
    request: GetInterventionPlaybookRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> GetInterventionPlaybookResponse:
    # TODO: Replace with real Foundry IQ retrieval using
    #       request.context_tags for semantic matching.
    tier = request.risk_tier.upper()
    actions = PLAYBOOK_ACTIONS.get(tier, PLAYBOOK_ACTIONS["LOW"])

    return GetInterventionPlaybookResponse(
        risk_tier=tier,
        actions=actions,
    )
