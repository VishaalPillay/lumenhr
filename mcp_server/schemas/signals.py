"""
Pydantic v2 data contracts for signal-related MCP tools.

Tools covered:
  - get_team_signals   (HR & Manager Agent)
  - get_member_trend   (HR & Manager Agent)
  - get_org_risk_map   (HR & Manager Agent)
  - get_my_signals     (Employee Agent)
"""

from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, Field


# ── get_team_signals ──────────────────────────────────────────────────────────


class GetTeamSignalsRequest(BaseModel):
    """Request payload for the get_team_signals MCP tool."""

    time_window: str = Field(
        default="7d",
        description="Lookback window for signals.",
    )
    department_id: str | None = Field(
        default=None,
        description="Optional department filter",
    )



class TeamSummaryMetrics(BaseModel):
    """Aggregate risk-tier counts across a manager's team."""

    low_risk: int = Field(
        ...,
        description="Count of team members at low risk.",
    )
    moderate_risk: int = Field(
        ...,
        description="Count of team members at moderate risk.",
    )
    high_risk: int = Field(
        ...,
        description="Count of team members at high risk.",
    )
    critical_risk: int = Field(
        ...,
        description="Count of team members at critical risk.",
    )


class MemberSignalSummary(BaseModel):
    """Anonymized signal snapshot for a single team member."""

    member_ref: str = Field(
        ...,
        description="Anonymized member reference, e.g., 'MEMBER-A'.",
    )
    risk_tier: str = Field(
        ...,
        description="Risk classification: LOW, MODERATE, HIGH, CRITICAL.",
    )
    score: int = Field(
        ...,
        description="Computed composite risk score from 0-100.",
    )
    trend: str = Field(
        ...,
        description="Trend direction: improving, stable, worsening.",
    )
    trend_delta: int = Field(
        ...,
        description="Change in score vs prior period.",
    )
    primary_signals: list[str] = Field(
        ...,
        description="Key drivers of the score, e.g., ['meeting_overload'].",
    )


class GetTeamSignalsResponse(BaseModel):
    """Response payload for the get_team_signals MCP tool."""

    last_updated: datetime = Field(
        ...,
        description="Timestamp of the last nightly calculation.",
    )
    team_summary: TeamSummaryMetrics = Field(
        ...,
        description="Aggregate counts of risk tiers across the team.",
    )
    members: list[MemberSignalSummary] = Field(
        ...,
        description="Anonymized array of individual team member scores.",
    )


# ── get_member_trend ──────────────────────────────────────────────────────────


class GetMemberTrendRequest(BaseModel):
    """Request payload for the get_member_trend MCP tool."""

    employee_id: str = Field(
        ...,
        description=(
            "Unique employee identifier (e.g. EMP-001) whose 4-week "
            "burnout trend is being requested."
        ),
    )


class WeeklyTrendPoint(BaseModel):
    """A single weekly data point in a member's burnout trend vector."""

    week_starting: date = Field(
        ...,
        description="ISO-8601 date marking the start of the measurement week.",
    )
    cognitive_load_index: int = Field(
        ...,
        description=(
            "Composite cognitive load score for the week (0-100), "
            "derived from PreComputedScore.score."
        ),
    )
    focus_time_deficit_hours: float = Field(
        ...,
        description=(
            "Hours of focus time lost relative to the employee's "
            "RoleBaseline.focus_time_min_hrs expectation."
        ),
    )
    burnout_risk_tier: str = Field(
        ...,
        description="Calculated risk classification for the week: LOW, MODERATE, HIGH, CRITICAL.",
    )


class GetMemberTrendResponse(BaseModel):
    """Response payload for the get_member_trend MCP tool."""

    employee_id: str = Field(
        ...,
        description="Echo of the requested employee identifier.",
    )
    trend: list[WeeklyTrendPoint] = Field(
        ...,
        description="Chronologically ordered list of weekly trend data points (up to 4 weeks).",
    )


# ── get_org_risk_map ──────────────────────────────────────────────────────────


class GetOrgRiskMapRequest(BaseModel):
    """Request payload for the get_org_risk_map MCP tool."""

    org_unit_id: str = Field(
        ...,
        description=(
            "Identifier of the organisational unit to analyse via "
            "Fabric IQ for macro friction zones."
        ),
    )


class DepartmentRiskSummary(BaseModel):
    """Risk summary for a single department within the org unit."""

    department: str = Field(
        ...,
        description="Department name as stored in the Employee table.",
    )
    aggregate_risk_tier: str = Field(
        ...,
        description="Dominant risk tier across the department: LOW, MODERATE, HIGH, CRITICAL.",
    )
    dominant_friction: str = Field(
        ...,
        description=(
            "Primary operational friction source identified by Fabric IQ "
            "(e.g. 'cross-department meeting overhead')."
        ),
    )
    headcount: int = Field(
        ...,
        description="Total active employees in the department.",
    )


class GetOrgRiskMapResponse(BaseModel):
    """Response payload for the get_org_risk_map MCP tool."""

    org_unit_id: str = Field(
        ...,
        description="Echo of the requested organisational unit identifier.",
    )
    departments: list[DepartmentRiskSummary] = Field(
        ...,
        description="Risk summaries for each department within the org unit.",
    )


# ── get_my_signals (Employee Agent) ──────────────────────────────────────────


class GetMySignalsRequest(BaseModel):
    """Request payload for the get_my_signals MCP tool."""

    employee_id: str = Field(
        ...,
        description=(
            "Employee identifier that MUST strict-match the subject "
            "identity resolved via JWT validation context."
        ),
    )


class PersonalSignalItem(BaseModel):
    """Personal workload metrics for a single measurement period."""

    week_starting: date = Field(
        ...,
        description="ISO-8601 date marking the start of the measurement week.",
    )
    meeting_hours: float = Field(
        ...,
        description="Total meeting hours logged during the week.",
    )
    message_count: int = Field(
        ...,
        description="Total messages sent/received during the week.",
    )
    focus_hours: float = Field(
        ...,
        description="Total uninterrupted focus hours during the week.",
    )
    optimization_tips: list[str] = Field(
        default_factory=list,
        description="Personalised workload optimisation suggestions based on current signals.",
    )


class GetMySignalsResponse(BaseModel):
    """Response payload for the get_my_signals MCP tool."""

    employee_id: str = Field(
        ...,
        description="Echo of the authenticated employee identifier.",
    )
    current: PersonalSignalItem = Field(
        ...,
        description="Workload metrics for the current/most recent week.",
    )
    baseline: PersonalSignalItem | None = Field(
        default=None,
        description=(
            "Expected workload metrics derived from RoleBaseline. "
            "None if no baseline has been configured for this role."
        ),
    )
