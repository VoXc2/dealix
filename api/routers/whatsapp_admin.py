"""
WhatsApp Business admin endpoints — list / send approved Meta templates.

Templates are pre-registered with Meta (the customer-success agency or
the founder owns this in the Business Manager). This router gives the
operator a thin admin surface to (a) see which templates are approved,
(b) trigger a send via the existing `WhatsAppClient.send_template`.

All endpoints are admin-only — they read tenant_id from request.state
just like the rest of /api/v1/admin/*.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from core.logging import get_logger

router = APIRouter(prefix="/api/v1/admin/whatsapp", tags=["admin", "whatsapp"])
log = get_logger(__name__)


def _meta_creds() -> tuple[str, str, str] | None:
    """Return (waba_id, phone_number_id, access_token) or None when missing."""
    waba_id = os.getenv("META_WABA_ID", "").strip()
    phone_id = os.getenv("META_WHATSAPP_PHONE_NUMBER_ID", "").strip()
    token = os.getenv("META_WHATSAPP_ACCESS_TOKEN", "").strip()
    if not (waba_id and phone_id and token):
        return None
    return waba_id, phone_id, token


@router.get("/templates")
async def list_meta_templates(request: Request) -> dict[str, Any]:
    """List the customer's approved Meta WhatsApp templates."""
    creds = _meta_creds()
    if creds is None:
        raise HTTPException(503, "whatsapp_not_configured")
    waba_id, _, token = creds
    url = f"https://graph.facebook.com/v20.0/{waba_id}/message_templates"
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
                params={"fields": "name,language,category,status,components", "limit": 100},
            )
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("whatsapp_templates_fetch_failed")
        raise HTTPException(502, "meta_upstream_error") from None
    items = data.get("data", [])
    return {
        "count": len(items),
        "templates": [
            {
                "name": t.get("name"),
                "language": t.get("language"),
                "category": t.get("category"),
                "status": t.get("status"),
            }
            for t in items
        ],
    }


class WhatsAppTemplateSendIn(BaseModel):
    to: str = Field(..., min_length=7, max_length=20, pattern=r"^\+?[0-9]+$")
    template_name: str = Field(..., min_length=2, max_length=64)
    language_code: str = Field(default="ar", max_length=8)
    parameters: list[str] = Field(default_factory=list, max_length=20)


@router.post("/send")
async def send_template_message(
    payload: WhatsAppTemplateSendIn, request: Request
) -> dict[str, Any]:
    """Send a Meta-approved template message via the existing client."""
    try:
        from integrations.whatsapp import WhatsAppClient
    except Exception as exc:
        raise HTTPException(500, "whatsapp_client_unavailable") from exc

    components: list[dict[str, Any]] = []
    if payload.parameters:
        components.append(
            {
                "type": "body",
                "parameters": [{"type": "text", "text": p} for p in payload.parameters],
            }
        )
    client = WhatsAppClient()
    result = await client.send_template(
        to=payload.to,
        template_name=payload.template_name,
        language_code=payload.language_code,
        components=components,
    )
    return {
        "ok": result.success,
        "message_id": result.message_id,
        "error": result.error,
        "template": payload.template_name,
    }
