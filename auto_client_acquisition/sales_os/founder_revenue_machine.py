"""Founder-led Revenue Machine primitives for the Dealix Sales OS.

Deterministic only:
- no external sends
- no invoice finalization
- no autonomous actions without explicit approval flags
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


PipelineState = Literal[
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
]

DiagnosticTier = Literal["starter", "standard", "executive"]
RiskBand = Literal["low", "medium", "high"]

PIPELINE_STATES: tuple[PipelineState, ...] = (
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

PRICING_TIERS_SAR: dict[DiagnosticTier, int] = {
    "starter": 4999,
    "standard": 9999,
    "executive": 15000,
}

_TRANSITIONS: dict[PipelineState, tuple[PipelineState, ...]] = {
    "new_lead": ("qualified_A", "qualified_B", "nurture", "partner_candidate", "closed_lost"),
    "qualified_A": ("meeting_booked", "nurture", "closed_lost"),
    "qualified_B": ("meeting_booked", "nurture", "partner_candidate", "closed_lost"),
    "nurture": ("qualified_B", "qualified_A", "meeting_booked", "closed_lost"),
    "partner_candidate": ("meeting_booked", "nurture", "closed_lost"),
    "meeting_booked": ("meeting_done", "nurture", "closed_lost"),
    "meeting_done": ("scope_requested", "nurture", "closed_lost"),
    "scope_requested": ("scope_sent", "nurture", "closed_lost"),
    "scope_sent": ("invoice_sent", "nurture", "closed_lost"),
    "invoice_sent": ("invoice_paid", "nurture", "closed_lost"),
    "invoice_paid": ("delivery_started", "closed_lost"),
    "delivery_started": ("proof_pack_sent", "closed_lost"),
    "proof_pack_sent": ("sprint_candidate", "retainer_candidate", "nurture", "closed_lost"),
    "sprint_candidate": ("retainer_candidate", "nurture", "closed_lost"),
    "retainer_candidate": ("nurture", "closed_lost"),
    "closed_lost": (),
}

_NEXT_ACTIONS: dict[PipelineState, str] = {
    "new_lead": "Score lead and choose one governed next step.",
    "qualified_A": "Review account and approve a personalized booking invite draft.",
    "qualified_B": "Send a proof-first nurture touch with Sample Proof Pack CTA.",
    "nurture": "Queue the next nurture touch from sequence.",
    "partner_candidate": "Send partner-angle intro and propose referral/joint diagnostic.",
    "meeting_booked": "Prepare meeting brief, discovery questions, and demo path.",
    "meeting_done": "Capture discovery notes and decide scope or nurture.",
    "scope_requested": "Generate scope + pricing recommendation + invoice draft for approval.",
    "scope_sent": "Follow up and move to invoice only after explicit approval.",
    "invoice_sent": "Track payment and prepare onboarding assets.",
    "invoice_paid": "Open delivery checklist and evidence logging.",
    "delivery_started": "Build the Proof Pack draft and schedule review.",
    "proof_pack_sent": "Trigger upsell decision (Sprint/Retainer) and referral ask.",
    "sprint_candidate": "Finalize sprint scope and payment path.",
    "retainer_candidate": "Finalize recurring governance cadence and contract details.",
    "closed_lost": "Document reason and stop outbound unless re-opened by consent.",
}

MACHINE_GUARDRAILS: tuple[str, ...] = (
    "No meeting_done without notes.",
    "No scope_sent without fit score.",
    "No invoice_sent without founder approval.",
    "No delivery_started without invoice_paid.",
    "No proof_pack_sent without founder review.",
    "No case study publish without written approval.",
)

SALES_MACHINE_CONFIG: dict[str, Any] = {
    "offer_name": "7-Day Governed Revenue & AI Ops Diagnostic",
    "delivery_window_business_days": "5-7",
    "promise": (
        "Identify revenue leakage, data readiness gaps, AI risk boundaries, "
        "and the top 3 operational decisions with evidence."
    ),
    "ctas": {
        "primary": "Get Sample Proof Pack",
        "secondary": "Book Diagnostic Review",
    },
    "pricing_sar": PRICING_TIERS_SAR,
    "deliverables": [
        "Revenue Workflow Map",
        "CRM / Source Quality Review",
        "AI Usage Risk Review",
        "Approval Boundaries",
        "Evidence Trail Gaps",
        "Top 3 Revenue Decisions",
        "Proof Pack",
        "Recommended Sprint / Retainer",
    ],
    "what_we_do_not_do": [
        "We do not send autonomous AI messages.",
        "We do not claim revenue without evidence.",
        "We do not replace your CRM.",
        "We do not publish case studies without approval.",
        "We do not sell generic chatbot automation.",
    ],
}


def recommended_tier(score: int) -> DiagnosticTier:
    """Map qualification score to a starting diagnostic tier."""
    if score >= 15:
        return "executive"
    if score >= 12:
        return "standard"
    return "starter"


def score_lead_fit(*, signals: dict[str, bool]) -> dict[str, Any]:
    """Score lead using the exact Founder-led weighting rubric."""
    score = 0

    if signals.get("decision_maker"):
        score += 3
    if signals.get("b2b_company"):
        score += 3
    if signals.get("has_crm_or_revenue_process"):
        score += 3
    if signals.get("uses_or_plans_ai"):
        score += 3
    if signals.get("saudi_or_gcc"):
        score += 2
    if signals.get("urgency_within_30_days"):
        score += 2
    if signals.get("budget_5k_sar_plus"):
        score += 2

    if signals.get("no_company"):
        score -= 3
    if signals.get("student_or_job_seeker"):
        score -= 3
    if signals.get("vague_curiosity"):
        score -= 2

    if score >= 12:
        stage: PipelineState = "qualified_A"
    elif score >= 8:
        stage = "qualified_B"
    elif score >= 5:
        stage = "nurture"
    else:
        stage = "closed_lost"

    tier = None if stage in {"nurture", "closed_lost"} else recommended_tier(score)
    return {
        "score": score,
        "stage": stage,
        "recommended_tier": tier,
        "next_action": _NEXT_ACTIONS[stage],
        "evidence_event": "lead_captured",
    }


@dataclass(frozen=True, slots=True)
class RiskScoreInput:
    has_crm: bool
    uses_ai: bool
    has_external_approval_gate: bool
    can_link_workflow_to_financial_outcome: bool
    follow_up_is_documented: bool
    source_clarity_for_decisions: bool
    has_evidence_pack: bool


def compute_ops_risk_score(payload: RiskScoreInput) -> dict[str, Any]:
    """Compute AI + revenue ops governance risk for lead-magnet form."""
    controls = (
        payload.has_crm,
        payload.has_external_approval_gate,
        payload.can_link_workflow_to_financial_outcome,
        payload.follow_up_is_documented,
        payload.source_clarity_for_decisions,
        payload.has_evidence_pack,
    )
    missing_controls = sum(1 for ok in controls if not ok)
    numeric_score = int((missing_controls / len(controls)) * 100)

    if missing_controls >= 4 or (payload.uses_ai and missing_controls >= 3):
        risk_band: RiskBand = "high"
    elif missing_controls >= 2:
        risk_band = "medium"
    else:
        risk_band = "low"

    recommended_step = {
        "high": "Book Diagnostic Review",
        "medium": "Get Sample Proof Pack then book a review",
        "low": "Review one workflow and decide if a 7-day diagnostic is needed",
    }[risk_band]

    return {
        "risk_band": risk_band,
        "numeric_score": numeric_score,
        "missing_controls": missing_controls,
        "recommended_step": recommended_step,
        "cta_primary": SALES_MACHINE_CONFIG["ctas"]["primary"],
        "cta_secondary": SALES_MACHINE_CONFIG["ctas"]["secondary"],
    }


def validate_transition(
    *,
    current_state: str,
    target_state: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate pipeline transition with strict governance guardrails."""
    context = context or {}
    if current_state not in PIPELINE_STATES:
        return {"allowed": False, "reason": "unknown_current_state"}
    if target_state not in PIPELINE_STATES:
        return {"allowed": False, "reason": "unknown_target_state"}

    current = current_state  # narrowing for readability
    target = target_state
    allowed_targets = _TRANSITIONS[current]  # type: ignore[index]
    if target not in allowed_targets:
        return {"allowed": False, "reason": "transition_not_allowed"}

    if target == "meeting_done" and not str(context.get("meeting_notes") or "").strip():
        return {"allowed": False, "reason": "meeting_notes_required"}
    if target == "scope_sent" and context.get("fit_score") is None:
        return {"allowed": False, "reason": "fit_score_required"}
    if target == "invoice_sent" and not bool(context.get("founder_approved_invoice")):
        return {"allowed": False, "reason": "founder_invoice_approval_required"}
    if target == "delivery_started" and current != "invoice_paid":
        return {"allowed": False, "reason": "invoice_paid_required_before_delivery"}
    if target == "proof_pack_sent" and not bool(context.get("founder_approved_proof_pack")):
        return {"allowed": False, "reason": "founder_proof_pack_approval_required"}
    if bool(context.get("publish_case_study")) and not bool(context.get("written_case_study_approval")):
        return {"allowed": False, "reason": "written_case_study_approval_required"}

    return {
        "allowed": True,
        "reason": "ok",
        "evidence_event": target,
        "next_action": _NEXT_ACTIONS[target],  # type: ignore[index]
    }


def transitions() -> dict[str, list[str]]:
    """JSON-safe transitions map for API responses."""
    return {k: list(v) for k, v in _TRANSITIONS.items()}

