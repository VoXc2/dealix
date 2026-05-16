from __future__ import annotations

from auto_client_acquisition.revenue_os.governed_value_decisions import (
    EVIDENCE_STATE_LEVEL,
    NORTH_STAR_KEY,
    can_recognize_revenue,
    is_governed_value_decision,
    validate_transition,
)


def test_north_star_key_is_governed_value_decisions() -> None:
    assert NORTH_STAR_KEY == "governed_value_decisions_created"


def test_state_levels_follow_l2_to_l7_model() -> None:
    assert EVIDENCE_STATE_LEVEL["prepared_not_sent"] == "L2"
    assert EVIDENCE_STATE_LEVEL["used_in_meeting"] == "L5"
    assert EVIDENCE_STATE_LEVEL["scope_requested"] == "L6"
    assert EVIDENCE_STATE_LEVEL["invoice_paid"] == "L7_confirmed"


def test_cannot_send_without_founder_confirmation() -> None:
    ok, reason = validate_transition(
        "prepared_not_sent",
        "sent",
        founder_confirmed=False,
        payment_received=False,
        used_in_meeting=False,
        market_pull_confirmed=False,
    )
    assert ok is False
    assert reason == "founder_confirmation_required_before_send"


def test_l6_plus_requires_meeting_usage_and_pull_signal() -> None:
    ok, reason = validate_transition(
        "scope_requested",
        "invoice_sent",
        founder_confirmed=True,
        payment_received=False,
        used_in_meeting=True,
        market_pull_confirmed=False,
    )
    assert ok is False
    assert reason == "l6_signal_required_before_invoice"

    ok, reason = validate_transition(
        "scope_requested",
        "invoice_sent",
        founder_confirmed=True,
        payment_received=False,
        used_in_meeting=True,
        market_pull_confirmed=True,
    )
    assert ok is True
    assert reason == "ok"


def test_invoice_paid_requires_payment_and_revenue_rule() -> None:
    ok, reason = validate_transition(
        "invoice_sent",
        "invoice_paid",
        founder_confirmed=True,
        payment_received=False,
        used_in_meeting=True,
        market_pull_confirmed=True,
    )
    assert ok is False
    assert reason == "payment_required_for_l7_confirmed"

    assert can_recognize_revenue(evidence_state="invoice_sent", payment_received=True) is False
    assert can_recognize_revenue(evidence_state="invoice_paid", payment_received=False) is False
    assert can_recognize_revenue(evidence_state="invoice_paid", payment_received=True) is True


def test_governed_value_decision_predicate() -> None:
    assert is_governed_value_decision(
        has_source=True,
        has_approval=True,
        has_evidence=True,
        measurable_impact=True,
    )
    assert not is_governed_value_decision(
        has_source=True,
        has_approval=True,
        has_evidence=False,
        measurable_impact=True,
    )
