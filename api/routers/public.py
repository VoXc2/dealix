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

from auto_client_acquisition.sales_os.client_risk_score import (
    ClientRiskSignals,
    client_risk_score,
)
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.qualification import qualify
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


# ── Public Diagnostic Funnel — Risk Score ──────────────────────────────────

# Roles that signal a decision-maker is in the room.
_OWNER_ROLES: frozenset[str] = frozenset({
    "founder", "co-founder", "cofounder", "ceo", "owner", "gm",
    "general manager", "managing director", "md", "partner",
})

# The biggest-pain options the funnel form offers.
_PAIN_KEYS: frozenset[str] = frozenset({
    "pipeline", "crm", "follow_up", "approvals", "reporting",
})

_RISK_SCORE_DISCLAIMER = (
    "Estimated fit is not a guaranteed outcome / "
    "الملاءمة التقديرية ليست نتيجة مضمونة."
)


def _truthy(value: Any) -> bool:
    """Coerce a JSON form value (bool / string / number) to a boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "1", "y", "on"}
    return bool(value)


def _risk_bucket(score: int, blocked: bool) -> str:
    """Map a 0-100 qualification score to a funnel bucket."""
    if blocked:
        return "blocked"
    if score >= 70:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


@router.post("/risk-score")
async def risk_score(req: Request) -> dict[str, Any]:
    """Public diagnostic funnel — compute a deterministic AI/revenue-ops fit score.

    Doctrine: empty input is rejected (422) and never produces a fabricated
    score. Scoring is deterministic (``sales_os.qualify``) — no LLM, no live
    send. The founder reviews every captured lead in ``/api/v1/founder/leads``.
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: silently accept, do not score, do not persist.
    if body.get("website"):
        log.info("risk_score_honeypot_triggered")
        return {"ok": True, "governance_decision": "allow"}

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    # Anti-fabrication: with no identity there is no score. Empty input must
    # never be turned into a synthesized result.
    if not name or not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")

    role = str(body.get("role") or "").strip()
    linkedin = str(body.get("linkedin") or "").strip()
    sector = str(body.get("sector") or "").strip()
    team_size = str(body.get("team_size") or "").strip()
    crm = _truthy(body.get("crm"))
    crm_system = str(body.get("crm_system") or "").strip()
    ai_usage = _truthy(body.get("ai_usage"))
    biggest_pain = str(body.get("biggest_pain") or "").strip().lower()
    consent_external = _truthy(body.get("consent_before_external_action"))
    link_value = _truthy(body.get("can_link_workflow_to_value"))
    budget_range = str(body.get("budget_range") or "").strip().lower()
    urgency = str(body.get("urgency") or "").strip().lower()
    consent = _truthy(body.get("consent"))
    notes = str(body.get("notes") or body.get("message") or "").strip()

    has_budget = budget_range not in {
        "", "none", "unknown", "not_sure", "no_budget",
    }
    pain_clear = biggest_pain in _PAIN_KEYS
    owner_present = role.lower() in _OWNER_ROLES

    result = qualify(
        pain_clear=pain_clear,
        owner_present=owner_present,
        data_available=crm,
        accepts_governance=consent_external,
        has_budget=has_budget,
        wants_safe_methods=True,
        proof_path_visible=link_value,
        retainer_path_visible=(urgency == "high" and has_budget),
        raw_request_text=" ".join([notes, crm_system, biggest_pain]),
        sector=sector,
    )

    blocked = bool(result.doctrine_violations) or result.decision == "reject"
    bucket = _risk_bucket(result.score, blocked)
    governance_decision = "blocked" if blocked else "allow"

    icp = icp_score(ICPDimensions(
        b2b_service_fit=70 if pain_clear else 30,
        data_maturity=70 if crm else 25,
        governance_posture=80 if consent_external else 20,
        budget_signal=70 if has_budget else 25,
        decision_velocity=75 if owner_present else 35,
    ))
    risk = client_risk_score(ClientRiskSignals(
        wants_scraping_or_spam="scraping" in result.doctrine_violations,
        wants_guaranteed_sales="guaranteed_sales" in result.doctrine_violations,
        unclear_pain=not pain_clear,
        no_owner=not owner_present,
        data_not_ready=not crm,
        budget_unknown=not has_budget,
    ))

    next_step = {
        "blocked": "request_cannot_proceed_as_described",
        "high": "book_diagnostic_review",
        "medium": "request_sample_proof_pack",
        "low": "educational_resources",
    }[bucket]

    # The sample Proof Pack is consent-gated and is NEVER auto-sent — the
    # response only returns a flag the founder acts on after review.
    proof_pack_available = consent and not blocked
    sample_proof_pack = {
        "available": proof_pack_available,
        "reason": (
            None if proof_pack_available
            else ("blocked" if blocked else "consent_required")
        ),
    }

    # Durable evidence record — the founder reviews every lead. Best-effort:
    # a disk hiccup must never 5xx the public form.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": str(body.get("phone") or "").strip(),
            "role": role,
            "linkedin": linkedin,
            "sector": sector,
            "team_size": team_size,
            "crm": crm,
            "crm_system": crm_system,
            "ai_usage": ai_usage,
            "biggest_pain": biggest_pain,
            "consent": consent,
            "consent_before_external_action": consent_external,
            "can_link_workflow_to_value": link_value,
            "budget_range": budget_range,
            "urgency": urgency,
            "notes": notes,
            "source": str(body.get("source") or "public_diagnostic"),
            "ref": str(body.get("ref") or ""),
            "fit_score": result.score,
            "icp_score": icp,
            "client_risk_score": risk,
            "risk_bucket": bucket,
            "decision": result.decision,
            "recommended_offer": result.recommended_offer,
            "reasons": list(result.reasons),
            "doctrine_violations": list(result.doctrine_violations),
            "governance_decision": governance_decision,
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("risk_score_lead_inbox_append_failed")

    # Analytics — fire-and-forget, never blocks the response.
    try:
        await capture_event(
            "risk_score_completed",
            distinct_id=email,
            properties={
                "company": company,
                "sector": sector,
                "bucket": bucket,
                "fit_score": result.score,
                "source": "dealix.diagnostic_funnel",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    log.info(
        "risk_score_completed email=%s company=%s bucket=%s score=%s lead_id=%s",
        email, company, bucket, result.score, lead_id,
    )

    return {
        "ok": True,
        "lead_id": lead_id,
        "fit_score": result.score,
        "bucket": bucket,
        "decision": result.decision,
        "reasons": list(result.reasons),
        "doctrine_violations": list(result.doctrine_violations),
        "recommended_offer": result.recommended_offer,
        "icp_score": icp,
        "client_risk_score": risk,
        "next_step": next_step,
        "sample_proof_pack": sample_proof_pack,
        "governance_decision": governance_decision,
        "disclaimer": _RISK_SCORE_DISCLAIMER,
    }
