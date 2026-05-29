"""
Pydantic v2 data contracts for score-related MCP tools.

Tools covered:
  - recommend_task_assignment  (HR & Manager Agent)
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── recommend_task_assignment ─────────────────────────────────────────────────


class RecommendTaskAssignmentRequest(BaseModel):
    """Request payload for the recommend_task_assignment MCP tool."""

    required_skills: list[str] = Field(
        ...,
        description=(
            "List of skill tags required for the task "
            "(e.g. ['python', 'data-engineering'])."
        ),
    )
    task_weight_hours: float = Field(
        ...,
        description="Estimated effort in hours to complete the task.",
    )


class CandidateMatch(BaseModel):
    """A single candidate employee ranked for task assignment."""

    employee_id: str = Field(
        ...,
        description="Unique employee identifier (e.g. EMP-003).",
    )
    display_name: str = Field(
        ...,
        description="Human-readable display name of the employee.",
    )
    skill_compatibility_index: float = Field(
        ...,
        description=(
            "Normalised compatibility score between 0.0 and 1.0 "
            "indicating how well the employee's skills match the requirements."
        ),
    )
    current_cognitive_load: int = Field(
        ...,
        description=(
            "Current cognitive load score (0-100) sourced directly "
            "from PreComputedScore.score in PostgreSQL."
        ),
    )
    risk_tier: str = Field(
        ...,
        description="Current burnout risk classification: LOW, MODERATE, HIGH, CRITICAL.",
    )
    available_capacity_hours: float = Field(
        ...,
        description=(
            "Estimated remaining capacity in hours before the employee "
            "exceeds their role baseline overload threshold."
        ),
    )


class RecommendTaskAssignmentResponse(BaseModel):
    """Response payload for the recommend_task_assignment MCP tool."""

    candidates: list[CandidateMatch] = Field(
        ...,
        description=(
            "Prioritised list of qualified team members ranked by skill "
            "compatibility and available cognitive capacity."
        ),
    )
