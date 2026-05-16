"""North-star metric — Governed Value Decisions Created — tests.

A decision counts only when it carries ALL FOUR required elements:
clear source, clear approval, documented evidence, measurable value.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_pipeline.governed_value_decisions import (
    GovernedValueDecision,
    count_governed_value_decisions,
    governed_value_decision_from_lead,
    qualifies_as_governed_value_decision,
)
from auto_client_acquisition.revenue_pipeline.lead import Lead


def _complete() -> GovernedValueDecision:
    return GovernedValueDecision(
        id="gvd_1",
        source="revenue_pipeline:slot-a",
        approval="founder_advanced",
        evidence_ref="moyasar_dashboard_2026-05-16.png",
        decision="advanced lead to 'payment_received'",
        value_sar=25000,
    )


def test_complete_decision_qualifies():
    d = _complete()
    assert d.missing_elements() == ()
    assert qualifies_as_governed_value_decision(d) is True


def test_missing_source_does_not_count():
    d = _complete().model_copy(update={"source": "   "})
    assert "source" in d.missing_elements()
    assert qualifies_as_governed_value_decision(d) is False


def test_missing_approval_does_not_count():
    d = _complete().model_copy(update={"approval": ""})
    assert "approval" in d.missing_elements()
    assert qualifies_as_governed_value_decision(d) is False


def test_missing_evidence_does_not_count():
    d = _complete().model_copy(update={"evidence_ref": ""})
    assert "evidence" in d.missing_elements()
    assert qualifies_as_governed_value_decision(d) is False


def test_missing_or_nonpositive_value_does_not_count():
    for bad_value in (None, 0, -1):
        d = _complete().model_copy(update={"value_sar": bad_value})
        assert "value" in d.missing_elements()
        assert qualifies_as_governed_value_decision(d) is False


def test_count_only_counts_qualifying_decisions():
    good = _complete()
    no_evidence = _complete().model_copy(update={"id": "gvd_2", "evidence_ref": ""})
    no_value = _complete().model_copy(update={"id": "gvd_3", "value_sar": None})
    assert count_governed_value_decisions([good, no_evidence, no_value]) == 1
    assert count_governed_value_decisions([]) == 0


def test_from_lead_returns_none_before_commitment():
    """A lead that has not reached a commitment stage is not yet a decision."""
    lead = Lead.make(slot_id="slot-a", stage="message_drafted")
    assert governed_value_decision_from_lead(lead) is None


def test_from_lead_paid_lead_qualifies():
    """A paid lead carries evidence + measurable value, so it counts."""
    lead = Lead.make(
        slot_id="slot-a",
        stage="payment_received",
        payment_evidence="bank_statement_ref",
        actual_amount_sar=25000,
    )
    decision = governed_value_decision_from_lead(lead)
    assert decision is not None
    assert qualifies_as_governed_value_decision(decision) is True


def test_from_lead_commitment_without_amount_does_not_count():
    """A written commitment with no measurable amount is not yet a value decision."""
    lead = Lead.make(
        slot_id="slot-b",
        stage="commitment_received",
        commitment_evidence="signed_intent_email_ref",
    )
    decision = governed_value_decision_from_lead(lead)
    assert decision is not None
    assert "value" in decision.missing_elements()
    assert qualifies_as_governed_value_decision(decision) is False
