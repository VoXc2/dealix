"""No-Build Gate — build must earn the right; default is sell/deliver."""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.no_build_gate import no_build_decision


def test_nothing_justified_means_no_build() -> None:
    decision = no_build_decision()
    assert decision.should_build is False
    assert decision.directive == "SELL_DELIVER_MEASURE_LEARN"
    assert decision.reasons == ()


def test_customer_request_justifies_build() -> None:
    decision = no_build_decision(customer_requested=True)
    assert decision.should_build is True
    assert "customer_requested" in decision.reasons


def test_workflow_repeat_threshold() -> None:
    assert no_build_decision(workflow_repeat_count=2).should_build is False
    assert no_build_decision(workflow_repeat_count=3).should_build is True


def test_each_condition_independently_justifies_build() -> None:
    assert no_build_decision(reduces_real_risk=True).should_build is True
    assert no_build_decision(speeds_paid_delivery=True).should_build is True
    assert no_build_decision(opens_retainer=True).should_build is True
