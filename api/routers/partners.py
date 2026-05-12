"""
Partners router — deal registration for the agency/referral channel.

Distinct from `partnership_os` (which is the intelligence + scoring engine
for strategic partnerships). This router is the lightweight, customer-
facing "I sourced a lead" capture surface used by signed-up partners.

Endpoints:
    POST /api/v1/partners/deals/register — record a partner-introduced lead
    GET  /api/v1/partners/health         — liveness for partner portals

Behaviour:
    - No auth at the moment — partners are identified by `partner_id` in the
      payload, validated against a partner registry the founder maintains
      manually. A future iteration will mint per-partner API keys.
    - Persists to the same lead-inbox the demo form uses, tagged so the
      founder's daily digest distinguishes partner-sourced leads.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/partners", tags=["partners"])


class DealRegistration(BaseModel):
    """A lead introduced by a registered partner."""

    partner_id: str = Field(..., min_length=2, max_length=64)
    prospect_company: str = Field(..., min_length=1, max_length=120)
    prospect_email: EmailStr
    prospect_name: str = Field(default="", max_length=120)
    prospect_phone: str = Field(default="", max_length=20, pattern=r"^\+?[0-9\s\-()]*$")
    sector: str = Field(default="", max_length=80)
    expected_deal_sar: float | None = Field(default=None, ge=0)
    notes: str = Field(default="", max_length=2000)
    introduced_via: str = Field(default="email", max_length=40)


@router.post("/deals/register")
async def register_partner_deal(payload: DealRegistration) -> dict[str, Any]:
    """Record a partner-introduced lead.

    Idempotency note: there is no dedupe on this endpoint yet — if the same
    deal is registered twice, the founder reconciles manually. Acceptable
    until partner volume justifies a deal-registry table.
    """
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox

        rec = lead_inbox.append({
            "name": payload.prospect_name,
            "company": payload.prospect_company,
            "email": payload.prospect_email,
            "phone": payload.prospect_phone,
            "sector": payload.sector,
            "message": payload.notes,
            "consent": True,  # partner attests on the prospect's behalf
            "source": f"partner:{payload.partner_id}",
            "ref": payload.introduced_via,
            "event": "partner_deal_registered",
            "expected_deal_sar": payload.expected_deal_sar,
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("partner_deal_inbox_failed")
        # If we cannot capture the lead, the partner needs to know.
        raise HTTPException(status_code=503, detail="lead_capture_unavailable") from None

    try:
        from dealix.analytics import capture_event

        await capture_event(
            "partner_deal_registered",
            distinct_id=payload.prospect_email,
            properties={
                "partner_id": payload.partner_id,
                "company": payload.prospect_company,
                "sector": payload.sector,
                "expected_deal_sar": payload.expected_deal_sar,
                "introduced_via": payload.introduced_via,
            },
        )
    except Exception:
        log.warning("posthog_capture_failed", exc_info=True)

    log.info(
        "partner_deal_registered partner=%s company=%s lead=%s value_sar=%s",
        payload.partner_id,
        payload.prospect_company,
        lead_id,
        payload.expected_deal_sar,
    )

    return {
        "ok": True,
        "lead_id": lead_id,
        "partner_id": payload.partner_id,
        "ack_message": (
            "Deal registered. The founder will reach out to confirm next steps "
            "and commission terms within one business day."
        ),
    }


@router.get("/health")
async def partners_health() -> dict[str, Any]:
    """Lightweight liveness probe for partner portal embeds."""
    return {"ok": True, "service": "dealix-partners"}
