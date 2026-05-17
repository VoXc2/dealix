"""
Public endpoints — no auth, CORS-open. Used by the landing page.

Routes:
  POST /api/v1/public/demo-request   — landing form submission
    Body: {name, company, email, phone, sector?, size?, message?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

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


# ── Public Diagnostic Funnel (PR4) ────────────────────────────────
# Unauthenticated funnel endpoints. The /api/v1/public prefix is
# auth-exempt; all of these reuse the honeypot pattern above.


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "نعم"}


def _parse_budget(value: Any) -> float:
    digits = "".join(c for c in str(value or "") if c.isdigit())
    return float(digits) if digits else 0.0


def _public_risk_score(body: dict[str, Any]) -> dict[str, Any]:
    """Deterministic 0–100 readiness estimate from public form input.

    This is an ESTIMATE — it reads only the submitted form, never CRM
    data — so callers tag the result is_estimate=True with a source.
    """
    score = 0
    factors: list[str] = []

    role = str(body.get("role") or "").lower()
    if any(k in role for k in ("ceo", "founder", "owner", "coo", "cro",
                               "head", "مدير", "مؤسس", "رئيس")):
        score += 20
        factors.append("decision_maker_role")
    if str(body.get("company") or "").strip():
        score += 10
        factors.append("has_company")
    if _truthy(body.get("has_crm")):
        score += 15
        factors.append("has_crm_process")
    if _truthy(body.get("uses_ai")):
        score += 15
        factors.append("uses_or_plans_ai")

    region = str(body.get("region") or body.get("country") or "").lower()
    if any(k in region for k in ("saudi", "ksa", "gcc", "uae", "qatar",
                                 "سعود", "خليج", "الإمارات", "قطر")):
        score += 15
        factors.append("saudi_gcc_region")

    urgency = str(body.get("urgency") or "").lower()
    if any(k in urgency for k in ("urgent", "30", "now", "asap",
                                  "عاجل", "شهر", "الآن")):
        score += 15
        factors.append("near_term_urgency")
    if _parse_budget(body.get("budget")) >= 5000:
        score += 10
        factors.append("budget_5k_plus")

    score = min(100, score)
    band = "high" if score >= 65 else "medium" if score >= 35 else "low"
    return {"score": score, "band": band, "factors": factors}


@router.post("/leads")
async def public_lead(req: Request) -> dict[str, Any]:
    """Public diagnostic-funnel lead capture. Consent is mandatory."""
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    if body.get("website"):  # honeypot
        return {"ok": True}

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    if not name or not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not bool(body.get("consent")):
        raise HTTPException(status_code=422, detail="consent_required")

    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox

        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": str(body.get("phone") or "").strip(),
            "sector": str(body.get("sector") or "").strip(),
            "role": str(body.get("role") or "").strip(),
            "message": str(body.get("message") or "").strip(),
            "consent": True,
            "source": str(body.get("source") or "public.diagnostic_funnel"),
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("public_lead_inbox_append_failed")

    try:
        from auto_client_acquisition.evidence_control_plane_os.event_store import (
            record_evidence_event,
        )

        record_evidence_event(
            event_type="lead_captured",
            entity_type="lead",
            entity_id=lead_id or email,
            action="public_funnel_submit",
            summary_en=f"Public diagnostic-funnel lead captured: {company}",
            source="public.diagnostic_funnel",
        )
    except Exception:
        log.exception("public_lead_evidence_failed")

    return {"ok": True, "lead_id": lead_id, "next_step": "risk_score"}


@router.post("/risk-score")
async def public_risk_score(req: Request) -> dict[str, Any]:
    """Deterministic readiness estimate for the diagnostic funnel.

    Always returns is_estimate=True — the score reads only the submitted
    form, never persisted CRM data.
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    result = _public_risk_score(body if isinstance(body, dict) else {})

    try:
        from auto_client_acquisition.evidence_control_plane_os.event_store import (
            record_evidence_event,
        )

        record_evidence_event(
            event_type="risk_score_estimated",
            entity_type="lead",
            entity_id=str(body.get("email") or "anonymous"),
            action="public_risk_score",
            summary_en=f"Public risk score estimated: {result['score']}",
            payload={"score": result["score"], "band": result["band"]},
            is_estimate=True,
            source="public_diagnostic_estimate",
        )
    except Exception:
        log.exception("public_risk_score_evidence_failed")

    return {
        "score": result["score"],
        "band": result["band"],
        "factors": result["factors"],
        "is_estimate": True,
        "source": "public_diagnostic_estimate",
        "disclaimer": "تقدير أولي مبني على بياناتك فقط — ليس تقييماً نهائياً",
    }


@router.get("/proof-pack/sample")
async def public_proof_pack_sample() -> dict[str, Any]:
    """A synthetic sample Proof Pack. Contains NO real customer data."""
    return {
        "sample": True,
        "is_estimate": True,
        "source": "synthetic_sample",
        "disclaimer": "نموذج توضيحي ببيانات افتراضية — لا يحتوي بيانات عملاء حقيقية",
        "title_ar": "نموذج حزمة الإثبات",
        "title_en": "Sample Proof Pack",
        "sections": [
            {
                "id": "diagnosis",
                "title_en": "Operational Diagnosis",
                "body_en": "Illustrative finding: 38% of inbound leads waited "
                           ">24h for a first reply (synthetic figure).",
            },
            {
                "id": "opportunities",
                "title_en": "Qualified Opportunities",
                "body_en": "Illustrative output: 10 scored opportunities with "
                           "next actions (synthetic figures).",
            },
            {
                "id": "evidence",
                "title_en": "Evidence Trail",
                "body_en": "Every recommendation links to a sourced evidence "
                           "event — no unverified claims.",
            },
        ],
    }


@router.post("/support")
async def public_support(req: Request) -> dict[str, Any]:
    """Public support entry — opens a ticket via the support lifecycle."""
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    if body.get("website"):  # honeypot
        return {"ok": True}

    message = str(body.get("message") or "").strip()
    if not message:
        raise HTTPException(status_code=422, detail="message_required")

    from auto_client_acquisition.support import create_ticket

    ticket = create_ticket(
        subject=str(body.get("subject") or "").strip(),
        message=message,
        channel="public_form",
        customer_id=str(body.get("email") or "").strip() or None,
    )
    return {
        "ok": True,
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
        "message": "تم استلام طلبك — سنتواصل معك قريباً",
    }


@router.get("/services")
async def public_services() -> dict[str, Any]:
    """Public, read-only service catalog with disclosed pricing."""
    from auto_client_acquisition.service_catalog import list_offerings

    offerings = [o.model_dump(mode="json") for o in list_offerings()]
    return {"count": len(offerings), "services": offerings}
