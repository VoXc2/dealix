"""Founder revenue-machine workflows A–G (no LLM, no live sends).

Seven automation steps from the founder-led revenue doctrine. Every
workflow is **draft-only or approval-gated** — none sends a message,
issues an invoice, or charges a card. Each one records exactly one
evidence event to the proof ledger and returns a draft for the founder
to review.

  A  new_lead        — classify a captured lead + draft a follow-up
  B  qualified_a     — draft outreach + meeting brief for a hot lead
  C  meeting_booked  — prepare a discovery meeting brief
  D  meeting_done    — capture discovery outcome + route the next step
  E  scope_requested — draft the diagnostic scope + invoice
  F  invoice_paid    — prepare onboarding + delivery checklist
  G  delivery_done   — draft the final Proof Pack handover + upsell
"""

from __future__ import annotations

import inspect
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from auto_client_acquisition.crm_v10.founder_lead_scoring import score_founder_lead
from auto_client_acquisition.crm_v10.pipeline_view import LeadClassification
from auto_client_acquisition.proof_ledger.factory import get_default_ledger
from auto_client_acquisition.proof_ledger.schemas import ProofEvent, ProofEventType
from auto_client_acquisition.service_catalog.registry import get_offering

# Action modes — never "live_send"/"live_charge" (Article 4).
DRAFT_ONLY = "draft_only"
APPROVAL_REQUIRED = "approval_required"

_DIAGNOSTIC_TIER_IDS = frozenset({
    "governed_diagnostic_starter_4999",
    "governed_diagnostic_standard_9999",
    "governed_diagnostic_executive_15000",
})


class UnknownWorkflow(ValueError):
    """Raised when a workflow name is not in the registry."""


class WorkflowInputError(ValueError):
    """Raised when a workflow receives invalid input."""


@dataclass(frozen=True, slots=True)
class WorkflowDraft:
    """The output of a workflow — a draft, never a sent action."""

    workflow: str
    action_mode: str
    draft: dict[str, Any]
    next_action: str
    proof_event_id: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _record(
    *,
    event_type: ProofEventType,
    company_handle: str,
    summary_en: str,
    summary_ar: str,
    workflow: str,
    payload: dict[str, Any],
) -> str:
    """Append one evidence event and return its id."""
    event = ProofEvent(
        event_type=event_type,
        customer_handle=company_handle,
        summary_en=summary_en,
        summary_ar=summary_ar,
        evidence_source=f"founder_workflow:{workflow}",
        approval_status="approval_required",
        payload={"workflow": workflow, **payload},
    )
    get_default_ledger().record(event)
    return event.id


# ── Workflow A — New Lead ───────────────────────────────────────────
_OFFER_FOR_CLASSIFICATION: dict[str, str | None] = {
    LeadClassification.QUALIFIED_A.value: "governed_diagnostic_starter_4999",
    LeadClassification.QUALIFIED_B.value: "governed_diagnostic_starter_4999",
    LeadClassification.NURTURE.value: "free_mini_diagnostic",
    LeadClassification.PARTNER_CANDIDATE.value: "agency_partner_os",
    LeadClassification.DROP.value: None,
}


def workflow_new_lead(
    *,
    company_handle: str = "Saudi B2B lead",
    decision_maker: bool = False,
    is_b2b: bool = False,
    has_crm_or_revenue_process: bool = False,
    uses_or_plans_ai: bool = False,
    in_gcc: bool = False,
    urgent_within_30_days: bool = False,
    budget_5k_plus_sar: bool = False,
    no_company: bool = False,
    student_or_jobseeker: bool = False,
    vague_curiosity: bool = False,
    is_partner: bool = False,
) -> WorkflowDraft:
    """A — score the lead, recommend an offer, draft a follow-up."""
    score = score_founder_lead(
        decision_maker=decision_maker,
        is_b2b=is_b2b,
        has_crm_or_revenue_process=has_crm_or_revenue_process,
        uses_or_plans_ai=uses_or_plans_ai,
        in_gcc=in_gcc,
        urgent_within_30_days=urgent_within_30_days,
        budget_5k_plus_sar=budget_5k_plus_sar,
        no_company=no_company,
        student_or_jobseeker=student_or_jobseeker,
        vague_curiosity=vague_curiosity,
        is_partner=is_partner,
    )
    recommended_offer = _OFFER_FOR_CLASSIFICATION.get(score.classification)
    follow_up_en = (
        "Thanks for reaching out. The lowest-friction next step is a short "
        "diagnostic review of one revenue workflow — source clarity, approval "
        "boundaries, evidence trail, proof of value."
    )
    follow_up_ar = (
        "شكراً لتواصلك. أقل خطوة احتكاكاً هي مراجعة تشخيصيّة قصيرة لـ workflow "
        "إيراد واحد — وضوح المصدر، حدود الموافقة، أثر الأدلّة، إثبات القيمة."
    )
    draft = {
        "classification": score.classification,
        "lead_score": score.score,
        "score_reasons": score.reasons,
        "recommended_offer": recommended_offer,
        "follow_up_draft_en": follow_up_en,
        "follow_up_draft_ar": follow_up_ar,
    }
    next_action = (
        "discard_politely" if score.classification == LeadClassification.DROP.value
        else "founder_review_follow_up_draft"
    )
    event_id = _record(
        event_type=ProofEventType.LEAD_INTAKE,
        company_handle=company_handle,
        summary_en=f"New lead captured — {score.classification} (score {score.score})",
        summary_ar=f"عميل محتمل جديد — {score.classification} (نتيجة {score.score})",
        workflow="new_lead",
        payload=draft,
    )
    return WorkflowDraft(
        workflow="new_lead",
        action_mode=DRAFT_ONLY,
        draft=draft,
        next_action=next_action,
        proof_event_id=event_id,
    )


# ── Workflow B — Qualified A ────────────────────────────────────────
def workflow_qualified_a(
    *,
    company_handle: str = "Saudi B2B lead",
    contact_role: str = "decision maker",
    sector: str = "b2b_services",
) -> WorkflowDraft:
    """B — draft outreach + a meeting brief for a hot (qualified_A) lead."""
    email_en = (
        "Based on what you shared, the most useful starting point is a short "
        "diagnostic review — one workflow, evaluated across source clarity, "
        "approval boundaries, evidence trail, and proof of value. "
        "Would 20 minutes this week work?"
    )
    email_ar = (
        "بناءً على ما شاركته، أفضل نقطة بداية هي مراجعة تشخيصيّة قصيرة — "
        "workflow واحد يُقيَّم من زوايا وضوح المصدر، حدود الموافقة، أثر الأدلّة، "
        "وإثبات القيمة. هل تناسبك ٢٠ دقيقة هذا الأسبوع؟"
    )
    draft = {
        "email_draft_en": email_en,
        "email_draft_ar": email_ar,
        "meeting_brief": {
            "company": company_handle,
            "contact_role": contact_role,
            "sector": sector,
            "objective": "Confirm one workflow worth a 7-day diagnostic",
        },
        "booking_message": "Send the Calendly link only after founder approval.",
    }
    event_id = _record(
        event_type=ProofEventType.LEAD_INTAKE,
        company_handle=company_handle,
        summary_en="Qualified-A outreach draft prepared for founder approval",
        summary_ar="مسودة تواصل لعميل مؤهّل (A) جاهزة لموافقة المؤسّس",
        workflow="qualified_a",
        payload=draft,
    )
    return WorkflowDraft(
        workflow="qualified_a",
        action_mode=APPROVAL_REQUIRED,
        draft=draft,
        next_action="founder_approves_then_sends_booking_link",
        proof_event_id=event_id,
        notes=["outbound message — never sent automatically"],
    )


# ── Workflow C — Meeting Booked ─────────────────────────────────────
def workflow_meeting_booked(
    *,
    company_handle: str = "Saudi B2B lead",
    sector: str = "b2b_services",
) -> WorkflowDraft:
    """C — prepare a discovery meeting brief."""
    draft = {
        "meeting_brief": {
            "company": company_handle,
            "sector": sector,
            "likely_pain": "messy pipeline / weak follow-up / ungoverned AI usage",
            "discovery_questions": [
                "Which revenue workflow loses the most time or money today?",
                "Do you have a CRM, and is it trusted?",
                "Is AI used internally today?",
                "Who approves external messages or decisions?",
                "How do you know a workflow created value?",
            ],
            "demo_path": "sample Proof Pack walkthrough → one-workflow review",
            "objections_expected": ["price", "timing", "we'll do it internally"],
        },
    }
    event_id = _record(
        event_type=ProofEventType.MEETING_BOOKED,
        company_handle=company_handle,
        summary_en="Discovery meeting booked — brief prepared",
        summary_ar="تم حجز اجتماع الاكتشاف — تم تجهيز الملخّص",
        workflow="meeting_booked",
        payload=draft,
    )
    return WorkflowDraft(
        workflow="meeting_booked",
        action_mode=DRAFT_ONLY,
        draft=draft,
        next_action="founder_reviews_brief_before_meeting",
        proof_event_id=event_id,
    )


# ── Workflow D — Meeting Done ───────────────────────────────────────
def workflow_meeting_done(
    *,
    company_handle: str = "Saudi B2B lead",
    pain_confirmed: bool = False,
    budget_range: str = "",
    timeline: str = "",
    decision_maker_present: bool = False,
    scope_requested: bool = False,
) -> WorkflowDraft:
    """D — capture the discovery outcome and route the next step."""
    draft = {
        "pain_confirmed": pain_confirmed,
        "budget_range": budget_range,
        "timeline": timeline,
        "decision_maker_present": decision_maker_present,
        "scope_requested": scope_requested,
    }
    next_action = (
        "run_workflow_scope_requested" if scope_requested
        else "add_to_nurture_sequence"
    )
    event_id = _record(
        event_type=ProofEventType.MEETING_COMPLETED,
        company_handle=company_handle,
        summary_en=f"Discovery completed — scope_requested={scope_requested}",
        summary_ar=f"اكتمل الاكتشاف — طلب نطاق={scope_requested}",
        workflow="meeting_done",
        payload=draft,
    )
    return WorkflowDraft(
        workflow="meeting_done",
        action_mode=DRAFT_ONLY,
        draft=draft,
        next_action=next_action,
        proof_event_id=event_id,
    )


# ── Workflow E — Scope Requested ────────────────────────────────────
def workflow_scope_requested(
    *,
    company_handle: str = "Saudi B2B lead",
    tier: str = "governed_diagnostic_starter_4999",
) -> WorkflowDraft:
    """E — draft the diagnostic scope document + an invoice draft."""
    if tier not in _DIAGNOSTIC_TIER_IDS:
        raise WorkflowInputError(
            f"tier must be one of {sorted(_DIAGNOSTIC_TIER_IDS)}, got {tier!r}"
        )
    offering = get_offering(tier)
    assert offering is not None  # registry guarantees presence for valid ids
    draft = {
        "scope_document": {
            "objective": "7-day Governed Revenue & AI Ops Diagnostic",
            "inputs_required": ["CRM/source export", "AI usage list", "approval map"],
            "diagnostic_activities": list(offering.deliverables),
            "deliverables": list(offering.deliverables),
            "timeline_days": offering.duration_days,
            "price_sar": offering.price_sar,
            "exclusions": ["implementation", "tooling licenses", "ongoing retainer"],
        },
        "invoice_draft": {
            "service_id": offering.id,
            "amount_sar": offering.price_sar,
            "currency": "SAR",
            "status": "draft",
        },
    }
    event_id = _record(
        event_type=ProofEventType.PILOT_OFFERED,
        company_handle=company_handle,
        summary_en=f"Diagnostic scope + invoice drafted ({tier})",
        summary_ar=f"تم تجهيز مسودة النطاق والفاتورة ({tier})",
        workflow="scope_requested",
        payload={"tier": tier, "amount_sar": offering.price_sar},
    )
    return WorkflowDraft(
        workflow="scope_requested",
        action_mode=APPROVAL_REQUIRED,
        draft=draft,
        next_action="founder_approves_scope_and_invoice",
        proof_event_id=event_id,
        notes=["invoice is a draft — founder issues it manually"],
    )


# ── Workflow F — Invoice Paid ───────────────────────────────────────
def workflow_invoice_paid(
    *,
    company_handle: str = "Saudi B2B lead",
    tier: str = "governed_diagnostic_starter_4999",
    payment_evidence_source: str = "",
) -> WorkflowDraft:
    """F — prepare onboarding + the delivery checklist (post-payment)."""
    if tier not in _DIAGNOSTIC_TIER_IDS:
        raise WorkflowInputError(
            f"tier must be one of {sorted(_DIAGNOSTIC_TIER_IDS)}, got {tier!r}"
        )
    if not payment_evidence_source:
        raise WorkflowInputError(
            "payment_evidence_source is required — delivery prep cannot start "
            "without recorded payment evidence"
        )
    draft = {
        "onboarding_form": "diagnostic_onboarding_v1",
        "delivery_folder": f"diagnostic/{company_handle}/{tier}",
        "diagnostic_checklist": [
            "Collect CRM/source export",
            "Map AI usage and approval boundaries",
            "Review evidence trail gaps",
            "Draft revenue workflow map",
            "Draft top 3 revenue decisions",
            "Assemble Proof Pack draft",
        ],
        "proof_pack_draft": f"proof_pack_draft/{company_handle}",
    }
    event_id = _record(
        event_type=ProofEventType.PAYMENT_CONFIRMED,
        company_handle=company_handle,
        summary_en="Payment confirmed — onboarding + delivery checklist prepared",
        summary_ar="تم تأكيد الدفع — تم تجهيز الإعداد وقائمة التسليم",
        workflow="invoice_paid",
        payload={"tier": tier, "payment_evidence_source": payment_evidence_source},
    )
    return WorkflowDraft(
        workflow="invoice_paid",
        action_mode=DRAFT_ONLY,
        draft=draft,
        next_action="founder_starts_delivery",
        proof_event_id=event_id,
    )


# ── Workflow G — Delivery Done ──────────────────────────────────────
def workflow_delivery_done(
    *,
    company_handle: str = "Saudi B2B lead",
    value_confirmed: bool = False,
) -> WorkflowDraft:
    """G — draft the final Proof Pack handover + an upsell recommendation."""
    draft: dict[str, Any] = {
        "final_proof_pack": f"proof_pack/{company_handle}",
        "upsell_recommendation": "revenue_proof_sprint_499",
        "follow_up_task": "Follow up 3 days after Proof Pack handover",
        "testimonial_request": (
            "Request a testimonial — value was confirmed."
            if value_confirmed
            else None
        ),
    }
    notes = ["Proof Pack handover — never sent automatically"]
    if not value_confirmed:
        notes.append("no testimonial request — value not yet confirmed")
    event_id = _record(
        event_type=ProofEventType.PROOF_PACK_SENT,
        company_handle=company_handle,
        summary_en=f"Delivery done — Proof Pack handover drafted (value_confirmed={value_confirmed})",
        summary_ar=f"اكتمل التسليم — تم تجهيز تسليم Proof Pack (تأكيد القيمة={value_confirmed})",
        workflow="delivery_done",
        payload={"value_confirmed": value_confirmed},
    )
    return WorkflowDraft(
        workflow="delivery_done",
        action_mode=APPROVAL_REQUIRED,
        draft=draft,
        next_action="founder_approves_proof_pack_handover_and_upsell",
        proof_event_id=event_id,
        notes=notes,
    )


WORKFLOWS: dict[str, Callable[..., WorkflowDraft]] = {
    "new_lead": workflow_new_lead,
    "qualified_a": workflow_qualified_a,
    "meeting_booked": workflow_meeting_booked,
    "meeting_done": workflow_meeting_done,
    "scope_requested": workflow_scope_requested,
    "invoice_paid": workflow_invoice_paid,
    "delivery_done": workflow_delivery_done,
}


def run_workflow(name: str, params: dict[str, Any]) -> WorkflowDraft:
    """Dispatch a workflow by name.

    ``params`` may carry the union of all workflow fields; only the keys
    the chosen workflow declares are forwarded, so a shared request model
    can drive every workflow.
    """
    fn = WORKFLOWS.get(name)
    if fn is None:
        raise UnknownWorkflow(
            f"unknown workflow {name!r}; known: {sorted(WORKFLOWS)}"
        )
    accepted = set(inspect.signature(fn).parameters)
    return fn(**{k: v for k, v in params.items() if k in accepted})


__all__ = [
    "APPROVAL_REQUIRED",
    "DRAFT_ONLY",
    "UnknownWorkflow",
    "WORKFLOWS",
    "WorkflowDraft",
    "WorkflowInputError",
    "run_workflow",
    "workflow_delivery_done",
    "workflow_invoice_paid",
    "workflow_meeting_booked",
    "workflow_meeting_done",
    "workflow_new_lead",
    "workflow_qualified_a",
    "workflow_scope_requested",
]
