"""
Public endpoints — no auth, CORS-open. Used by the landing page.

Routes:
  POST /api/v1/public/demo-request   — landing form submission
    Body: {name, company, email, phone, sector?, size?, message?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
  POST /api/v1/public/risk-score     — AI & Revenue Ops risk-score lead magnet
    Body: {company, email, consent, governance answers, website(honeypot)}
    Returns: {ok: true, risk_score, risk_band, gaps, recommended_next_step, ...}
  POST /api/v1/public/partner-application — agency/freelancer partner signup
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from auto_client_acquisition import risk_score as risk_score_engine
from dealix.analytics import FUNNEL_EVENTS, capture_event

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/public", tags=["public"])


CALENDLY_URL = os.getenv(
    "CALENDLY_URL",
    "https://calendly.com/sami-assiri11/dealix-demo",
)


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
                "source": "landing.demo_form",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    # Persist to local lead-inbox (gitignored var/lead-inbox.jsonl) so the
    # founder can review every inquiry in /api/v1/founder/leads — completes
    # the previous TODO. Best-effort: failure never 5xx the public form.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "sector": sector,
            "size": size,
            "message": message,
            "consent": consent,
            "source": str(body.get("source") or "landing.demo_form"),
            "ref": str(body.get("ref") or ""),
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    log.info(
        "demo_request_accepted email=%s company=%s sector=%s lead_id=%s",
        email,
        company,
        sector,
        lead_id,
    )

    # Wave 14B activation: fire transactional confirmation email — best-effort,
    # never blocks the 200 response. Whitelisted kind only; Gmail OAuth
    # configured via env. If Gmail isn't set up, this no-ops gracefully.
    transactional_status = "skipped_not_configured"
    try:
        from auto_client_acquisition.email.transactional import (
            render_diagnostic_intake_confirmation,
            send_transactional,
        )
        subject, body_plain = render_diagnostic_intake_confirmation(
            customer_name=name, sector=sector or "b2b_services"
        )
        send_result = await send_transactional(
            kind="diagnostic_intake_confirmation",
            to_email=email,
            subject=subject,
            body_plain=body_plain,
        )
        transactional_status = send_result.reason_code
    except Exception:
        log.exception("transactional_confirmation_failed")
        transactional_status = "exception_caught"

    return {
        "ok": True,
        "calendly_url": CALENDLY_URL,
        "message": "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل",
        "lead_id": lead_id,
        "transactional_confirmation": transactional_status,
        "governance_decision": "allow",
    }


@router.post("/risk-score")
async def risk_score(req: Request) -> dict[str, Any]:
    """Public lead-magnet — AI & Revenue Ops governance risk score.

    Body: {company, email, name?, phone?, sector?, team_size?, budget_band?,
           urgency?, consent, website(honeypot), plus the six governance
           control answers — has_crm, pipeline_reliable,
           approval_before_external_action, followup_documented,
           can_link_workflow_to_value, has_evidence_pack — and uses_ai}.
    Returns: the estimated risk score, gaps, and recommended next step.
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: silently drop bots without persisting.
    if body.get("website"):
        log.info("risk_score_honeypot_triggered")
        return {"ok": True, **risk_score_engine.score({})}

    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    name = str(body.get("name") or "").strip()

    if not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not bool(body.get("consent")):
        raise HTTPException(status_code=422, detail="consent_required")

    result = risk_score_engine.score(body)

    # Persist to founder lead inbox — review-only, no automated outreach.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox

        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": str(body.get("phone") or "").strip(),
            "sector": str(body.get("sector") or "").strip(),
            "team_size": str(body.get("team_size") or "").strip(),
            "budget_band": str(body.get("budget_band") or "").strip(),
            "urgency": str(body.get("urgency") or "").strip(),
            "consent": True,
            "source": str(body.get("source") or "landing.risk_score"),
            "ref": str(body.get("ref") or ""),
            "risk_score": result["risk_score"],
            "risk_band": result["risk_band"],
            "gap_count": result["gap_count"],
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("risk_score_lead_inbox_append_failed")

    try:
        await capture_event(
            "risk_score_submitted",
            distinct_id=email,
            properties={
                "company": company,
                "risk_score": result["risk_score"],
                "risk_band": result["risk_band"],
                "gap_count": result["gap_count"],
                "source": "landing.risk_score",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    log.info(
        "risk_score_accepted email=%s company=%s score=%s band=%s lead_id=%s",
        email,
        company,
        result["risk_score"],
        result["risk_band"],
        lead_id,
    )

    return {
        "ok": True,
        "lead_id": lead_id,
        "governance_decision": "allow",
        **result,
    }


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
