"""WhatsApp Decision Bot HTTP surface (Phase 7).

  GET  /api/v1/whatsapp-decision/status
  POST /api/v1/whatsapp-decision/brief
  POST /api/v1/whatsapp-decision/command
  POST /api/v1/whatsapp-decision/approval-preview

ADMIN-ONLY. NEVER customer outbound. NEVER live send.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from auto_client_acquisition.whatsapp_decision_bot import (
    SUPPORTED_COMMANDS,
    build_brief,
    parse_command,
    preview_action,
)

router = APIRouter(
    prefix="/api/v1/whatsapp-decision",
    tags=["whatsapp-decision-bot"],
)

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_customer_outbound": True,
    "no_cold_whatsapp": True,
    "no_blast": True,
    "no_purchased_lists": True,
    "internal_admin_only": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "whatsapp_decision_bot",
        "version": "1.0.0",
        "supported_commands": SUPPORTED_COMMANDS,
        "supports_customer_outbound": False,
        "hard_gates": _HARD_GATES,
    }


@router.post("/brief")
async def brief(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    customer_handle = payload.get("customer_handle")
    b = build_brief(customer_handle=customer_handle)
    return {**b, "hard_gates": _HARD_GATES}


@router.post("/command")
async def command(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    text = (payload.get("text") or "").strip()
    customer_handle = payload.get("customer_handle")
    result = parse_command(text=text, customer_handle=customer_handle)
    return {
        "command": result.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/approval-preview")
async def approval_preview(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    action_kind = payload.get("action_kind", "send_whatsapp")
    text_to_send = payload.get("text_to_send", "")
    target_handle = payload.get("target_handle")
    preview = preview_action(
        action_kind=action_kind,
        text_to_send=text_to_send,
        target_handle=target_handle,
    )
    return {
        "preview": preview.model_dump(mode="json"),
        "would_send_live_now": False,  # always false at this layer
        "hard_gates": _HARD_GATES,
    }
