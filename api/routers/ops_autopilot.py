"""Dealix Sales + Customer Ops Autopilot router.

Governance-first automation surface:
- Automates drafting, scoring, classification, and state updates.
- High-risk external actions are approval-gated (never auto-executed).
- Every meaningful step writes an evidence event.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query

from auto_client_acquisition.approval_center import ApprovalRequest, get_default_approval_store
from auto_client_acquisition.support_os import classify_message, draft_response

router = APIRouter(prefix="/api/v1", tags=["ops-autopilot"])


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_cold_linkedin_dm": True,
    "approval_required_for_external_actions": True,
    "traceable_evidence_required": True,
}

_LEAD_STAGES = (
    "new_lead",
    "qualified_A",
    "qualified_B",
    "nurture",
    "partner_candidate",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "sprint_candidate",
    "retainer_candidate",
    "closed_lost",
)

_APPROVAL_REQUIRED_TYPES = {
    "message_send",
    "scope_send",
    "invoice_send",
    "diagnostic_final",
    "case_study_publish",
    "security_claim",
    "agent_action",
    "discount_request",
}

_CLAIM_KEYWORDS = ("security", "compliance", "guarantee", "roi", "revenue", "legal", "privacy")

_SUPPORT_ESCALATE_INTENTS = {
    "privacy_pdpl",
    "refund",
    "payment",
    "angry_customer",
    "security_question",
    "refund_or_discount",
    "client_specific_diagnosis",
}


_LEADS: dict[str, dict[str, Any]] = {}
_OPPORTUNITIES: dict[str, dict[str, Any]] = {}
_BOOKINGS: dict[str, dict[str, Any]] = {}
_DIAGNOSTICS: dict[str, dict[str, Any]] = {}
_SUPPORT_TICKETS: dict[str, dict[str, Any]] = {}
_KNOWLEDGE_ARTICLES: dict[str, dict[str, Any]] = {}
_KNOWLEDGE_GAPS: list[dict[str, Any]] = []
_EVIDENCE_EVENTS: list[dict[str, Any]] = []
_INVOICES: dict[str, dict[str, Any]] = {}
_APPROVALS: dict[str, dict[str, Any]] = {}


def _seed_kb() -> None:
    if _KNOWLEDGE_ARTICLES:
        return
    seed_rows = [
        {
            "title": "Dealix Overview",
            "slug": "dealix-overview",
            "category": "overview",
            "content": "Dealix is a Saudi Revenue + Customer Ops Autopilot with approval-first governance.",
            "locale": "en",
            "visibility": "internal",
            "source": "founder_playbook",
            "approved": True,
            "version": 1,
            "risk_level": "low",
        },
        {
            "title": "نطاق التشخيص",
            "slug": "diagnostic-scope-ar",
            "category": "diagnostic_scope",
            "content": "التشخيص يحدد فجوات البيانات والموافقة والأولوية التجارية ولا يقدم وعود نتائج مالية.",
            "locale": "ar",
            "visibility": "internal",
            "source": "founder_playbook",
            "approved": True,
            "version": 1,
            "risk_level": "medium",
        },
        {
            "title": "Pricing Policy",
            "slug": "pricing-policy",
            "category": "pricing",
            "content": "Pricing ranges are indicative. Negotiation, large discounts, and refunds require founder approval.",
            "locale": "en",
            "visibility": "internal",
            "source": "pricing_policy",
            "approved": True,
            "version": 1,
            "risk_level": "medium",
        },
    ]
    for row in seed_rows:
        article_id = _new_id("kb")
        _KNOWLEDGE_ARTICLES[article_id] = {
            "id": article_id,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "last_reviewed_at": _now_iso(),
            "owner": "founder",
            **row,
        }


def _contains_high_risk_claim(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in _CLAIM_KEYWORDS)


def _log_evidence(
    *,
    event_type: str,
    entity_type: str,
    entity_id: str,
    summary: str,
    account_id: str | None = None,
    contact_id: str | None = None,
    source: str = "ops_autopilot",
    linked_asset: str | None = None,
    confidence: float = 0.85,
    approval_id: str | None = None,
    created_by: str = "system",
) -> dict[str, Any]:
    event = {
        "id": _new_id("ev"),
        "event_type": event_type,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "account_id": account_id,
        "contact_id": contact_id,
        "source": source,
        "summary": summary,
        "linked_asset": linked_asset,
        "confidence": confidence,
        "approval_id": approval_id,
        "created_by": created_by,
        "created_at": _now_iso(),
    }
    _EVIDENCE_EVENTS.append(event)
    return event


def _create_approval(
    *,
    approval_type: str,
    risk_level: str,
    entity_type: str,
    entity_id: str,
    proposed_action: str,
    draft: str,
    source: str,
    required_evidence: list[str],
    agent_rationale: str,
) -> dict[str, Any]:
    local_id = _new_id("apr")
    approval = {
        "id": local_id,
        "approval_id": local_id,
        "type": approval_type,
        "risk_level": risk_level,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "proposed_action": proposed_action,
        "draft": draft,
        "source": source,
        "required_evidence": required_evidence,
        "status": "pending",
        "agent_rationale": agent_rationale,
        "approved_by": None,
        "approved_at": None,
        "rejection_reason": "",
        "created_at": _now_iso(),
    }
    # Mirror into the canonical Approval Center store so existing
    # /api/v1/approvals endpoints and UI stay consistent.
    canonical = get_default_approval_store().create(
        ApprovalRequest.model_validate(
            {
                "object_type": entity_type,
                "object_id": entity_id,
                "action_type": approval_type,
                "action_mode": "approval_required",
                "channel": "internal",
                "summary_ar": proposed_action,
                "summary_en": proposed_action,
                "risk_level": risk_level,
                "proof_impact": ", ".join(required_evidence),
            }
        )
    )
    approval["id"] = canonical.approval_id
    approval["approval_id"] = canonical.approval_id
    _APPROVALS[approval["id"]] = approval
    _log_evidence(
        event_type="approval_requested",
        entity_type=entity_type,
        entity_id=entity_id,
        summary=f"Approval requested: {approval_type}",
        source="approval_center",
    )
    return approval


def _require_approval_for_action(
    *,
    action_type: str,
    draft_text: str,
    risk_level: str,
) -> bool:
    if action_type in _APPROVAL_REQUIRED_TYPES:
        return True
    if risk_level in {"high", "critical"}:
        return True
    return _contains_high_risk_claim(draft_text)


def _normalize_budget_value(raw: Any) -> float:
    if isinstance(raw, (int, float)):
        return float(raw)
    if raw is None:
        return 0.0
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    return float(digits) if digits else 0.0


def _lead_scoring_breakdown(payload: dict[str, Any]) -> dict[str, Any]:
    score = 0
    reasons: list[str] = []
    role = str(payload.get("role") or payload.get("title") or "").lower()
    company = str(payload.get("company") or "").strip()
    pain = str(payload.get("pain") or payload.get("message") or "").strip()
    country = str(payload.get("country") or payload.get("region") or "").lower()
    budget_value = _normalize_budget_value(
        payload.get("budget_sar") or payload.get("budget") or payload.get("budget_range")
    )
    urgency = str(payload.get("urgency") or "").lower()
    has_crm = bool(payload.get("has_crm") or payload.get("crm_in_use"))
    ai_usage = bool(payload.get("ai_usage") or payload.get("uses_ai"))
    referral = bool(payload.get("partner_referral") or payload.get("referral_potential"))
    vague = bool(payload.get("vague_curiosity"))

    if any(token in role for token in ("founder", "ceo", "coo", "cro", "head of ops")):
        score += 4
        reasons.append("+4 executive owner")
    if bool(payload.get("is_b2b", True)):
        score += 3
        reasons.append("+3 b2b fit")
    if has_crm:
        score += 3
        reasons.append("+3 crm maturity")
    if ai_usage:
        score += 3
        reasons.append("+3 ai readiness")
    if any(token in country for token in ("saudi", "ksa", "gcc", "uae", "qatar", "kuwait", "oman", "bahrain")):
        score += 2
        reasons.append("+2 regional fit")
    if "30" in urgency or "urgent" in urgency:
        score += 2
        reasons.append("+2 urgency")
    if budget_value >= 5000:
        score += 2
        reasons.append("+2 budget ready")
    if referral:
        score += 2
        reasons.append("+2 referral potential")
    if not company:
        score -= 4
        reasons.append("-4 no company")
    if any(token in role for token in ("student", "job seeker", "intern")):
        score -= 3
        reasons.append("-3 role mismatch")
    if vague:
        score -= 3
        reasons.append("-3 vague curiosity")
    if len(pain) < 10:
        score -= 2
        reasons.append("-2 unclear workflow pain")

    score = max(0, min(30, score))
    if score >= 15:
        stage = "qualified_A"
    elif score >= 10:
        stage = "qualified_B"
    elif score >= 6:
        stage = "nurture"
    else:
        stage = "new_lead"
    return {"score": score, "stage": stage, "reasons": reasons}


def _risk_score(payload: dict[str, Any]) -> dict[str, Any]:
    score = 10
    reasons: list[str] = []
    if not str(payload.get("company") or "").strip():
        score += 20
        reasons.append("no_company_context")
    if not str(payload.get("pain") or payload.get("message") or "").strip():
        score += 15
        reasons.append("no_workflow_pain")
    if _contains_high_risk_claim(str(payload.get("request") or payload.get("message") or "")):
        score += 20
        reasons.append("high_risk_claim_terms_detected")
    if bool(payload.get("wants_cold_outreach")):
        score += 25
        reasons.append("cold_outreach_request_blocked")
    if bool(payload.get("wants_guarantee")):
        score += 25
        reasons.append("guarantee_request_blocked")
    if bool(payload.get("consent", True)) is False:
        score += 20
        reasons.append("consent_missing")
    score = max(0, min(100, score))
    level = "low" if score < 35 else "medium" if score < 70 else "high"
    return {"score": score, "level": level, "reasons": reasons}


def _search_kb(query: str, locale: str = "ar") -> list[dict[str, Any]]:
    _seed_kb()
    q = query.lower().strip()
    rows = []
    for article in _KNOWLEDGE_ARTICLES.values():
        if not article.get("approved"):
            continue
        haystack = f"{article['title']} {article['content']} {article['category']}".lower()
        if q and q in haystack:
            rows.append(article)
    if not rows and q:
        # fallback: same locale first, then any approved article
        locale_rows = [a for a in _KNOWLEDGE_ARTICLES.values() if a["approved"] and a["locale"] == locale]
        rows = locale_rows or [a for a in _KNOWLEDGE_ARTICLES.values() if a["approved"]]
    return rows[:5]


@router.get("/ops-autopilot/status")
async def ops_autopilot_status() -> dict[str, Any]:
    return {
        "service": "ops_autopilot",
        "status": "operational",
        "loop": [
            "marketing",
            "sales",
            "payment",
            "delivery",
            "support",
            "upsell",
            "learning",
        ],
        "hard_gates": _HARD_GATES,
    }


@router.post("/public/risk-score")
async def public_risk_score(payload: dict[str, Any]) -> dict[str, Any]:
    risk = _risk_score(payload)
    return {
        "risk_score": risk["score"],
        "risk_level": risk["level"],
        "reasons": risk["reasons"],
        "recommended_next": "continue_to_lead_capture" if risk["level"] != "high" else "requires_founder_review",
        "hard_gates": _HARD_GATES,
    }


@router.post("/public/leads")
async def public_lead_capture(payload: dict[str, Any]) -> dict[str, Any]:
    required = ("name", "email", "company")
    missing = [key for key in required if not str(payload.get(key) or "").strip()]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing_required_fields: {missing}")

    lead_id = _new_id("lead")
    score_info = _lead_scoring_breakdown(payload)
    risk = _risk_score(payload)
    lead = {
        "id": lead_id,
        "name": str(payload.get("name")),
        "email": str(payload.get("email")),
        "phone": str(payload.get("phone") or ""),
        "company": str(payload.get("company")),
        "role": str(payload.get("role") or ""),
        "industry": str(payload.get("industry") or payload.get("sector") or ""),
        "country": str(payload.get("country") or "Saudi Arabia"),
        "source": str(payload.get("source") or "public_funnel"),
        "pain": str(payload.get("pain") or payload.get("message") or ""),
        "crm_status": "created",
        "ai_usage": bool(payload.get("ai_usage") or payload.get("uses_ai")),
        "budget_range": str(payload.get("budget_range") or payload.get("budget") or ""),
        "urgency": str(payload.get("urgency") or "normal"),
        "consent_status": "granted" if bool(payload.get("consent", True)) else "missing",
        "lead_score": score_info["score"],
        "risk_score": risk["score"],
        "stage": score_info["stage"],
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _LEADS[lead_id] = lead

    evidence = _log_evidence(
        event_type="lead_captured",
        entity_type="lead",
        entity_id=lead_id,
        summary=f"Lead captured from public funnel ({lead['stage']})",
        source="public_lead_capture",
    )

    proof_pack_allowed = lead["consent_status"] == "granted"
    sample_proof_pack = {
        "enabled": proof_pack_allowed,
        "note": "Sample proof pack can be shared after consent only.",
    }

    return {
        "lead": lead,
        "score_reasons": score_info["reasons"],
        "risk_level": risk["level"],
        "sample_proof_pack": sample_proof_pack,
        "evidence_event_id": evidence["id"],
        "next_action": "book_diagnostic_review" if lead["stage"] in {"qualified_A", "qualified_B"} else "nurture_follow_up",
        "hard_gates": _HARD_GATES,
    }


@router.get("/public/proof-pack/sample")
async def public_proof_pack_sample() -> dict[str, Any]:
    return {
        "pack_id": "sample_proof_pack_v1",
        "sections": [
            "problem_map",
            "signal_summary",
            "evidence_chain",
            "quick_win_plan",
            "governance_warnings",
        ],
        "disclaimer_ar": "هذه عينة إرشادية وليست تشخيصاً نهائياً للعميل.",
        "disclaimer_en": "This is a guided sample and not a final customer-specific diagnosis.",
        "requires_consent": True,
        "hard_gates": _HARD_GATES,
    }


@router.post("/public/booking-request")
async def public_booking_request(payload: dict[str, Any]) -> dict[str, Any]:
    lead_id = str(payload.get("lead_id") or "")
    if lead_id and lead_id not in _LEADS:
        raise HTTPException(status_code=404, detail="lead_not_found")
    booking_id = _new_id("book")
    booking = {
        "id": booking_id,
        "lead_id": lead_id or None,
        "status": "requested",
        "meeting_date": payload.get("meeting_date"),
        "channel": payload.get("channel", "meet"),
        "notes": payload.get("notes", ""),
        "brief": None,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _BOOKINGS[booking_id] = booking
    _log_evidence(
        event_type="meeting_booked",
        entity_type="booking",
        entity_id=booking_id,
        summary="Public booking request submitted",
        source="public_booking_request",
    )
    return {"booking": booking, "hard_gates": _HARD_GATES}


@router.post("/public/support")
async def public_support(payload: dict[str, Any]) -> dict[str, Any]:
    return await support_create_ticket(payload)


@router.get("/public/services")
async def public_services() -> dict[str, Any]:
    return {
        "services": [
            {
                "id": "diagnostic_499",
                "name_ar": "Sprint تشخيص 499 SAR",
                "name_en": "499 SAR Diagnostic Sprint",
                "pricing_sar": 499,
                "delivery_window_days": 7,
            },
            {
                "id": "data_pack_1500",
                "name_ar": "حزمة بيانات 1,500 SAR",
                "name_en": "1,500 SAR Data Pack",
                "pricing_sar": 1500,
                "delivery_window_days": 10,
            },
            {
                "id": "managed_ops_2999",
                "name_ar": "Managed Ops شهري",
                "name_en": "Managed Ops Monthly",
                "pricing_sar_range": [2999, 4999],
                "delivery_window_days": 30,
            },
        ],
        "hard_gates": _HARD_GATES,
    }


@router.get("/leads")
async def list_leads() -> dict[str, Any]:
    rows = sorted(_LEADS.values(), key=lambda item: item["created_at"], reverse=True)
    return {"count": len(rows), "items": rows, "hard_gates": _HARD_GATES}


@router.get("/leads/{lead_id}")
async def get_lead(lead_id: str) -> dict[str, Any]:
    lead = _LEADS.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    return {"lead": lead, "hard_gates": _HARD_GATES}


@router.post("/leads/{lead_id}/score")
async def rescore_lead(lead_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    lead = _LEADS.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    merged = {**lead, **payload}
    score_info = _lead_scoring_breakdown(merged)
    lead["lead_score"] = score_info["score"]
    lead["stage"] = score_info["stage"]
    lead["updated_at"] = _now_iso()
    _log_evidence(
        event_type="lead_scored",
        entity_type="lead",
        entity_id=lead_id,
        summary=f"Lead rescored to {lead['lead_score']}",
        source="lead_score_engine",
    )
    return {"lead": lead, "reasons": score_info["reasons"], "hard_gates": _HARD_GATES}


@router.post("/leads/{lead_id}/draft-message")
async def draft_lead_message(lead_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    lead = _LEADS.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")

    tone = str(payload.get("tone") or "professional")
    draft = (
        f"Hi {lead['name']}, based on your workflow in {lead['company']} we prepared a diagnostic path. "
        f"We can share a governed sample proof pack and schedule a review. Tone={tone}."
    )
    risk_level = "high" if _contains_high_risk_claim(draft) else "medium" if lead["lead_score"] < 10 else "low"
    approval = None
    if _require_approval_for_action(action_type="message_send", draft_text=draft, risk_level=risk_level):
        approval = _create_approval(
            approval_type="message_send",
            risk_level=risk_level,
            entity_type="lead",
            entity_id=lead_id,
            proposed_action="send_first_outreach_message",
            draft=draft,
            source="sales_autopilot",
            required_evidence=["lead_score", "consent_status"],
            agent_rationale="First external message is always founder-approved.",
        )
    _log_evidence(
        event_type="message_prepared",
        entity_type="lead",
        entity_id=lead_id,
        summary="Outreach draft prepared",
        source="sales_autopilot",
        approval_id=approval["id"] if approval else None,
    )
    return {
        "lead_id": lead_id,
        "draft": draft,
        "risk_level": risk_level,
        "requires_approval": approval is not None,
        "approval": approval,
        "hard_gates": _HARD_GATES,
    }


@router.post("/leads/{lead_id}/classify-reply")
async def classify_lead_reply(lead_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    if lead_id not in _LEADS:
        raise HTTPException(status_code=404, detail="lead_not_found")
    text = str(payload.get("reply") or "")
    lowered = text.lower()
    if any(token in lowered for token in ("book", "meeting", "call", "schedule", "demo")):
        label = "meeting_intent"
        next_action = "create_booking"
    elif any(token in lowered for token in ("price", "pricing", "budget", "cost")):
        label = "pricing_question"
        next_action = "send_pricing_range"
    elif any(token in lowered for token in ("not interested", "later", "stop")):
        label = "negative_or_nurture"
        next_action = "move_to_nurture"
    else:
        label = "neutral"
        next_action = "follow_up_reminder"
    _log_evidence(
        event_type="reply_received",
        entity_type="lead",
        entity_id=lead_id,
        summary=f"Lead reply classified as {label}",
        source="reply_classifier",
    )
    return {"classification": label, "next_action": next_action, "hard_gates": _HARD_GATES}


@router.post("/leads/{lead_id}/convert-opportunity")
async def convert_opportunity(lead_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    lead = _LEADS.get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    opp_id = _new_id("opp")
    opportunity = {
        "id": opp_id,
        "lead_id": lead_id,
        "account_id": payload.get("account_id"),
        "offer_id": payload.get("offer_id", "diagnostic_499"),
        "stage": "meeting_booked" if lead["stage"] in {"qualified_A", "qualified_B"} else "new_lead",
        "amount_sar": float(payload.get("amount_sar") or 0.0),
        "probability": float(payload.get("probability") or 0.35),
        "expected_close_date": payload.get("expected_close_date"),
        "next_action": payload.get("next_action", "prepare_meeting_brief"),
        "evidence_level": payload.get("evidence_level", "L2"),
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _OPPORTUNITIES[opp_id] = opportunity
    _log_evidence(
        event_type="opportunity_created",
        entity_type="opportunity",
        entity_id=opp_id,
        summary="Lead converted to opportunity",
        source="sales_autopilot",
    )
    return {"opportunity": opportunity, "hard_gates": _HARD_GATES}


@router.get("/sales/pipeline")
async def sales_pipeline() -> dict[str, Any]:
    stage_counts = {stage: 0 for stage in _LEAD_STAGES}
    for lead in _LEADS.values():
        stage = lead.get("stage", "new_lead")
        if stage in stage_counts:
            stage_counts[stage] += 1
    for opp in _OPPORTUNITIES.values():
        stage = str(opp.get("stage") or "")
        if stage in stage_counts:
            stage_counts[stage] += 1
    return {
        "stages": [{"stage": stage, "count": count} for stage, count in stage_counts.items()],
        "lead_count": len(_LEADS),
        "opportunity_count": len(_OPPORTUNITIES),
        "hard_gates": _HARD_GATES,
    }


@router.post("/opportunities/{opportunity_id}/next-action")
async def set_opportunity_next_action(opportunity_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    opp = _OPPORTUNITIES.get(opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    next_action = str(payload.get("next_action") or "").strip()
    if not next_action:
        raise HTTPException(status_code=422, detail="next_action_required")
    opp["next_action"] = next_action
    opp["updated_at"] = _now_iso()
    _log_evidence(
        event_type="next_action_created",
        entity_type="opportunity",
        entity_id=opportunity_id,
        summary=f"Next action set: {next_action}",
        source="sales_autopilot",
    )
    return {"opportunity": opp, "hard_gates": _HARD_GATES}


@router.post("/bookings")
async def create_booking(payload: dict[str, Any]) -> dict[str, Any]:
    lead_id = payload.get("lead_id")
    if lead_id and lead_id not in _LEADS:
        raise HTTPException(status_code=404, detail="lead_not_found")
    booking_id = _new_id("book")
    row = {
        "id": booking_id,
        "lead_id": lead_id,
        "opportunity_id": payload.get("opportunity_id"),
        "status": "booked",
        "meeting_date": payload.get("meeting_date"),
        "channel": payload.get("channel", "meet"),
        "brief": None,
        "outcome": None,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _BOOKINGS[booking_id] = row
    _log_evidence(
        event_type="meeting_booked",
        entity_type="booking",
        entity_id=booking_id,
        summary="Meeting booked",
        source="booking_automation",
    )
    return {"booking": row, "hard_gates": _HARD_GATES}


@router.post("/bookings/{booking_id}/prepare-brief")
async def prepare_booking_brief(booking_id: str) -> dict[str, Any]:
    booking = _BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking_not_found")
    lead = _LEADS.get(str(booking.get("lead_id"))) if booking.get("lead_id") else {}
    brief = {
        "company": lead.get("company"),
        "pain_summary": lead.get("pain"),
        "lead_score": lead.get("lead_score"),
        "top_questions": [
            "What workflow bottleneck blocks revenue right now?",
            "What proof event can be created within 7 days?",
            "What approvals are needed for external actions?",
        ],
    }
    booking["brief"] = brief
    booking["updated_at"] = _now_iso()
    _log_evidence(
        event_type="meeting_brief_generated",
        entity_type="booking",
        entity_id=booking_id,
        summary="Meeting brief generated",
        source="meeting_brief_agent",
    )
    return {"booking": booking, "hard_gates": _HARD_GATES}


@router.post("/bookings/{booking_id}/mark-done")
async def mark_booking_done(booking_id: str) -> dict[str, Any]:
    booking = _BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking_not_found")
    booking["status"] = "done"
    booking["updated_at"] = _now_iso()
    _log_evidence(
        event_type="meeting_done",
        entity_type="booking",
        entity_id=booking_id,
        summary="Meeting marked as done",
        source="booking_automation",
    )
    return {"booking": booking, "hard_gates": _HARD_GATES}


@router.post("/bookings/{booking_id}/outcome")
async def booking_outcome(booking_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    booking = _BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking_not_found")
    booking["outcome"] = {
        "scope_requested": bool(payload.get("scope_requested", True)),
        "notes": payload.get("notes", ""),
    }
    booking["updated_at"] = _now_iso()
    _log_evidence(
        event_type="scope_requested",
        entity_type="booking",
        entity_id=booking_id,
        summary="Meeting outcome recorded",
        source="booking_automation",
    )
    return {"booking": booking, "hard_gates": _HARD_GATES}


@router.post("/diagnostics")
async def create_diagnostic(payload: dict[str, Any]) -> dict[str, Any]:
    diag_id = _new_id("diag")
    row = {
        "id": diag_id,
        "lead_id": payload.get("lead_id"),
        "opportunity_id": payload.get("opportunity_id"),
        "status": "onboarding_pending",
        "onboarding": [],
        "analysis": None,
        "proof_pack": None,
        "upsell": None,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _DIAGNOSTICS[diag_id] = row
    _log_evidence(
        event_type="diagnostic_started",
        entity_type="diagnostic",
        entity_id=diag_id,
        summary="Diagnostic workflow created",
        source="diagnostic_automation",
    )
    return {"diagnostic": row, "hard_gates": _HARD_GATES}


@router.get("/diagnostics/{diagnostic_id}")
async def get_diagnostic(diagnostic_id: str) -> dict[str, Any]:
    row = _DIAGNOSTICS.get(diagnostic_id)
    if not row:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    return {"diagnostic": row, "hard_gates": _HARD_GATES}


@router.post("/diagnostics/{diagnostic_id}/onboarding")
async def diagnostic_onboarding(diagnostic_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _DIAGNOSTICS.get(diagnostic_id)
    if not row:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    checklist = payload.get("checklist") or [
        "access_crm",
        "access_support_inbox",
        "define_primary_offer",
        "confirm_governance_rules",
    ]
    row["onboarding"] = checklist
    row["status"] = "onboarding_in_progress"
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="onboarding_started",
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        summary="Onboarding checklist prepared",
        source="onboarding_agent",
    )
    return {"diagnostic": row, "hard_gates": _HARD_GATES}


@router.post("/diagnostics/{diagnostic_id}/analyze")
async def diagnostic_analyze(diagnostic_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _DIAGNOSTICS.get(diagnostic_id)
    if not row:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    row["analysis"] = {
        "source_quality": payload.get("source_quality", "medium"),
        "approval_gaps": payload.get("approval_gaps", ["invoice_send", "security_claim"]),
        "primary_bottleneck": payload.get("primary_bottleneck", "lead_to_scope_latency"),
        "generated_at": _now_iso(),
    }
    row["status"] = "analysis_ready"
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="diagnostic_analyzed",
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        summary="Diagnostic analysis generated",
        source="diagnostic_agent",
    )
    return {"diagnostic": row, "hard_gates": _HARD_GATES}


@router.post("/diagnostics/{diagnostic_id}/generate-proof-pack")
async def diagnostic_generate_proof_pack(diagnostic_id: str) -> dict[str, Any]:
    row = _DIAGNOSTICS.get(diagnostic_id)
    if not row:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    pack = {
        "pack_id": _new_id("pack"),
        "sections": [
            "executive_summary",
            "risk_and_readiness",
            "signal_evidence",
            "draft_action_plan",
            "approval_checklist",
        ],
        "status": "draft",
        "requires_founder_review": True,
    }
    row["proof_pack"] = pack
    row["status"] = "proof_pack_draft_ready"
    row["updated_at"] = _now_iso()
    approval = _create_approval(
        approval_type="diagnostic_final",
        risk_level="high",
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        proposed_action="send_final_diagnostic_to_customer",
        draft="Diagnostic final report draft prepared.",
        source="proof_pack_agent",
        required_evidence=["diagnostic_analyzed", "proof_pack_draft"],
        agent_rationale="Final diagnostic output is always founder-approved.",
    )
    _log_evidence(
        event_type="proof_pack_sent",
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        summary="Proof pack draft generated",
        source="proof_pack_agent",
        approval_id=approval["id"],
    )
    return {"diagnostic": row, "approval": approval, "hard_gates": _HARD_GATES}


@router.post("/diagnostics/{diagnostic_id}/recommend-upsell")
async def diagnostic_recommend_upsell(diagnostic_id: str) -> dict[str, Any]:
    row = _DIAGNOSTICS.get(diagnostic_id)
    if not row:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    offer = "managed_ops_2999" if row.get("analysis") else "data_pack_1500"
    recommendation = {
        "offer_id": offer,
        "reason": "Proof pack indicates repeatable wins and pending automation queue.",
        "confidence": 0.78,
    }
    row["upsell"] = recommendation
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="upsell_proposed",
        entity_type="diagnostic",
        entity_id=diagnostic_id,
        summary=f"Upsell recommended: {offer}",
        source="upsell_recommendation_agent",
    )
    return {"diagnostic": row, "hard_gates": _HARD_GATES}


@router.post("/support/tickets")
async def support_create_ticket(payload: dict[str, Any]) -> dict[str, Any]:
    message = str(payload.get("message") or payload.get("question") or "").strip()
    if not message:
        raise HTTPException(status_code=422, detail="message_required")
    ticket_id = _new_id("tkt")
    classification = classify_message(message)
    kb_hits = _search_kb(message, str(payload.get("locale") or "ar"))
    kb_sources = [hit["id"] for hit in kb_hits]
    draft = draft_response(message=message, classification=classification)
    risk_level = "high" if classification.category in _SUPPORT_ESCALATE_INTENTS else "medium" if not kb_hits else "low"
    escalation_required = risk_level in {"high", "medium"} and (
        draft.escalation.should_escalate or not kb_hits
    )
    status = "escalated" if escalation_required else "auto_draft_ready"
    row = {
        "id": ticket_id,
        "account_id": payload.get("account_id"),
        "contact_id": payload.get("contact_id"),
        "channel": payload.get("channel", "web"),
        "subject": payload.get("subject", "support_request"),
        "message": message,
        "intent": classification.category,
        "priority": "p0" if risk_level == "high" else "p1" if risk_level == "medium" else "p3",
        "risk_level": risk_level,
        "status": status,
        "assigned_to": payload.get("assigned_to"),
        "ai_summary": f"Intent={classification.category} confidence={classification.confidence}",
        "suggested_response": draft.text_ar if str(payload.get("locale") or "ar") == "ar" else draft.text_en,
        "source_article_ids": kb_sources,
        "escalation_required": escalation_required,
        "sla": "60m" if risk_level == "high" else "24h" if risk_level == "medium" else "48h",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _SUPPORT_TICKETS[ticket_id] = row

    approval = None
    if escalation_required:
        approval = _create_approval(
            approval_type="agent_action",
            risk_level=risk_level,
            entity_type="support_ticket",
            entity_id=ticket_id,
            proposed_action="review_sensitive_support_response",
            draft=row["suggested_response"],
            source="support_autopilot",
            required_evidence=["kb_source" if kb_hits else "missing_kb_source"],
            agent_rationale="Sensitive or low-evidence support answer requires human review.",
        )

    _log_evidence(
        event_type="support_ticket_created",
        entity_type="support_ticket",
        entity_id=ticket_id,
        summary=f"Support ticket created ({classification.category})",
        source="support_autopilot",
        approval_id=approval["id"] if approval else None,
    )

    return {"ticket": row, "approval": approval, "hard_gates": _HARD_GATES}


@router.get("/support/tickets")
async def support_list_tickets(
    status: str | None = Query(default=None),
    intent: str | None = Query(default=None),
) -> dict[str, Any]:
    rows = list(_SUPPORT_TICKETS.values())
    if status:
        rows = [row for row in rows if row.get("status") == status]
    if intent:
        rows = [row for row in rows if row.get("intent") == intent]
    rows.sort(key=lambda item: item["created_at"], reverse=True)
    return {"count": len(rows), "items": rows, "hard_gates": _HARD_GATES}


@router.get("/support/tickets/{ticket_id}")
async def support_get_ticket(ticket_id: str) -> dict[str, Any]:
    row = _SUPPORT_TICKETS.get(ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    return {"ticket": row, "hard_gates": _HARD_GATES}


@router.post("/support/tickets/{ticket_id}/classify")
async def support_classify(ticket_id: str) -> dict[str, Any]:
    row = _SUPPORT_TICKETS.get(ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    classification = classify_message(str(row["message"]))
    row["intent"] = classification.category
    row["updated_at"] = _now_iso()
    return {"ticket": row, "classification": classification.__dict__, "hard_gates": _HARD_GATES}


@router.post("/support/tickets/{ticket_id}/draft-response")
async def support_draft(ticket_id: str) -> dict[str, Any]:
    row = _SUPPORT_TICKETS.get(ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    classification = classify_message(str(row["message"]))
    draft = draft_response(message=str(row["message"]), classification=classification)
    kb_hits = _search_kb(str(row["message"]), "ar")
    auto_answer_allowed = (
        row["risk_level"] == "low"
        and bool(kb_hits)
        and not draft.escalation.should_escalate
    )
    row["suggested_response"] = draft.text_ar
    row["status"] = "auto_answer_ready" if auto_answer_allowed else "awaiting_approval"
    row["source_article_ids"] = [hit["id"] for hit in kb_hits]
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="message_prepared",
        entity_type="support_ticket",
        entity_id=ticket_id,
        summary="Support response draft prepared",
        source="support_autopilot",
    )
    return {
        "ticket": row,
        "auto_answer_allowed": auto_answer_allowed,
        "sources": row["source_article_ids"],
        "hard_gates": _HARD_GATES,
    }


@router.post("/support/tickets/{ticket_id}/escalate")
async def support_escalate(ticket_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _SUPPORT_TICKETS.get(ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    reason = str(payload.get("reason") or "manual_escalation")
    row["status"] = "escalated"
    row["escalation_required"] = True
    row["updated_at"] = _now_iso()
    approval = _create_approval(
        approval_type="agent_action",
        risk_level=row["risk_level"],
        entity_type="support_ticket",
        entity_id=ticket_id,
        proposed_action="send_sensitive_support_reply",
        draft=row.get("suggested_response") or "",
        source="support_console",
        required_evidence=["support_ticket_context", "kb_sources"],
        agent_rationale=reason,
    )
    return {"ticket": row, "approval": approval, "hard_gates": _HARD_GATES}


@router.post("/support/tickets/{ticket_id}/resolve")
async def support_resolve(ticket_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _SUPPORT_TICKETS.get(ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    row["status"] = "resolved"
    row["resolution_note"] = payload.get("resolution_note", "resolved")
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="support_resolved",
        entity_type="support_ticket",
        entity_id=ticket_id,
        summary="Support ticket resolved",
        source="support_console",
    )
    return {"ticket": row, "hard_gates": _HARD_GATES}


@router.post("/knowledge/articles")
async def knowledge_create_article(payload: dict[str, Any]) -> dict[str, Any]:
    required = ("title", "category", "content")
    missing = [key for key in required if not str(payload.get(key) or "").strip()]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing_required_fields: {missing}")
    article_id = _new_id("kb")
    slug = str(payload.get("slug") or str(payload["title"]).lower().replace(" ", "-"))
    row = {
        "id": article_id,
        "title": payload["title"],
        "slug": slug,
        "category": payload["category"],
        "content": payload["content"],
        "locale": payload.get("locale", "ar"),
        "visibility": payload.get("visibility", "internal"),
        "source": payload.get("source", "manual"),
        "approved": bool(payload.get("approved", False)),
        "version": int(payload.get("version", 1)),
        "risk_level": payload.get("risk_level", "low"),
        "owner": payload.get("owner", "founder"),
        "last_reviewed_at": payload.get("last_reviewed_at", _now_iso()),
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _KNOWLEDGE_ARTICLES[article_id] = row
    return {"article": row, "hard_gates": _HARD_GATES}


@router.get("/knowledge/search")
async def knowledge_search(q: str = Query(min_length=2), locale: str = "ar") -> dict[str, Any]:
    hits = _search_kb(q, locale)
    return {
        "count": len(hits),
        "items": [
            {
                "id": item["id"],
                "title": item["title"],
                "category": item["category"],
                "locale": item["locale"],
                "approved": item["approved"],
                "snippet": str(item["content"])[:180],
            }
            for item in hits
        ],
        "hard_gates": _HARD_GATES,
    }


@router.post("/knowledge/suggest-answer")
async def knowledge_suggest_answer(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question") or "").strip()
    if not question:
        raise HTTPException(status_code=422, detail="question_required")
    locale = str(payload.get("locale") or "ar")
    hits = _search_kb(question, locale)
    if not hits:
        return {
            "found": False,
            "answer": "أحتاج أصعّد هذا للفريق." if locale == "ar" else "I need to escalate this to the team.",
            "sources": [],
            "requires_escalation": True,
            "hard_gates": _HARD_GATES,
        }
    first = hits[0]
    answer = str(first["content"])[:280]
    return {
        "found": True,
        "answer": answer,
        "sources": [first["id"]],
        "requires_escalation": bool(first.get("risk_level") in {"high", "critical"}),
        "hard_gates": _HARD_GATES,
    }


@router.post("/knowledge/gap-detect")
async def knowledge_gap_detect(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question") or "").strip()
    if not question:
        raise HTTPException(status_code=422, detail="question_required")
    hits = _search_kb(question, str(payload.get("locale") or "ar"))
    gap = {
        "id": _new_id("gap"),
        "question": question,
        "detected_at": _now_iso(),
        "has_existing_answer": bool(hits),
        "suggested_article_title": payload.get("suggested_article_title") or f"Knowledge gap: {question[:64]}",
    }
    _KNOWLEDGE_GAPS.append(gap)
    return {"gap": gap, "hard_gates": _HARD_GATES}


@router.post("/evidence/events")
async def evidence_create_event(payload: dict[str, Any]) -> dict[str, Any]:
    required = ("event_type", "entity_type", "entity_id", "summary")
    missing = [key for key in required if not str(payload.get(key) or "").strip()]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing_required_fields: {missing}")
    event = _log_evidence(
        event_type=str(payload["event_type"]),
        entity_type=str(payload["entity_type"]),
        entity_id=str(payload["entity_id"]),
        summary=str(payload["summary"]),
        account_id=payload.get("account_id"),
        contact_id=payload.get("contact_id"),
        source=str(payload.get("source") or "manual"),
        linked_asset=payload.get("linked_asset"),
        confidence=float(payload.get("confidence") or 0.8),
        approval_id=payload.get("approval_id"),
        created_by=str(payload.get("created_by") or "manual"),
    )
    return {"event": event, "hard_gates": _HARD_GATES}


@router.get("/evidence/events")
async def evidence_list_events(
    event_type: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
) -> dict[str, Any]:
    rows = list(_EVIDENCE_EVENTS)
    if event_type:
        rows = [row for row in rows if row.get("event_type") == event_type]
    if entity_type:
        rows = [row for row in rows if row.get("entity_type") == entity_type]
    if entity_id:
        rows = [row for row in rows if row.get("entity_id") == entity_id]
    rows.sort(key=lambda item: item["created_at"], reverse=True)
    return {"count": len(rows), "items": rows, "hard_gates": _HARD_GATES}


@router.get("/evidence/accounts/{account_id}")
async def evidence_account_events(account_id: str) -> dict[str, Any]:
    rows = [row for row in _EVIDENCE_EVENTS if row.get("account_id") == account_id]
    return {"count": len(rows), "items": rows, "hard_gates": _HARD_GATES}


@router.get("/evidence/opportunities/{opportunity_id}")
async def evidence_opportunity_events(opportunity_id: str) -> dict[str, Any]:
    rows = [
        row
        for row in _EVIDENCE_EVENTS
        if row.get("entity_type") == "opportunity" and row.get("entity_id") == opportunity_id
    ]
    return {"count": len(rows), "items": rows, "hard_gates": _HARD_GATES}


def _invoice_amount_for_tier(tier: str) -> int:
    if tier == "diagnostic_499":
        return 499
    if tier == "data_pack_1500":
        return 1500
    if tier == "managed_ops_2999":
        return 2999
    return 499


@router.post("/invoices/draft")
async def invoice_draft(payload: dict[str, Any]) -> dict[str, Any]:
    email = str(payload.get("customer_email") or "").strip()
    if "@" not in email:
        raise HTTPException(status_code=422, detail="valid_customer_email_required")
    tier = str(payload.get("tier_id") or "diagnostic_499")
    invoice_id = _new_id("inv")
    row = {
        "id": invoice_id,
        "tier_id": tier,
        "customer_email": email,
        "customer_handle": payload.get("customer_handle", ""),
        "amount_sar": _invoice_amount_for_tier(tier),
        "description": payload.get("description") or "Dealix governed invoice draft",
        "status": "draft",
        "requires_approval": True,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _INVOICES[invoice_id] = row
    approval = _create_approval(
        approval_type="invoice_send",
        risk_level="high",
        entity_type="invoice",
        entity_id=invoice_id,
        proposed_action="send_invoice_to_customer",
        draft=f"Invoice draft {invoice_id} for {email}",
        source="billing_autopilot",
        required_evidence=["scope_draft", "pricing_tier"],
        agent_rationale="Final invoice send is high-impact and approval-gated.",
    )
    _log_evidence(
        event_type="invoice_sent",
        entity_type="invoice",
        entity_id=invoice_id,
        summary="Invoice draft prepared",
        source="billing_autopilot",
        approval_id=approval["id"],
    )
    return {"invoice": row, "approval": approval, "hard_gates": _HARD_GATES}


@router.post("/invoices/{invoice_id}/approve-send")
async def invoice_approve_send(invoice_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _INVOICES.get(invoice_id)
    if not row:
        raise HTTPException(status_code=404, detail="invoice_not_found")
    approved_by = str(payload.get("approved_by") or "founder")
    row["status"] = "approved_to_send"
    row["approved_by"] = approved_by
    row["approved_at"] = _now_iso()
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="invoice_approved",
        entity_type="invoice",
        entity_id=invoice_id,
        summary=f"Invoice approved by {approved_by}",
        source="billing_autopilot",
    )
    return {"invoice": row, "hard_gates": _HARD_GATES}


@router.post("/invoices/{invoice_id}/mark-paid")
async def invoice_mark_paid(invoice_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    row = _INVOICES.get(invoice_id)
    if not row:
        raise HTTPException(status_code=404, detail="invoice_not_found")
    payment_ref = str(payload.get("payment_ref") or _new_id("pay"))
    row["status"] = "paid"
    row["payment_ref"] = payment_ref
    row["paid_at"] = _now_iso()
    row["updated_at"] = _now_iso()
    _log_evidence(
        event_type="invoice_paid",
        entity_type="invoice",
        entity_id=invoice_id,
        summary=f"Invoice paid ({payment_ref})",
        source="billing_autopilot",
    )
    return {"invoice": row, "hard_gates": _HARD_GATES}


@router.get("/billing/overview")
async def billing_overview() -> dict[str, Any]:
    invoices = list(_INVOICES.values())
    paid = [row for row in invoices if row.get("status") == "paid"]
    pending = [row for row in invoices if row.get("status") != "paid"]
    return {
        "invoice_count": len(invoices),
        "paid_count": len(paid),
        "pending_count": len(pending),
        "paid_total_sar": sum(float(row.get("amount_sar") or 0) for row in paid),
        "hard_gates": _HARD_GATES,
    }


@router.get("/reports/founder-command-center")
async def founder_command_center_report() -> dict[str, Any]:
    approvals_pending = len([row for row in _APPROVALS.values() if row["status"] == "pending"])
    support_open = len([row for row in _SUPPORT_TICKETS.values() if row["status"] != "resolved"])
    support_auto_resolved = len([row for row in _SUPPORT_TICKETS.values() if row["status"] == "auto_answer_ready"])
    support_escalated = len([row for row in _SUPPORT_TICKETS.values() if row["status"] == "escalated"])
    proof_pack_delivered = len([row for row in _DIAGNOSTICS.values() if row.get("proof_pack") is not None])
    return {
        "top_actions_today": [
            "Review pending high-risk approvals",
            "Advance qualified_A leads to meeting briefs",
            "Close support escalations with missing KB coverage",
        ],
        "metrics": {
            "new_leads_today": len(_LEADS),
            "qualified_A": len([row for row in _LEADS.values() if row.get("stage") == "qualified_A"]),
            "proof_pack_requests": proof_pack_delivered,
            "meetings_booked": len(_BOOKINGS),
            "scopes_requested": len(
                [row for row in _BOOKINGS.values() if bool((row.get("outcome") or {}).get("scope_requested"))]
            ),
            "invoices_sent": len(_INVOICES),
            "invoices_paid": len([row for row in _INVOICES.values() if row.get("status") == "paid"]),
            "support_tickets_open": support_open,
            "tickets_auto_resolved": support_auto_resolved,
            "tickets_escalated": support_escalated,
            "proof_packs_delivered": proof_pack_delivered,
            "upsell_candidates": len([row for row in _DIAGNOSTICS.values() if row.get("upsell")]),
            "blocked_approvals": approvals_pending,
            "unsupported_claims_caught": len(
                [row for row in _APPROVALS.values() if "security" in row.get("proposed_action", "")]
            ),
            "no_build_warnings": 0,
        },
        "hard_gates": _HARD_GATES,
    }

