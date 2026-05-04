"""Role Command OS v5 — bilingual brief per role, read-only."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.role_command_os import (
    RoleName,
    build_role_brief,
    list_roles,
)

router = APIRouter(prefix="/api/v1/role-command", tags=["role-command-os"])


@router.get("/status")
async def role_command_status() -> dict:
    return {
        "module": "role_command_os",
        "roles": list_roles(),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/{role}")
async def get_role_brief(role: str) -> dict:
    """Get a single role's brief.

    Roles: ceo, sales, growth, partnership, cs, finance, compliance.
    """
    try:
        r = RoleName(role)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"unknown role: {role}; valid: {list_roles()}",
        ) from exc
    brief = build_role_brief(r)
    return brief.as_dict()
