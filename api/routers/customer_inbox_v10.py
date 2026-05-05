"""Customer Inbox v10 — Chatwoot-inspired API surface.

All outbound is draft_only / approval_required / blocked. NEVER live-send.
"""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.customer_inbox_v10 import (
    Channel,
    Conversation,
    add_inbound,
    compute_sla,
    sla_table,
    start_conversation,
    suggest_reply,
)

router = APIRouter(prefix="/api/v1/customer-inbox-v10", tags=["customer-inbox-v10"])


# In-memory ephemeral store keyed by conversation id.
_CONV_STORE: dict[str, Conversation] = {}


@router.get("/status")
async def status() -> dict:
    return {
        "module": "customer_inbox_v10",
        "guardrails": {
            "no_auto_send_external": True,
            "no_cold_whatsapp": True,
            "manual_linkedin_only": True,
            "approval_required_for_external_actions": True,
            "no_pii_in_messages": True,
        },
    }


@router.post("/conversation/start")
async def conversation_start(payload: dict = Body(...)) -> dict:
    handle = payload.get("customer_handle")
    channel = payload.get("channel")
    if not handle or not channel:
        raise HTTPException(status_code=400, detail="customer_handle and channel required")
    try:
        conv = start_conversation(str(handle), Channel(channel))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _CONV_STORE[conv.id] = conv
    return conv.model_dump(mode="json")


@router.post("/conversation/{conv_id}/inbound")
async def conversation_inbound(conv_id: str, payload: dict = Body(...)) -> dict:
    conv = _CONV_STORE.get(conv_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    body = payload.get("body", "")
    if not isinstance(body, str):
        raise HTTPException(status_code=400, detail="body must be string")
    conv = add_inbound(conv, body)
    _CONV_STORE[conv.id] = conv
    return conv.model_dump(mode="json")


@router.post("/suggest-reply")
async def suggest_reply_endpoint(payload: dict = Body(...)) -> dict:
    try:
        conv = Conversation.model_validate(payload)
    except Exception as exc:  # pragma: no cover - pydantic raises ValidationError
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return suggest_reply(conv).model_dump(mode="json")


@router.post("/sla-status")
async def sla_status_endpoint(payload: dict = Body(...)) -> dict:
    try:
        conv = Conversation.model_validate(payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return compute_sla(conv).model_dump(mode="json")


@router.get("/sla-policy")
async def sla_policy_endpoint() -> dict:
    return {
        "schema_version": 1,
        "channel_targets_hours": sla_table(),
    }
