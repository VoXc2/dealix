"""Governed Revenue & AI Operations policy primitives.

This module codifies the company-level operating law:
- Decision quality over vanity activity.
- Approval-first external actions.
- Evidence-linked progression from L2 to L7.
"""

from __future__ import annotations

from typing import Literal

EvidenceState = Literal[
    "prepared_not_sent",
    "sent",
    "replied_interested",
    "meeting_booked",
    "used_in_meeting",
    "scope_requested",
    "pilot_intro_requested",
    "invoice_sent",
    "invoice_paid",
]

EvidenceLevel = Literal[
    "L2",
    "L4",
    "L5",
    "L6",
    "L7_candidate",
    "L7_confirmed",
]

NORTH_STAR_KEY = "governed_value_decisions_created"
NORTH_STAR_DEFINITION_EN = (
    "Count of operating or revenue decisions taken with a clear source, "
    "explicit approval, logged evidence, and measurable business impact."
)
NORTH_STAR_DEFINITION_AR = (
    "عدد القرارات التشغيلية أو الإيرادية التي تمت بمصدر واضح وموافقة واضحة "
    "ودليل موثق وأثر قابل للقياس."
)

CORE_COMMERCIAL_OFFERS: tuple[str, ...] = (
    "governed_revenue_ops_diagnostic",
    "revenue_intelligence_sprint",
    "governed_ops_retainer",
)

EVIDENCE_STATE_LEVEL: dict[EvidenceState, EvidenceLevel] = {
    "prepared_not_sent": "L2",
    "sent": "L4",
    "replied_interested": "L4",
    "meeting_booked": "L4",
    "used_in_meeting": "L5",
    "scope_requested": "L6",
    "pilot_intro_requested": "L6",
    "invoice_sent": "L7_candidate",
    "invoice_paid": "L7_confirmed",
}

_ALLOWED_TRANSITIONS: dict[EvidenceState, tuple[EvidenceState, ...]] = {
    "prepared_not_sent": ("sent",),
    "sent": ("replied_interested", "meeting_booked"),
    "replied_interested": ("meeting_booked",),
    "meeting_booked": ("used_in_meeting",),
    "used_in_meeting": ("scope_requested", "pilot_intro_requested"),
    "scope_requested": ("invoice_sent",),
    "pilot_intro_requested": ("invoice_sent",),
    "invoice_sent": ("invoice_paid",),
    "invoice_paid": (),
}


def next_allowed_states(state: EvidenceState) -> tuple[EvidenceState, ...]:
    """Return valid next states for one engagement evidence record."""
    return _ALLOWED_TRANSITIONS[state]


def validate_transition(
    current: EvidenceState,
    target: EvidenceState,
    *,
    founder_confirmed: bool,
    payment_received: bool,
    used_in_meeting: bool,
    market_pull_confirmed: bool,
) -> tuple[bool, str]:
    """Validate a state transition under Dealix governance rules."""
    if target not in _ALLOWED_TRANSITIONS[current]:
        return False, f"invalid_transition:{current}->{target}"

    if target == "sent" and not founder_confirmed:
        return False, "founder_confirmation_required_before_send"

    if EVIDENCE_STATE_LEVEL[target] in {"L5", "L6", "L7_candidate", "L7_confirmed"} and not used_in_meeting:
        return False, "l5_plus_requires_used_in_meeting"

    if target in {"invoice_sent", "invoice_paid"} and not market_pull_confirmed:
        return False, "l6_signal_required_before_invoice"

    if target == "invoice_paid" and not payment_received:
        return False, "payment_required_for_l7_confirmed"

    return True, "ok"


def can_recognize_revenue(
    *,
    evidence_state: EvidenceState,
    payment_received: bool,
) -> bool:
    """Revenue is recognized only after confirmed payment."""
    return evidence_state == "invoice_paid" and payment_received


def is_governed_value_decision(
    *,
    has_source: bool,
    has_approval: bool,
    has_evidence: bool,
    measurable_impact: bool,
) -> bool:
    """North Star counting predicate for one decision."""
    return has_source and has_approval and has_evidence and measurable_impact
