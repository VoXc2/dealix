"""
Public endpoints — no auth, CORS-open. Used by the landing page.

Routes:
  POST /api/v1/public/demo-request   — landing form submission
    Body: DemoRequestIn (see model)
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
  POST /api/v1/public/partner-application — agency/freelancer signup
  GET  /api/v1/public/health         — unauthenticated liveness probe
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from dealix.analytics import FUNNEL_EVENTS, capture_event

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/public", tags=["public"])


# CALENDLY_URL must be configured via environment in production. The previous
# default leaked a personal handle; we now refuse to serve a booking link if
# unset, which forces a real config decision and protects founder PII.
CALENDLY_URL = os.getenv("CALENDLY_URL", "").strip()


class DemoRequestIn(BaseModel):
    """Public demo-request payload. Tight bounds — landing form is hostile-input territory."""

    name: str = Field(..., min_length=1, max_length=120)
    company: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=20, pattern=r"^\+?[0-9\s\-()]+$")
    sector: str = Field(default="", max_length=80)
    size: str = Field(default="", max_length=40)
    message: str = Field(default="", max_length=2000)
    consent: bool
    # Honeypot — bots happily fill this; humans never see it.
    website: str | None = Field(default=None, max_length=200)
    source: str = Field(default="landing.demo_form", max_length=80)
    ref: str = Field(default="", max_length=120)


class PartnerApplicationIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    company: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    phone: str = Field(default="", max_length=20, pattern=r"^\+?[0-9\s\-()]*$")
    partnership_type: str = Field(default="referral", max_length=40)
    services: str = Field(default="", max_length=500)
    active_clients: str = Field(default="0", max_length=10)
    why: str = Field(default="", max_length=1000)


def _booking_url_or_503() -> str:
    if not CALENDLY_URL:
        log.error("calendly_url_unconfigured")
        raise HTTPException(status_code=503, detail="booking_unavailable")
    return CALENDLY_URL


@router.post("/demo-request")
async def demo_request(payload: DemoRequestIn) -> dict[str, Any]:
    """Public landing form — captures demo request and returns Calendly booking URL."""
    # Honeypot — silently accept and drop bot submissions (never reveal config).
    if payload.website:
        log.info("demo_request_honeypot_triggered")
        return {"ok": True, "calendly_url": CALENDLY_URL or ""}

    if not payload.consent:
        raise HTTPException(status_code=422, detail="consent_required")

    booking_url = _booking_url_or_503()

    # Fire PostHog event (fire-and-forget — never blocks response)
    try:
        await capture_event(
            (
                FUNNEL_EVENTS.DEMO_REQUESTED
                if hasattr(FUNNEL_EVENTS, "DEMO_REQUESTED")
                else "demo_requested"
            ),
            distinct_id=payload.email,
            properties={
                "name": payload.name,
                "company": payload.company,
                "email": payload.email,
                "phone": payload.phone,
                "sector": payload.sector,
                "size": payload.size,
                "message_len": len(payload.message),
                "source": "landing.demo_form",
            },
        )
    except Exception:
        # Analytics is best-effort; never 5xx the public form.
        log.exception("posthog_capture_failed")

    # Persist to local lead-inbox (gitignored var/lead-inbox.jsonl) so the
    # founder can review every inquiry in /api/v1/founder/leads. Best-effort.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": payload.name,
            "company": payload.company,
            "email": payload.email,
            "phone": payload.phone,
            "sector": payload.sector,
            "size": payload.size,
            "message": payload.message,
            "consent": payload.consent,
            "source": payload.source,
            "ref": payload.ref,
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    log.info(
        "demo_request_accepted email=%s company=%s sector=%s lead_id=%s",
        payload.email,
        payload.company,
        payload.sector,
        lead_id,
    )

    return {
        "ok": True,
        "calendly_url": booking_url,
        "message": "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل",
        "lead_id": lead_id,
    }


@router.get("/health")
async def public_health() -> dict[str, Any]:
    """Unauthenticated health probe for landing page to show live status."""
    return {"ok": True, "service": "dealix-api"}


@router.post("/partner-application")
async def partner_application(req: Request) -> dict[str, Any]:
    """Public partner signup — for agencies/freelancers/consultants.

    Accepts JSON or form-urlencoded (Formspree-style) bodies. Validates via
    PartnerApplicationIn after normalising shape.
    """
    try:
        body: dict[str, Any] = await req.json()
    except (ValueError, UnicodeDecodeError):
        # Form-urlencoded fallback for partner pages embedding Formspree-style HTML forms.
        form = await req.form()
        body = dict(form)

    # Normalise alternate field names before validation.
    if "type" in body and "partnership_type" not in body:
        body["partnership_type"] = body.pop("type")
    if "clients" in body and "active_clients" not in body:
        body["active_clients"] = body.pop("clients")

    try:
        payload = PartnerApplicationIn(**body)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="missing_required_fields") from exc

    log.info(
        "partner_application_received company=%s type=%s clients=%s",
        payload.company,
        payload.partnership_type,
        payload.active_clients,
    )

    try:
        await capture_event(
            "partner_application_submitted",
            distinct_id=payload.email or payload.company or "anonymous",
            properties={
                "company": payload.company,
                "partnership_type": payload.partnership_type,
                "active_clients": payload.active_clients,
                "has_phone": bool(payload.phone),
                "has_services": bool(payload.services),
                "has_why": bool(payload.why),
                "source": "dealix.partners_page",
            },
        )
    except Exception:
        log.warning("posthog_capture_failed", exc_info=True)

    return {
        "ok": True,
        "message": "وصلنا طلبك. سنتواصل خلال 48 ساعة.",
        "next_step": "email_review",
    }
