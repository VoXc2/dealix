"""Governed Revenue Ops Diagnostic funnel engine.

Deterministic internal automation for one offer only:
    Governed Revenue Ops Diagnostic

All external actions remain approval-first (draft_only/approval_required).
No live send and no live charge is performed by this module.
"""

from __future__ import annotations

import os
import re
import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LeadGrade = Literal["A", "B", "C", "D"]
FunnelState = Literal[
    "visitor",
    "lead_captured",
    "qualified_A",
    "qualified_B",
    "nurture",
    "meeting_booked",
    "meeting_done",
    "scope_requested",
    "scope_sent",
    "invoice_sent",
    "invoice_paid",
    "delivery_started",
    "proof_pack_sent",
    "upsell_sprint",
    "retainer_candidate",
    "closed_lost",
]
DiagnosticTier = Literal["starter", "standard", "executive"]

_OFFER_NAME = "Governed Revenue Ops Diagnostic"
_JSONL_PATH = os.path.join("data", "governed_revenue_ops_diagnostic.jsonl")
_STORE: dict[str, "FunnelRecord"] = {}

_STATE_TRANSITIONS: dict[FunnelState, set[FunnelState]] = {
    "visitor": {"lead_captured", "closed_lost"},
    "lead_captured": {"qualified_A", "qualified_B", "nurture", "closed_lost"},
    "qualified_A": {"meeting_booked", "nurture", "closed_lost"},
    "qualified_B": {"nurture", "meeting_booked", "closed_lost"},
    "nurture": {"qualified_A", "qualified_B", "meeting_booked", "closed_lost"},
    "meeting_booked": {"meeting_done", "closed_lost"},
    "meeting_done": {"scope_requested", "closed_lost"},
    "scope_requested": {"scope_sent", "closed_lost"},
    "scope_sent": {"invoice_sent", "closed_lost"},
    "invoice_sent": {"invoice_paid", "closed_lost"},
    "invoice_paid": {"delivery_started", "closed_lost"},
    "delivery_started": {"proof_pack_sent", "closed_lost"},
    "proof_pack_sent": {"upsell_sprint", "retainer_candidate", "closed_lost"},
    "upsell_sprint": {"retainer_candidate", "closed_lost"},
    "retainer_candidate": {"closed_lost"},
    "closed_lost": set(),
}

_TIER_PRICING: dict[DiagnosticTier, int] = {
    "starter": 4999,
    "standard": 9999,
    "executive": 15000,
}

_DECISION_MAKER_HINTS = (
    "founder", "co-founder", "ceo", "coo", "cro", "head", "director", "vp", "gm",
    "owner", "partner", "lead", "مؤسس", "مدير", "رئيس",
)
_PARTNER_HINTS = (
    "consultant", "agency", "implementer", "partner", "vc", "investor", "advisor",
    "زوهو", "hubspot", "مستشار", "شريك", "مستثمر",
)
_STUDENT_HINTS = ("student", "intern", "job seeker", "looking for a job", "طالب", "متدرب")
_VAGUE_HINTS = ("just curious", "explore ai", "general ai", "فضول", "نجرب")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    hay = text.lower()
    return any(term in hay for term in terms)


def _budget_is_5k_plus(raw: str) -> bool:
    text = raw.lower().replace(",", "")
    if "5k" in text or "5000" in text or "4999" in text or "10000" in text:
        return True
    numbers = [int(match) for match in re.findall(r"\d+", text)]
    return any(value >= 5000 for value in numbers)


def _urgency_within_30_days(raw: str) -> bool:
    text = raw.lower()
    return (
        "30" in text
        or "this month" in text
        or "urgent" in text
        or "now" in text
        or "خلال شهر" in text
        or "مستعجل" in text
    )


class LeadCaptureInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    company: str = Field(default="", max_length=160)
    role: str = Field(default="", max_length=120)
    email: str = Field(min_length=3, max_length=200)
    linkedin_url: str = Field(default="", max_length=400)
    industry: str = Field(default="", max_length=100)
    team_size: str = Field(default="", max_length=100)
    current_crm: str = Field(default="", max_length=100)
    ai_usage_today: str = Field(default="", max_length=500)
    main_pain: str = Field(default="", max_length=1000)
    urgency: str = Field(default="", max_length=120)
    budget_range: str = Field(default="", max_length=120)
    permission_to_contact: bool = False
    source: str = Field(default="landing", max_length=80)
    region: str = Field(default="Saudi Arabia", max_length=80)


class ApprovalQueueItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approval_id: str
    action_type: str
    channel: str
    draft_text: str
    action_mode: Literal["approval_required"] = "approval_required"
    status: Literal["pending", "approved", "rejected"] = "pending"
    created_at: datetime = Field(default_factory=_now)


class ScoreResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score_total: int
    grade: LeadGrade
    score_breakdown: dict[str, int]
    reasons: list[str]
    recommended_state: FunnelState


class FunnelRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    funnel_id: str
    offer_name: str = _OFFER_NAME
    state: FunnelState
    state_history: list[FunnelState] = Field(default_factory=list)
    lead_grade: LeadGrade
    lead_score_total: int
    score_breakdown: dict[str, int] = Field(default_factory=dict)
    scoring_reasons: list[str] = Field(default_factory=list)
    lead: LeadCaptureInput
    recommended_offer: dict[str, str]
    follow_up_draft: ApprovalQueueItem | None = None
    approval_queue: list[ApprovalQueueItem] = Field(default_factory=list)
    meeting_brief: dict[str, object] | None = None
    scope_draft: dict[str, object] | None = None
    invoice_draft: dict[str, object] | None = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    safety_summary: str = "all_external_actions_are_approval_required"


def _should_persist() -> bool:
    return os.getenv("APP_ENV") != "test" and os.getenv("DEALIX_DISABLE_LOCAL_PERSIST") != "1"


def _persist(record: FunnelRecord) -> None:
    _STORE[record.funnel_id] = record
    if not _should_persist():
        return
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)
    with open(_JSONL_PATH, "a", encoding="utf-8") as handle:
        handle.write(record.model_dump_json() + "\n")


def _grade_to_state(grade: LeadGrade) -> FunnelState:
    if grade == "A":
        return "qualified_A"
    if grade == "B":
        return "qualified_B"
    if grade == "C":
        return "nurture"
    return "closed_lost"


def score_lead(payload: LeadCaptureInput) -> ScoreResult:
    score = 0
    breakdown: dict[str, int] = {}
    reasons: list[str] = []

    role = payload.role.strip()
    company = payload.company.strip()
    region = payload.region.strip().lower()
    crm = payload.current_crm.strip().lower()
    ai_usage = payload.ai_usage_today.strip().lower()
    pain = payload.main_pain.strip().lower()
    urgency = payload.urgency.strip()
    budget = payload.budget_range.strip()
    industry = payload.industry.strip().lower()

    decision_maker = _contains_any(role, _DECISION_MAKER_HINTS)
    partner_profile = _contains_any(role, _PARTNER_HINTS) or _contains_any(industry, _PARTNER_HINTS)
    student_profile = _contains_any(role, _STUDENT_HINTS)
    has_company = bool(company)
    uses_crm = bool(crm and crm not in {"none", "unknown", "n/a", "لا يوجد"})
    has_ai_signal = bool(ai_usage and ai_usage not in {"none", "not using", "no ai", "لا يوجد"})
    gcc_b2b = ("saudi" in region or "gcc" in region or "uae" in region or "qatar" in region) and has_company
    urgent_30 = _urgency_within_30_days(urgency)
    budget_5k_plus = _budget_is_5k_plus(budget)
    vague_curiosity = _contains_any(pain, _VAGUE_HINTS) or len(pain) < 12

    if decision_maker:
        score += 3
        breakdown["decision_maker"] = 3
    if uses_crm:
        score += 3
        breakdown["uses_crm"] = 3
    if has_ai_signal:
        score += 3
        breakdown["has_ai_or_automation_signal"] = 3
    if gcc_b2b:
        score += 2
        breakdown["gcc_b2b"] = 2
    if urgent_30:
        score += 2
        breakdown["urgency_under_30_days"] = 2
    if budget_5k_plus:
        score += 2
        breakdown["budget_5k_plus_sar"] = 2
    if student_profile:
        score -= 3
        breakdown["student_or_job_seeker"] = -3
    if not has_company:
        score -= 3
        breakdown["no_company"] = -3
    if vague_curiosity:
        score -= 2
        breakdown["vague_curiosity"] = -2

    a_criteria = all([
        has_company,
        decision_maker,
        uses_crm or "pipeline" in pain or "crm" in pain or "process" in pain,
        has_ai_signal or "ai" in pain,
        budget_5k_plus,
    ])
    b_criteria = has_company and ("crm" in pain or "pipeline" in pain or "process" in pain)

    if student_profile:
        grade: LeadGrade = "D"
        reasons.append("Non-commercial profile (student/job seeker).")
    elif partner_profile:
        grade = "C"
        reasons.append("Partner/referral profile.")
    elif a_criteria and score >= 10:
        grade = "A"
        reasons.append("Strong ICP fit for paid diagnostic now.")
    elif b_criteria and score >= 6:
        grade = "B"
        reasons.append("Qualified but budget/timing confidence is not complete.")
    elif score >= 3:
        grade = "C"
        reasons.append("Low-confidence fit; keep in nurture/partner path.")
    else:
        grade = "D"
        reasons.append("Not enough business pain/fit signal.")

    return ScoreResult(
        score_total=score,
        grade=grade,
        score_breakdown=breakdown,
        reasons=reasons,
        recommended_state=_grade_to_state(grade),
    )


def _build_recommended_offer(payload: LeadCaptureInput) -> dict[str, str]:
    tier: DiagnosticTier = "starter"
    if _budget_is_5k_plus(payload.budget_range):
        tier = "standard"
    if _budget_is_5k_plus(payload.budget_range) and ("enterprise" in payload.team_size.lower() or "100" in payload.team_size):
        tier = "executive"
    return {
        "offer_name": _OFFER_NAME,
        "recommended_tier": tier,
        "recommended_price_sar": str(_TIER_PRICING[tier]),
        "value_statement": "Map revenue leakage, data readiness, and AI governance risks in 7 days.",
    }


def _approval_item(*, action_type: str, channel: str, draft_text: str) -> ApprovalQueueItem:
    return ApprovalQueueItem(
        approval_id=f"apr_{uuid.uuid4().hex[:10]}",
        action_type=action_type,
        channel=channel,
        draft_text=draft_text,
    )


def _follow_up_draft(payload: LeadCaptureInput, grade: LeadGrade) -> str:
    if grade == "A":
        return (
            f"Hi {payload.name}, thanks for sharing context on {payload.company}. "
            "I prepared a diagnostic review path for one workflow so we can map source clarity, "
            "approval boundaries, evidence trail, and proof of value in 20 minutes."
        )
    if grade == "B":
        return (
            f"Hi {payload.name}, thanks for the context. "
            "Would you like a sample proof pack first, then we can decide timing for a diagnostic review?"
        )
    if grade == "C":
        return (
            f"Hi {payload.name}, appreciated your note. "
            "If you are open, we can discuss a partner motion where you bring clients and Dealix delivers the governed diagnostic."
        )
    return "Lead does not match paid diagnostic profile now; keep as internal archive."


def capture_lead(payload: LeadCaptureInput) -> FunnelRecord:
    if not payload.permission_to_contact:
        raise ValueError("permission_to_contact must be true before any follow-up draft.")

    score = score_lead(payload)
    state = score.recommended_state
    record = FunnelRecord(
        funnel_id=f"funnel_{uuid.uuid4().hex[:10]}",
        state=state,
        state_history=["visitor", "lead_captured", state],
        lead_grade=score.grade,
        lead_score_total=score.score_total,
        score_breakdown=score.score_breakdown,
        scoring_reasons=score.reasons,
        lead=payload,
        recommended_offer=_build_recommended_offer(payload),
    )

    follow_up = _approval_item(
        action_type="send_follow_up_draft",
        channel="email",
        draft_text=_follow_up_draft(payload, score.grade),
    )
    record.follow_up_draft = follow_up
    record.approval_queue.append(follow_up)

    if score.grade == "A":
        record.approval_queue.append(_approval_item(
            action_type="send_booking_link_draft",
            channel="email",
            draft_text="Send booking link draft for Diagnostic Review (20-minute discovery).",
        ))
    elif score.grade == "B":
        record.approval_queue.append(_approval_item(
            action_type="send_sample_proof_pack_draft",
            channel="email",
            draft_text="Send sample proof pack first, then propose booking link if qualified.",
        ))
    elif score.grade == "C":
        record.approval_queue.append(_approval_item(
            action_type="send_partner_motion_draft",
            channel="linkedin",
            draft_text="Share referral/partner offer draft. No live send without founder approval.",
        ))

    record.updated_at = _now()
    _persist(record)
    return record


def _record_or_raise(funnel_id: str) -> FunnelRecord:
    rec = _STORE.get(funnel_id)
    if rec is None:
        raise ValueError("funnel_id not found")
    return rec


def _require_history(record: FunnelRecord, state: FunnelState, reason: str) -> None:
    if state not in record.state_history:
        raise ValueError(reason)


def advance_state(*, funnel_id: str, target_state: FunnelState) -> FunnelRecord:
    record = _record_or_raise(funnel_id)
    current = record.state
    allowed = _STATE_TRANSITIONS[current]
    if target_state not in allowed:
        raise ValueError(f"invalid transition: {current} -> {target_state}")

    if target_state == "invoice_sent":
        _require_history(record, "scope_sent", "cannot reach invoice_sent before scope_sent")
    if target_state == "delivery_started":
        _require_history(record, "invoice_paid", "cannot reach delivery_started before invoice_paid")
    if target_state == "proof_pack_sent":
        _require_history(record, "delivery_started", "cannot reach proof_pack_sent before delivery_started")
    if target_state in {"upsell_sprint", "retainer_candidate"}:
        _require_history(record, "proof_pack_sent", "cannot upsell before proof_pack_sent")

    record.state = target_state
    record.state_history.append(target_state)
    record.updated_at = _now()
    _persist(record)
    return record


def build_meeting_brief(*, funnel_id: str) -> dict[str, object]:
    record = _record_or_raise(funnel_id)
    lead = record.lead
    brief: dict[str, object] = {
        "company_context": {
            "company": lead.company or "Unknown company",
            "industry": lead.industry or "Unspecified",
            "team_size": lead.team_size or "Unspecified",
            "crm": lead.current_crm or "Unknown",
        },
        "likely_pain": lead.main_pain or "CRM/pipeline quality and workflow governance gap.",
        "recommended_vertical": lead.industry or "b2b_services",
        "recommended_offer": record.recommended_offer,
        "discovery_questions": [
            "Which single revenue workflow leaks the most value today?",
            "Which source fields are trusted vs. missing in your CRM pipeline?",
            "Where is AI used today without explicit approval boundaries?",
        ],
        "demo_path": [
            "Show current workflow map.",
            "Show source clarity and data quality notes.",
            "Show approval boundaries and evidence trail example.",
            "Show top three decisions for the next 7 days.",
        ],
        "risk_warnings": [
            "No external message is sent without founder approval.",
            "No legal/security guarantee claims are allowed.",
            "No case study publication without written customer consent.",
        ],
        "next_step": "If fit is confirmed, move to scope_requested then scope_sent.",
    }
    record.meeting_brief = brief
    record.updated_at = _now()
    _persist(record)
    return brief


def build_scope_draft(*, funnel_id: str, tier: DiagnosticTier) -> dict[str, object]:
    record = _record_or_raise(funnel_id)
    if "meeting_done" not in record.state_history:
        raise ValueError("scope draft requires meeting_done first")
    amount = _TIER_PRICING[tier]
    scope = {
        "offer_name": _OFFER_NAME,
        "tier": tier,
        "amount_sar": amount,
        "timeline_days": 7,
        "deliverables": [
            "Workflow map",
            "Source quality notes",
            "Approval risks",
            "AI usage risks",
            "Revenue leakage points",
            "Top 3 operational decisions",
            "Proof pack appendix",
        ],
        "action_mode": "approval_required",
    }
    record.scope_draft = scope
    record.approval_queue.append(_approval_item(
        action_type="send_scope_draft",
        channel="email",
        draft_text=f"Send {tier} scope draft for {_OFFER_NAME} ({amount} SAR).",
    ))
    record.updated_at = _now()
    _persist(record)
    return scope


def build_invoice_draft(
    *,
    funnel_id: str,
    tier: DiagnosticTier,
    payment_method: Literal["bank_transfer", "payment_link_external"] = "payment_link_external",
) -> dict[str, object]:
    record = _record_or_raise(funnel_id)
    if "scope_sent" not in record.state_history:
        raise ValueError("invoice draft requires scope_sent first")
    amount = _TIER_PRICING[tier]
    invoice = {
        "offer_name": _OFFER_NAME,
        "tier": tier,
        "amount_sar": amount,
        "payment_method": payment_method,
        "payment_note": (
            "Use external payment link (Tap/PayTabs/HyperPay/Stripe if supported) "
            "or PDF invoice with bank transfer."
        ),
        "status": "draft",
        "action_mode": "approval_required",
    }
    record.invoice_draft = invoice
    record.approval_queue.append(_approval_item(
        action_type="send_invoice_draft",
        channel="email",
        draft_text=f"Send invoice draft for {amount} SAR via {payment_method}.",
    ))
    record.updated_at = _now()
    _persist(record)
    return invoice


def get_record(funnel_id: str) -> FunnelRecord:
    return _record_or_raise(funnel_id)


def list_records() -> list[FunnelRecord]:
    return sorted(_STORE.values(), key=lambda rec: rec.updated_at, reverse=True)


def daily_dashboard() -> dict[str, object]:
    records = list_records()
    state_counts: dict[str, int] = {state: 0 for state in _STATE_TRANSITIONS}
    qualified_a = 0
    meeting_booked = 0
    scopes_requested = 0
    invoices_sent = 0
    invoices_paid = 0
    proof_delivered = 0
    blocked_approvals = 0

    for rec in records:
        state_counts[rec.state] = state_counts.get(rec.state, 0) + 1
        qualified_a += 1 if "qualified_A" in rec.state_history else 0
        meeting_booked += 1 if "meeting_booked" in rec.state_history else 0
        scopes_requested += 1 if "scope_requested" in rec.state_history else 0
        invoices_sent += 1 if "invoice_sent" in rec.state_history else 0
        invoices_paid += 1 if "invoice_paid" in rec.state_history else 0
        proof_delivered += 1 if "proof_pack_sent" in rec.state_history else 0
        blocked_approvals += len([item for item in rec.approval_queue if item.status == "pending"])

    return {
        "offer": _OFFER_NAME,
        "kpis": {
            "new_leads": state_counts["lead_captured"],
            "qualified_A": qualified_a,
            "meetings_booked": meeting_booked,
            "scopes_requested": scopes_requested,
            "invoices_sent": invoices_sent,
            "invoices_paid": invoices_paid,
            "proof_packs_delivered": proof_delivered,
            "blocked_approvals": blocked_approvals,
        },
        "state_counts": state_counts,
        "next_best_actions": [
            "Approve pending outbound drafts in queue.",
            "Advance qualified_A leads to meeting_booked within 24h.",
            "Do not start delivery before invoice_paid.",
        ],
        "guardrails": {
            "no_invoice_before_scope": True,
            "no_delivery_before_invoice_paid": True,
            "no_proof_before_delivery": True,
            "no_upsell_before_proof": True,
            "no_case_study_without_written_approval": True,
            "all_external_actions_approval_required": True,
        },
    }


def sample_proof_pack() -> dict[str, object]:
    return {
        "offer": _OFFER_NAME,
        "title": "Sample Proof Pack (Draft)",
        "sections": [
            "Executive Summary",
            "Workflow Map",
            "Source Quality Notes",
            "Approval Risks",
            "AI Usage Risks",
            "Revenue Leakage Points",
            "Top 3 Decisions",
            "Recommended Sprint",
            "Evidence Appendix",
        ],
        "action_mode": "approval_required",
        "note": "Sample only. Client-facing pack must be approved before external sharing.",
    }


def reset_store_for_tests() -> None:
    _STORE.clear()
