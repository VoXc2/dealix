"""Stage transition and external-action policy guards (deterministic)."""

from __future__ import annotations

from dealix.revenue_ops_autopilot.schemas import LeadStage

_ORDER: tuple[LeadStage, ...] = (
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


def _idx(stage: LeadStage) -> int:
    try:
        return _ORDER.index(stage)
    except ValueError:
        return -1


def stage_transition_allowed(
    current: LeadStage,
    target: LeadStage,
    *,
    has_meeting_evidence: bool = False,
    has_scope_evidence: bool = False,
    has_payment_proof: bool = False,
    founder_reviewed_proof_pack: bool = False,
) -> tuple[bool, str]:
    """Returns (ok, reason)."""
    # Terminal / loss
    if target == "closed_lost":
        return True, "ok_closed_lost"

    # Explicit backward moves require manual ops (prevent accidental rewinds via API).
    if _idx(target) < _idx(current) and current not in {"closed_lost", "nurture"}:
        return False, "backward_transition_blocked"

    if target == "invoice_paid" and not has_payment_proof:
        return False, "needs_payment_proof"
    if target == "delivery_started":
        if current != "invoice_paid" and not has_payment_proof:
            return False, "needs_invoice_paid_before_delivery"
    if target == "invoice_sent":
        prev_ok = current in {"scope_sent", "scope_requested"} or has_scope_evidence
        if not prev_ok:
            return False, "needs_scope_evidence_before_invoice"
    if target == "proof_pack_sent":
        if not founder_reviewed_proof_pack:
            return False, "needs_founder_review_proof_pack"

    stages_needing_meeting = {
        "meeting_done",
        "scope_requested",
        "scope_sent",
        "invoice_sent",
        "invoice_paid",
        "delivery_started",
        "proof_pack_sent",
    }
    if target in stages_needing_meeting and not has_meeting_evidence:
        if target in {"scope_sent", "invoice_sent"}:
            return False, "needs_meeting_evidence_L5_plus"

    from dealix.revenue_ops_autopilot.config_loader import allowed_stage_edges

    edges = allowed_stage_edges()
    allowed = edges.get(current)
    if allowed and target not in allowed and target != "closed_lost":
        return False, "yaml_transition_not_allowed"

    return True, "ok"


def outbound_requires_approval(action: str) -> bool:
    return action in {
        "first_message_send",
        "invoice_send_final",
        "scope_send_final",
        "case_study_publish",
        "diagnostic_final",
        "external_agent_action",
    }


def kb_auto_reply_allowed(*, intent: str, risk_level: str) -> bool:
    if risk_level in {"high", "critical"}:
        return False
    safe_intents = {
        "faq_general",
        "pricing_question",
        "proof_pack_question",
        "delivery_status",
        "partnership",
    }
    return intent in safe_intents


# Billing draft may bind to funnel lead only after scope is materially agreed (Playbook Assurance §4).
INVOICE_DRAFT_ALLOWED_LEAD_STAGES: frozenset[LeadStage] = frozenset(
    (
        "scope_sent",
        "invoice_sent",
        "invoice_paid",
        "delivery_started",
        "proof_pack_sent",
        "sprint_candidate",
        "retainer_candidate",
    ),
)
