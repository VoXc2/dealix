"""Compliance OS — action-check matrix (no persistence)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from auto_client_acquisition.compliance_action import assess_external_action

router = APIRouter(prefix="/api/v1/compliance-os", tags=["compliance-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "compliance_action",
        "policies": ["pdpl_contact_first", "approval_first_external", "no_cold_whatsapp"],
    }


@router.post("/action-check")
async def action_check(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    action = str(payload.get("action_type", "") or "")
    has_consent = bool(payload.get("has_consent", False))
    founder_approved = bool(payload.get("founder_approved", False))
    result = assess_external_action(action, has_consent=has_consent, founder_approved=founder_approved)
    return {"action_type": action, **result}
