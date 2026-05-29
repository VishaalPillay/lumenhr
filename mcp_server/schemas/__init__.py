"""
MCP Server Pydantic Schemas — Barrel Exports.

Import all data contracts from here:
    from mcp_server.schemas import GetTeamSignalsRequest, GetTeamSignalsResponse
"""

# ── Signals (get_team_signals, get_member_trend, get_org_risk_map, get_my_signals)
from .signals import (  # noqa: F401
    GetTeamSignalsRequest,
    TeamSummaryMetrics,
    MemberSignalSummary,
    GetTeamSignalsResponse,
    GetMemberTrendRequest,
    WeeklyTrendPoint,
    GetMemberTrendResponse,
    GetOrgRiskMapRequest,
    DepartmentRiskSummary,
    GetOrgRiskMapResponse,
    GetMySignalsRequest,
    PersonalSignalItem,
    GetMySignalsResponse,
)

# ── Scores (recommend_task_assignment)
from .scores import (  # noqa: F401
    RecommendTaskAssignmentRequest,
    CandidateMatch,
    RecommendTaskAssignmentResponse,
)

# ── Interventions (get_intervention_playbook, create_checkin_event,
#                    log_intervention, escalate_to_hr)
from .interventions import (  # noqa: F401
    GetInterventionPlaybookRequest,
    PlaybookAction,
    GetInterventionPlaybookResponse,
    CreateCheckinEventRequest,
    CreateCheckinEventResponse,
    LogInterventionRequest,
    LogInterventionResponse,
    EscalateToHrRequest,
    EscalateToHrResponse,
)

# ── Employee (get_policy_info, draft_workload_email)
from .employee import (  # noqa: F401
    GetPolicyInfoRequest,
    PolicyBlock,
    GetPolicyInfoResponse,
    DraftWorkloadEmailRequest,
    DraftWorkloadEmailResponse,
)
