"""Role Command OS v5 — bilingual brief per role, read-only."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.role_command_os import (
    RoleName,
    build_role_brief,
    list_roles,
)

router = APIRouter(prefix="/api/v1/role-command", tags=["role-command-os"])


def _role_command_status_payload() -> dict:
    return {
        "service": "role_command_os",
        "module": "role_command_os",
        "status": "operational",
        "version": "v5",
        "degraded": False,
        "checks": {"roles_loaded": bool(list_roles())},
        "roles": list_roles(),
        "hard_gates": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
        "next_action_ar": "اختر الدور لرؤية ملخّصه اليومي",
        "next_action_en": "Pick a role to view its daily brief.",
        # Legacy shape preserved for back-compat with v5 callers:
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/status")
async def role_command_status() -> dict:
    return _role_command_status_payload()


@router.get("/_status")
async def role_command_status_alias() -> dict:
    """Path-collision-safe alias — guaranteed to never be matched as a role.

    The legacy ``/{role}`` catchall is registered AFTER ``/status``, so
    that path works too; this underscore alias is provided for callers
    that want a name unmistakably outside the role enum.
    """
    return _role_command_status_payload()


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
