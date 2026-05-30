"""
Pydantic v2 data contracts for intervention and action MCP tools.

Tools covered:
  - get_intervention_playbook  (HR & Manager Agent)
  - create_checkin_event       (HR & Manager Agent)
  - log_intervention           (HR & Manager Agent)
  - escalate_to_hr             (HR & Manager Agent)
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


# ── get_intervention_playbook ─────────────────────────────────────────────────


class GetInterventionPlaybookRequest(BaseModel):
    """Request payload for the get_intervention_playbook MCP tool."""

    risk_tier: str = Field(
        ...,
        description="Risk classification tier to match playbook actions against: LOW, MODERATE, HIGH, CRITICAL.",
    )
    context_tags: list[str] = Field(
        ...,
        description=(
            "Contextual tags describing the team situation "
            "(e.g. ['overtime', 'cross-team-meetings', 'new-hire-onboarding'])."
        ),
    )


class PlaybookAction(BaseModel):
    """A single recommended intervention action from the Foundry IQ policy store."""

    action_title: str = Field(
        ...,
        description="Short human-readable title for the intervention action.",
    )
    description: str = Field(
        ...,
        description="Detailed explanation of the recommended intervention steps.",
    )
    policy_citation: str = Field(
        ...,
        description=(
            "Formal citation to the authorised corporate policy "
            "(e.g. 'Employee Assistance Policy §4')."
        ),
    )
    source_document: str = Field(
        ...,
        description="Identifier or title of the source document in the Foundry IQ store.",
    )


class GetInterventionPlaybookResponse(BaseModel):
    """Response payload for the get_intervention_playbook MCP tool."""

    risk_tier: str = Field(
        ...,
        description="Echo of the requested risk tier.",
    )
    actions: list[PlaybookAction] = Field(
        ...,
        description="Ordered list of cited intervention actions matching the risk profile.",
    )


# ── create_checkin_event ──────────────────────────────────────────────────────


class CreateCheckinEventRequest(BaseModel):
    """Request payload for the create_checkin_event MCP tool."""

    employee_id: str = Field(
        ...,
        description="Unique employee identifier (e.g. EMP-001) for the welfare check-in.",
    )
    start_time: datetime = Field(
        ...,
        description=(
            "ISO-8601 datetime for the check-in start. "
            "Pydantic v2 natively parses ISO-8601 strings into datetime objects."
        ),
    )
    duration_minutes: int = Field(
        ...,
        description="Duration of the 1:1 welfare check-in in minutes.",
    )



class CreateCheckinEventResponse(BaseModel):
    """Response payload for the create_checkin_event MCP tool."""

    event_id: str = Field(
        ...,
        description="Generated Microsoft Outlook calendar item identifier.",
    )
    status: str = Field(
        ...,
        description="Creation status: 'created' or 'conflict'.",
    )
    location: str | None = Field(
        default=None,
        description="Meeting location or Teams link, if applicable.",
    )


# ── log_intervention ──────────────────────────────────────────────────────────


class LogInterventionRequest(BaseModel):
    """Request payload for the log_intervention MCP tool."""

    employee_id: str = Field(
        ...,
        description="Unique employee identifier for the intervention target.",
    )
    action_taken: str = Field(
        ...,
        description="Description of the managerial action taken (e.g. 'scheduled_checkin', 'workload_rebalance').",
    )
    notes: str | None = Field(
        default=None,
        description="Optional free-text notes providing additional context for the audit trail.",
    )


class LogInterventionResponse(BaseModel):
    """Response payload for the log_intervention MCP tool."""

    intervention_id: str = Field(
        ...,
        description="UUID of the newly created intervention log entry.",
    )
    created_at: datetime = Field(
        ...,
        description="Server-side timestamp when the intervention was recorded.",
    )
    status: str = Field(
        ...,
        description="Transaction status: 'recorded'.",
    )


# ── escalate_to_hr ────────────────────────────────────────────────────────────


class EscalateToHrRequest(BaseModel):
    """Request payload for the escalate_to_hr MCP tool."""

    origin_team_id: str = Field(
        ...,
        description="Identifier of the originating team where systemic pressure was detected.",
    )
    risk_factors: list[str] = Field(
        ...,
        description="List of identified risk factors driving the escalation (e.g. ['chronic_overtime', 'attrition_spike']).",
    )
    incident_summary: str = Field(
        ...,
        description="Anonymized narrative summary of the systemic team pressures requiring HR structural review.",
    )


class EscalateToHrResponse(BaseModel):
    """Response payload for the escalate_to_hr MCP tool."""

    ticket_id: str = Field(
        ...,
        description="Unique identifier for the generated HR escalation ticket.",
    )
    status: str = Field(
        ...,
        description="Escalation status: 'escalated'.",
    )
    created_at: datetime = Field(
        ...,
        description="Server-side timestamp when the escalation ticket was created.",
    )
