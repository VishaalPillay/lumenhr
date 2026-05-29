"""
Pydantic v2 data contracts for Employee Agent MCP tools.

Tools covered:
  - get_policy_info       (Employee Agent)
  - draft_workload_email  (Employee Agent)
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── get_policy_info ───────────────────────────────────────────────────────────


class GetPolicyInfoRequest(BaseModel):
    """Request payload for the get_policy_info MCP tool."""

    query_string: str = Field(
        ...,
        description=(
            "Natural-language query describing the policy information "
            "the employee is looking for (e.g. 'parental leave entitlements')."
        ),
    )


class PolicyBlock(BaseModel):
    """A single policy information block returned from the Foundry IQ document store."""

    title: str = Field(
        ...,
        description="Title of the matching corporate policy section.",
    )
    content: str = Field(
        ...,
        description="Full text content of the relevant policy section.",
    )
    section_reference: str = Field(
        ...,
        description="Formal section reference within the source document (e.g. '§3.2').",
    )
    source_id: str = Field(
        ...,
        description="Unique identifier of the source document in the Foundry IQ store.",
    )


class GetPolicyInfoResponse(BaseModel):
    """Response payload for the get_policy_info MCP tool."""

    results: list[PolicyBlock] = Field(
        ...,
        description="List of policy blocks matching the employee's query, with formal citations.",
    )


# ── draft_workload_email ──────────────────────────────────────────────────────


class DraftWorkloadEmailRequest(BaseModel):
    """Request payload for the draft_workload_email MCP tool."""

    recipient_manager_id: str = Field(
        ...,
        description="Azure AD object-id of the manager who will receive the workload email.",
    )
    focus_areas: list[str] = Field(
        ...,
        description=(
            "List of workload focus areas the employee wants to address "
            "(e.g. ['meeting_overload', 'after_hours_messages'])."
        ),
    )


class DraftWorkloadEmailResponse(BaseModel):
    """Response payload for the draft_workload_email MCP tool."""

    subject: str = Field(
        ...,
        description="Generated email subject line.",
    )
    body_markdown: str = Field(
        ...,
        description=(
            "Full email body in markdown format. Framed using structural "
            "baseline facts. Intended for manual review and sending by the employee."
        ),
    )
    disclaimer: str = Field(
        ...,
        description=(
            "Legal disclaimer reminding the employee that this draft must be "
            "manually sent — direct system-automated mailing is forbidden."
        ),
    )
