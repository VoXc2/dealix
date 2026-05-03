"""
Calls router — recommend a call + generate script. NEVER auto-dials.

  POST /api/v1/calls/recommend  body: {reason, has_user_permission, customer_label?, deal_amount_sar?}
  POST /api/v1/calls/{id}/script body: {call_reason, customer?, offer_sar?}
  POST /api/v1/calls/dial-live  → ALWAYS 403 (until CALLS_ALLOW_LIVE_DIAL is True)
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.revenue_company_os.call_recommendation_engine import (
    can_dial_live, generate_script, recommend,
)
from core.config.settings import get_settings

router = APIRouter(prefix="/api/v1/calls", tags=["calls"])


@router.post("/recommend")
async def post_recommend(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    rec = recommend(
        reason=str(body.get("reason") or ""),
        has_user_permission=bool(body.get("has_user_permission", False)),
        customer_label=str(body.get("customer_label") or "العميل"),
        deal_amount_sar=body.get("deal_amount_sar"),
    )
    out: dict[str, Any] = {
        "allowed": rec.allowed,
        "reason": rec.reason,
        "title_ar": rec.title_ar,
        "why_now_ar": rec.why_now_ar,
        "duration_minutes": rec.duration_minutes,
        "objective_ar": rec.objective_ar,
        "risk_level": rec.risk_level,
    }
    if not rec.allowed:
        out["blocked_reason"] = rec.blocked_reason
        out["refusal_reason_ar"] = rec.refusal_reason_ar
    if rec.allowed:
        out["call_id"] = f"call_{uuid.uuid4().hex[:12]}"
    return out


@router.post("/{call_id}/script")
async def post_script(call_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    call_reason = str(body.get("call_reason") or "")
    if not call_reason:
        raise HTTPException(status_code=400, detail="call_reason_required")
    script = generate_script(
        call_reason=call_reason,
        customer=str(body.get("customer") or "العميل"),
        offer_sar=body.get("offer_sar"),
    )
    if not script:
        raise HTTPException(status_code=400, detail="unsupported_call_reason")
    return {"call_id": call_id, "script_ar": script}


@router.post("/dial-live")
async def dial_live() -> dict[str, Any]:
    """Hard-blocked: live dialing is never enabled by default.

    This endpoint ALWAYS returns 403 in current policy. The shape exists so
    future implementations have a single auditable entry point.
    """
    settings = get_settings()
    allowed, reason = can_dial_live(settings)
    if not allowed:
        raise HTTPException(status_code=403, detail=reason)
    raise HTTPException(
        status_code=501,
        detail="live dial not implemented — recommendation/script only.",
    )
