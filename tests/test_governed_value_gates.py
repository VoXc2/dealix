"""The 7-gate proof-before-scale map."""

from __future__ import annotations

from auto_client_acquisition.governed_value_os.gate_map import GATES, evaluate_gates


def test_seven_gates_defined() -> None:
    assert len(GATES) == 7
    assert [g.number for g in GATES] == [1, 2, 3, 4, 5, 6, 7]
    for g in GATES:
        assert g.name_ar and g.name_en
        assert g.criterion_ar and g.criterion_en


def test_no_signals_passes_nothing() -> None:
    gates = evaluate_gates()
    assert all(not g["passed"] for g in gates)


def test_gate1_first_market_proof() -> None:
    gates = evaluate_gates(messages_sent=5, classified_replies=1)
    assert gates[0]["passed"] is True
    # 5 sent but no classified reply yet → not passed.
    gates = evaluate_gates(messages_sent=5, classified_replies=0)
    assert gates[0]["passed"] is False


def test_gate4_revenue_proof_needs_invoice_paid() -> None:
    gates = evaluate_gates(invoice_paid=1)
    assert gates[3]["passed"] is True


def test_gate6_retainer_needs_paid_and_repeat() -> None:
    gates = evaluate_gates(invoice_paid=1, offer_sold_twice=False)
    assert gates[5]["passed"] is False
    gates = evaluate_gates(invoice_paid=1, offer_sold_twice=True)
    assert gates[5]["passed"] is True


def test_gate7_platform_signal_needs_three_repeats() -> None:
    assert evaluate_gates(repeated_workflows=2)[6]["passed"] is False
    assert evaluate_gates(repeated_workflows=3)[6]["passed"] is True


def test_all_gates_pass_with_full_signals() -> None:
    gates = evaluate_gates(
        messages_sent=10,
        classified_replies=4,
        used_in_meeting=2,
        scope_requested=2,
        invoice_paid=2,
        offer_sold_twice=True,
        repeated_workflows=3,
    )
    assert all(g["passed"] for g in gates)
