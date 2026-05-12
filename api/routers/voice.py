"""
Voice channel router — Vapi webhook + transcripts + outbound call.

Endpoints:
    POST /api/v1/voice/inbound        — Vapi webhook (HMAC-verified)
    POST /api/v1/voice/outbound       — initiate outbound call
    GET  /api/v1/voice/transcripts/{call_id} — recall a transcript
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field

from core.logging import get_logger
from dealix.voice.vapi_client import is_configured as vapi_configured
from dealix.voice.vapi_client import place_outbound, verify_signature

router = APIRouter(prefix="/api/v1/voice", tags=["voice"])
log = get_logger(__name__)


class OutboundCallIn(BaseModel):
    to: str = Field(..., min_length=7, max_length=20, pattern=r"^\+?[0-9]+$")
    tenant_id: str = Field(..., max_length=64)
    assistant_id: str = Field(..., max_length=64)
    locale: str = Field(default="ar", max_length=8)


@router.post("/inbound")
async def vapi_inbound(
    req: Request,
    vapi_signature: str = Header(default="", alias="X-Vapi-Signature"),
) -> dict[str, Any]:
    body = await req.body()
    if not verify_signature(body, vapi_signature):
        log.warning("vapi_bad_signature")
        raise HTTPException(status_code=400, detail="invalid_signature")
    try:
        evt = await req.json()
    except Exception:
        evt = {}
    msg_type = (evt.get("message") or {}).get("type") or evt.get("type", "unknown")
    log.info(
        "vapi_inbound_received",
        msg_type=msg_type,
        call_id=(evt.get("call") or {}).get("id"),
    )

    # Function-call dispatch: when Vapi requests `lead_capture` /
    # `qualify` / `book_meeting`, route to the existing routers.
    fn = (evt.get("message") or {}).get("functionCall") or {}
    name = fn.get("name", "")
    params = fn.get("parameters", {}) or {}
    if name == "lead_capture":
        from auto_client_acquisition import lead_inbox

        rec = lead_inbox.append({
            "name": params.get("name", ""),
            "company": params.get("company", ""),
            "email": params.get("email", ""),
            "phone": params.get("phone", ""),
            "sector": params.get("sector", ""),
            "consent": True,
            "source": "voice.vapi",
        })
        return {"ok": True, "lead_id": rec.get("id")}
    if name == "escalate":
        return {"ok": True, "action": "queue_human"}

    return {"ok": True}


@router.post("/outbound")
async def voice_outbound(payload: OutboundCallIn, request: Request) -> dict[str, Any]:
    if not vapi_configured():
        raise HTTPException(503, "vapi_not_configured")
    # PDPL gate — outbound voice requires prior consent. The caller
    # is expected to assert consent against the contact registry
    # before invoking us; we audit the action regardless.
    result = await place_outbound(
        to=payload.to,
        assistant_id=payload.assistant_id,
        tenant_id=payload.tenant_id,
        locale=payload.locale,
    )
    log.info(
        "voice_outbound_placed",
        tenant_id=payload.tenant_id,
        to_prefix=payload.to[:6],
        ok=result.ok,
        call_id=result.call_id,
    )
    return {"ok": result.ok, "call_id": result.call_id, "error": result.error}


@router.get("/transcripts/{call_id}")
async def voice_transcript(call_id: str) -> dict[str, Any]:
    """Pull the transcript for a completed call (Vapi proxy)."""
    api_key = os.getenv("VAPI_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(503, "vapi_not_configured")
    import httpx

    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"https://api.vapi.ai/call/{call_id}",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        raise HTTPException(502, "vapi_upstream_error") from None
    return {
        "call_id": call_id,
        "status": data.get("status"),
        "transcript": data.get("transcript", ""),
        "summary": data.get("summary", ""),
        "duration_sec": data.get("duration"),
    }
