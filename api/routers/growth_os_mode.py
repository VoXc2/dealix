"""Growth OS — alias status for revenue execution naming."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/growth-os", tags=["growth-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "growth_os",
        "delegate": "growth_v10",
        "primary": "/api/v1/growth-v10/status",
        "guardrails": {
            "no_pii_in_events": True,
            "no_auto_publish": True,
            "no_marketing_claims": True,
            "approval_required_for_campaign_run": True,
            "consent_required_default": True,
        },
    }
