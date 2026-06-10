"""Customer Data & Consent Plane v5 — read/write API over the registry.

V12 extension: ``POST /action-check`` evaluates the action × channel
× consent matrix using ``compliance_os_v12.action_policy``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.compliance_os_v12 import (
    Channel,
    ConsentState,
    evaluate_action,
)
from auto_client_acquisition.customer_data_plane import (
    ChannelKind,
    contactability_check,
    get_default_registry,
    redact_text,
)
from auto_client_acquisition.customer_data_plane.consent_registry import (
    ConsentSource,
)

router = APIRouter(prefix="/api/v1/customer-data", tags=["customer-data-plane"])


class _ActionCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action_type: str
    channel: Channel = "internal"
    consent_state: ConsentState = "unknown"
    customer_id: str | None = None


@router.post("/action-check")
async def action_check(req: _ActionCheckRequest) -> dict[str, Any]:
    """Evaluate the V12 action × channel × consent policy matrix.

    Read-only. No DB write. No external call. Returns a deterministic
    verdict ``allowed | blocked | needs_review`` with bilingual reasons.
    """
    decision = evaluate_action(
        action_type=req.action_type,
        channel=req.channel,
        consent_state=req.consent_state,
        customer_id=req.customer_id,
    )
    return {
        "verdict": decision.verdict,
        "action_mode": decision.action_mode,
        "escalate_to_human": decision.escalate_to_human,
        "reason_ar": decision.reason_ar,
        "reason_en": decision.reason_en,
        "request": req.model_dump(mode="json"),
        "hard_gates": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "no_linkedin_automation": True,
            "no_fake_proof": True,
        },
    }


@router.get("/status")
async def status() -> dict:
    return {
        "module": "customer_data_plane",
        "guardrails": {
            "default_unknown_consent_is_blocked": True,
            "withdraw_propagates_immediately": True,
            "no_purchased_lists_accepted": True,
        },
    }


@router.post("/consent/grant")
async def consent_grant(payload: dict = Body(...)) -> dict:
    contact_id = payload.get("contact_id")
    channel = payload.get("channel")
    source = payload.get("source", "website_form")
    if not contact_id or not channel:
        raise HTTPException(status_code=400, detail="contact_id and channel required")
    try:
        rec = get_default_registry().grant(
            contact_id=str(contact_id),
            channel=str(channel),
            source=str(source),
            purposes=payload.get("purposes") or [],
            method_note=str(payload.get("method_note", "")),
            evidence_id=payload.get("evidence_id"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return rec.model_dump(mode="json")


@router.post("/consent/withdraw")
async def consent_withdraw(payload: dict = Body(...)) -> dict:
    contact_id = payload.get("contact_id")
    if not contact_id:
        raise HTTPException(status_code=400, detail="contact_id required")
    channel = payload.get("channel")
    try:
        out = get_default_registry().withdraw(
            contact_id=str(contact_id),
            channel=str(channel) if channel else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"withdrawn_count": len(out), "records": [r.model_dump(mode="json") for r in out]}


@router.post("/contactability/check")
async def contactability(payload: dict = Body(...)) -> dict:
    contact_id = payload.get("contact_id")
    channel = payload.get("channel")
    if not contact_id or not channel:
        raise HTTPException(status_code=400, detail="contact_id and channel required")
    try:
        result = contactability_check(str(contact_id), str(channel))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.to_dict()


@router.post("/redact")
async def redact_endpoint(payload: dict = Body(...)) -> dict:
    text = payload.get("text", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=400, detail="payload.text must be a string")
    return {"redacted": redact_text(text)}
