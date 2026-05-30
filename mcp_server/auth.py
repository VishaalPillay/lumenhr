"""
FastAPI authentication dependency for LumenHR MCP Server.

Development mode:
    Identity is resolved from mock headers (X-Mock-User-Id, X-Mock-Role).

Production mode:
    TODO: Replace with Microsoft Entra ID (Azure AD) JWT Bearer validation
    using the ``msal`` and ``azure-identity`` libraries. The JWT ``sub``
    claim will populate ``user_id`` and ``roles`` claim will populate
    ``role``.
"""

from __future__ import annotations

from fastapi import Header, HTTPException
from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    """Resolved identity of the authenticated API caller."""

    user_id: str = Field(
        ...,
        description="Unique identifier of the caller (e.g. EMP-001).",
    )
    role: str = Field(
        ...,
        description=(
            "Role of the caller: MANAGER, EMPLOYEE, HR_ADMIN. "
            "Used for downstream authorization gating."
        ),
    )


def get_current_user(
    x_mock_user_id: str | None = Header(default=None),
    x_mock_role: str = Header(default="EMPLOYEE"),
) -> CurrentUser:
    """FastAPI dependency — resolves the current user from mock headers.

    Headers:
        X-Mock-User-Id (required): Maps to ``CurrentUser.user_id``.
        X-Mock-Role    (optional): Maps to ``CurrentUser.role``.
                                   Defaults to ``"EMPLOYEE"``.

    Raises:
        HTTPException 401: If the ``X-Mock-User-Id`` header is missing.
    """
    # TODO: Replace this mock implementation with real Entra ID JWT
    #       validation via ``msal``. Decode the Bearer token, extract
    #       the ``sub`` claim for user_id and ``roles`` for role.
    if not x_mock_user_id:
        raise HTTPException(
            status_code=401,
            detail="Missing X-Mock-User-Id header.",
        )
    return CurrentUser(user_id=x_mock_user_id, role=x_mock_role)
