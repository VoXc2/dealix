"""Customer Data & Consent Plane v5 — read/write API over the registry."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

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
