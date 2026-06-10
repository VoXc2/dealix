"""Channel Policy Gateway HTTP surface (Phase 8).

  POST /api/v1/channel-policy/check
  GET  /api/v1/channel-policy/status
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.channel_policy_gateway import check_channel_policy

router = APIRouter(
    prefix="/api/v1/channel-policy",
    tags=["channel-policy-gateway"],
)

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_linkedin_auto": True,
    "no_scraping": True,
    "no_blast": True,
    "no_purchased_lists": True,
    "approval_required_for_external_actions": True,
}

_VALID_CHANNELS = {"whatsapp", "email", "linkedin", "calls"}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "channel_policy_gateway",
        "version": "1.0.0",
        "supported_channels": sorted(_VALID_CHANNELS),
        "hard_gates": _HARD_GATES,
    }


@router.post("/check")
async def check(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    channel = payload.get("channel")
    action_kind = payload.get("action_kind")
    if channel not in _VALID_CHANNELS:
        raise HTTPException(status_code=422, detail=f"channel must be one of {sorted(_VALID_CHANNELS)}")
    if not action_kind:
        raise HTTPException(status_code=422, detail="action_kind required")

    decision = check_channel_policy(
        channel=channel,  # type: ignore[arg-type]
        action_kind=action_kind,
        consent_record_exists=bool(payload.get("consent_record_exists", False)),
        approved_template_or_24h_window=bool(payload.get("approved_template_or_24h_window", False)),
        live_gate_true=bool(payload.get("live_gate_true", False)),
        human_approved=bool(payload.get("human_approved", False)),
        customer_permission=bool(payload.get("customer_permission", False)),
        is_cold=bool(payload.get("is_cold", False)),
        is_blast=bool(payload.get("is_blast", False)),
        is_purchased_list=bool(payload.get("is_purchased_list", False)),
    )
    return {
        "decision": decision.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }
