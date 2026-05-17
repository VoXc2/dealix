"""Revenue Assurance gates — deterministic guards for failure-mode tests.

These gates encode the non-negotiable boundaries the Red-Team suite asserts:
no invoice without an approved scope, no commission before payment, no
revenue without a payment, high-risk support escalates, claims need a
source, and agent output without a source is low-confidence.

Pure functions, no I/O.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

DEFAULT_QUALIFIED_LEAD_THRESHOLD = 70


@dataclass(frozen=True, slots=True)
class GateOutcome:
    allowed: bool
    reason: str
    flags: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def lead_approval_gate(
    *, lead_score: int, threshold: int = DEFAULT_QUALIFIED_LEAD_THRESHOLD
) -> GateOutcome:
    """A founder approval task is generated only for qualified leads.

    Weak leads must never disturb the founder; strong leads must.
    """
    qualified = lead_score >= threshold
    return GateOutcome(
        allowed=qualified,
        reason="qualified_lead" if qualified else "weak_lead_no_founder_disturb",
        flags={"generates_approval_task": qualified, "lead_score": lead_score},
    )


def claim_source_gate(*, has_source: bool) -> GateOutcome:
    """A claim without a source is blocked and needs a safe rewrite."""
    return GateOutcome(
        allowed=has_source,
        reason="claim_sourced" if has_source else "unsupported_claim",
        flags={
            "risk_level": "low" if has_source else "high",
            "safe_rewrite_required": not has_source,
        },
    )


def invoice_gate(*, scope_approved: bool) -> GateOutcome:
    """An invoice may not be sent without an approved scope."""
    return GateOutcome(
        allowed=scope_approved,
        reason="approved_scope" if scope_approved else "missing_approved_scope",
        flags={},
    )


def affiliate_disclosure_gate(*, has_disclosure: bool) -> GateOutcome:
    """An affiliate message without a disclosure raises a compliance flag.

    Required by FTC endorsement rules — disclosure must accompany the
    recommendation itself, not hide in an "About" page.
    """
    return GateOutcome(
        allowed=has_disclosure,
        reason="disclosure_present" if has_disclosure else "missing_disclosure",
        flags={"compliance_flag": not has_disclosure, "payout_hold": not has_disclosure},
    )


def commission_gate(*, invoice_paid: bool) -> GateOutcome:
    """No affiliate commission before the invoice is paid."""
    return GateOutcome(
        allowed=invoice_paid,
        reason="invoice_paid" if invoice_paid else "payout_before_payment_blocked",
        flags={},
    )


def revenue_record_gate(*, payment_confirmed: bool) -> GateOutcome:
    """Revenue may not be recorded without a confirmed payment."""
    return GateOutcome(
        allowed=payment_confirmed,
        reason="payment_confirmed" if payment_confirmed else "missing_payment_evidence",
        flags={},
    )


def support_escalation_gate(*, is_high_risk: bool) -> GateOutcome:
    """A high-risk support question must escalate to a human."""
    return GateOutcome(
        allowed=not is_high_risk,
        reason="routine_question" if not is_high_risk else "high_risk_escalated",
        flags={"escalated": is_high_risk},
    )


def agent_output_confidence_gate(*, has_source: bool) -> GateOutcome:
    """Agent output without a source is marked low-confidence."""
    return GateOutcome(
        allowed=has_source,
        reason="sourced_output" if has_source else "unsourced_output",
        flags={"confidence": "normal" if has_source else "low"},
    )


__all__ = [
    "DEFAULT_QUALIFIED_LEAD_THRESHOLD",
    "GateOutcome",
    "affiliate_disclosure_gate",
    "agent_output_confidence_gate",
    "claim_source_gate",
    "commission_gate",
    "invoice_gate",
    "lead_approval_gate",
    "revenue_record_gate",
    "support_escalation_gate",
]
