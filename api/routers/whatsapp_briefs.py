"""
WhatsApp Briefs router — returns the WhatsApp text + a gated send endpoint.

  GET  /api/v1/whatsapp/brief?role=sales_manager
       Returns {role, text, render_meta}; rendering is local — no live send.

  POST /api/v1/whatsapp/brief/send-internal
       body: {role, partner_id?, customer_id?}
       SAFETY: returns 403 unless WHATSAPP_ALLOW_INTERNAL_SEND=true AND
       WHATSAPP_ALLOW_LIVE_SEND=true. By default both are False.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query

from api.routers.role_briefs import _gather_data
from auto_client_acquisition.revenue_company_os.role_brief_builder import (
    SUPPORTED_ROLES, build,
)
from auto_client_acquisition.revenue_company_os.whatsapp_brief_renderer import (
    can_send_internal_brief, render,
)
from core.config.settings import get_settings

router = APIRouter(prefix="/api/v1/whatsapp", tags=["whatsapp-briefs"])


@router.get("/brief")
async def get_brief(
    role: str = Query(...),
    partner_id: str | None = Query(default=None),
) -> dict[str, Any]:
    role = role.lower()
    if role not in SUPPORTED_ROLES:
        raise HTTPException(status_code=400, detail=f"unknown_role: {role}")
    data = await _gather_data(role, partner_id=partner_id, customer_id=None)
    brief = build(role, data=data)
    text = render(brief)
    return {
        "role": role,
        "text": text,
        "lines": text.count("\n") + 1,
        "decision_count": min(3, len(brief.get("top_decisions") or [])),
    }


@router.post("/brief/send-internal")
async def send_internal(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    settings = get_settings()
    allowed, reason = can_send_internal_brief(settings)
    if not allowed:
        raise HTTPException(status_code=403, detail=reason)

    role = str(body.get("role") or "").lower()
    if role not in SUPPORTED_ROLES:
        raise HTTPException(status_code=400, detail=f"unknown_role: {role}")

    # Even when allowed, we DO NOT actually push to WhatsApp from here.
    # The gate exists so future implementation can be wired safely; today we
    # return an explicit not-implemented message so no silent send happens.
    raise HTTPException(
        status_code=501,
        detail=(
            "send-internal not implemented — gate is open but the WhatsApp "
            "transport requires explicit Meta business setup + audited approval."
        ),
    )
