"""
Public endpoints — no auth, CORS-open. Used by the landing page.

Routes:
  POST /api/v1/public/demo-request   — landing form submission
    Body: {name, company, email, phone, sector?, size?, message?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
"""

from __future__ import annotations

import hashlib
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from dealix.analytics import FUNNEL_EVENTS, capture_event

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/public", tags=["public"])


CALENDLY_URL = os.getenv(
    "CALENDLY_URL",
    "https://calendly.com/sami-assiri11/dealix-demo",
)


def _short_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:18]}"


def _dedup_hash(*parts: str) -> str:
    """Stable short hash used to dedupe form refills on the same email."""
    src = "|".join(p.strip().lower() for p in parts if p)
    return hashlib.sha1(src.encode("utf-8")).hexdigest()[:16]


async def _record_inbound_lead(
    *,
    name: str,
    company: str,
    email: str,
    phone: str,
    sector: str,
    size: str,
    message: str,
    request_id: str | None,
) -> str | None:
    """Persist an inbound demo request as a LeadRecord (idempotent on email).

    Returns the lead_id on success, None if the DB write was skipped.
    NEVER raises — the form submit must succeed even if the DB hiccups.
    Called fire-and-forget from the demo-request handler.
    """
    try:
        from sqlalchemy import select

        from db.models import LeadRecord
        from db.session import async_session_factory
    except Exception as exc:  # noqa: BLE001
        log.warning("inbound_lead_skipped_import_failed error=%s", exc)
        return None

    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)
    lead_id: str | None = None

    try:
        async with async_session_factory() as session:
            # Idempotent on email within 30d — refills update the existing row.
            existing = (await session.execute(
                select(LeadRecord)
                .where(LeadRecord.contact_email == email)
                .where(LeadRecord.created_at >= cutoff)
                .order_by(LeadRecord.created_at.desc())
                .limit(1)
            )).scalars().first()

            if existing is not None:
                lead_id = existing.id
                # Touch fields we care about on refill — never overwrite ID/created_at.
                if name and not existing.contact_name:
                    existing.contact_name = name[:255]
                if company and not existing.company_name:
                    existing.company_name = company[:255]
                if phone and not existing.contact_phone:
                    existing.contact_phone = phone[:32]
                if sector and not existing.sector:
                    existing.sector = sector[:64]
                if size and not existing.company_size:
                    existing.company_size = size[:32]
                if message and not existing.message:
                    existing.message = message[:8000]
                await session.commit()
                log.info(
                    "inbound_demo_request_received "
                    "lead_id=%s email=%s sector=%s request_id=%s mode=updated",
                    lead_id, email, sector, request_id,
                )
                return lead_id

            lead_id = _short_id("lead_")
            rec = LeadRecord(
                id=lead_id,
                source="website",
                company_name=company[:255] or "",
                contact_name=name[:255] or "",
                contact_email=email[:255] or None,
                contact_phone=phone[:32] or None,
                sector=sector[:64] or None,
                region="Saudi Arabia",
                company_size=size[:32] or None,
                status="new",
                message=message[:8000] or None,
                dedup_hash=_dedup_hash(email, phone),
            )
            session.add(rec)
            await session.commit()
        log.info(
            "inbound_demo_request_received "
            "lead_id=%s email=%s sector=%s request_id=%s mode=created",
            lead_id, email, sector, request_id,
        )
        return lead_id
    except Exception as exc:  # noqa: BLE001 — must never break the form response
        log.warning(
            "inbound_lead_write_skipped error=%s email=%s request_id=%s",
            type(exc).__name__, email, request_id,
        )
        return None


@router.post("/demo-request")
async def demo_request(req: Request) -> dict[str, Any]:
    """Public landing form — captures demo request and returns Calendly booking URL."""
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: if "website" field is filled, silently drop
    if body.get("website"):
        log.info("demo_request_honeypot_triggered")
        return {"ok": True, "calendly_url": CALENDLY_URL}

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    sector = str(body.get("sector") or "").strip()
    size = str(body.get("size") or "").strip()
    message = str(body.get("message") or "").strip()
    consent = bool(body.get("consent"))

    if not name or not company or "@" not in email or not phone:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not consent:
        raise HTTPException(status_code=422, detail="consent_required")

    # Persist as LeadRecord (defensive; never blocks the response).
    # Wrapped so even if the helper signature changes or it raises
    # unexpectedly, the visitor still gets the Calendly URL.
    request_id = req.headers.get("x-request-id")
    lead_id: str | None = None
    try:
        lead_id = await _record_inbound_lead(
            name=name, company=company, email=email, phone=phone,
            sector=sector, size=size, message=message,
            request_id=request_id,
        )
    except Exception as exc:  # noqa: BLE001 — never let DB write fail the form
        log.warning("inbound_lead_outer_skipped error=%s", type(exc).__name__)

    # Fire PostHog event (fire-and-forget — never blocks response)
    try:
        await capture_event(
            (
                FUNNEL_EVENTS.DEMO_REQUESTED
                if hasattr(FUNNEL_EVENTS, "DEMO_REQUESTED")
                else "demo_requested"
            ),
            distinct_id=email,
            properties={
                "name": name,
                "company": company,
                "email": email,
                "phone": phone,
                "sector": sector,
                "size": size,
                "message_len": len(message),
                "lead_id": lead_id or "",
                "source": "landing.demo_form",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    log.info(
        "demo_request_accepted email=%s company=%s sector=%s lead_id=%s",
        email, company, sector, lead_id,
    )

    response: dict[str, Any] = {
        "ok": True,
        "calendly_url": CALENDLY_URL,
        "message": "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل",
    }
    if lead_id:
        response["lead_id"] = lead_id
    return response


@router.get("/health")
async def public_health() -> dict[str, Any]:
    """Unauthenticated health probe for landing page to show live status."""
    return {"ok": True, "service": "dealix-api"}


@router.post("/partner-application")
async def partner_application(req: Request) -> dict[str, Any]:
    """Public partner signup — for agencies/freelancers/consultants."""
    try:
        body = await req.json()
    except Exception:
        # Also accept form-urlencoded submissions from Formspree-style forms
        form = await req.form()
        body = dict(form)

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    ptype = str(body.get("partnership_type") or body.get("type") or "referral").strip()
    services = str(body.get("services") or "").strip()
    active_clients = str(body.get("active_clients") or body.get("clients") or "0")
    why = str(body.get("why") or "").strip()

    if not name or not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")

    log.info(
        "partner_application_received company=%s type=%s clients=%s",
        company,
        ptype,
        active_clients,
    )

    try:
        await capture_event(
            "partner_application_submitted",
            distinct_id=email or company or "anonymous",
            properties={
                "company": company,
                "partnership_type": ptype,
                "active_clients": active_clients,
                "has_phone": bool(phone),
                "has_services": bool(services),
                "has_why": bool(why),
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
