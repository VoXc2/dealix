"""Assurance System — scorecards, health score, no-scale conditions."""
from __future__ import annotations

from auto_client_acquisition.assurance_os.conditions import (
    evaluate_no_scale_conditions,
)
from auto_client_acquisition.assurance_os.health_score import compute_health
from auto_client_acquisition.assurance_os.models import AssuranceInputs
from auto_client_acquisition.assurance_os.scorecards import (
    MACHINE_SPECS,
    evaluate_scorecards,
)

_FULL_MATURITY = {
    "sales_autopilot": 5, "marketing_factory": 5, "support_autopilot": 5,
    "delivery_factory": 5, "partner_machine": 5, "affiliate_machine": 5,
    "approval_center": 5, "evidence_ledger": 5, "no_build_engine": 5,
    "reporting": 5,
}


def test_nine_machine_scorecards() -> None:
    cards = evaluate_scorecards(AssuranceInputs())
    assert len(cards) == len(MACHINE_SPECS) == 9
    # no maturity supplied -> unknown, never met
    assert all(c.maturity is None and not c.met for c in cards)


def test_scorecard_meets_bar() -> None:
    cards = evaluate_scorecards(AssuranceInputs(machine_maturity={"approval_center": 5}))
    ac = next(c for c in cards if c.machine == "approval_center")
    assert ac.maturity == 5 and ac.met is True


def test_scorecard_below_bar_not_met() -> None:
    cards = evaluate_scorecards(AssuranceInputs(machine_maturity={"approval_center": 4}))
    ac = next(c for c in cards if c.machine == "approval_center")
    assert ac.maturity == 4 and ac.met is False  # bar is 5


def test_health_unknown_when_no_maturity() -> None:
    health = compute_health(AssuranceInputs())
    assert health.total == 0.0
    assert len(health.unknown_components) == 7
    assert health.meets_threshold is False


def test_health_full_score_is_100() -> None:
    health = compute_health(AssuranceInputs(machine_maturity=_FULL_MATURITY))
    assert health.total == 100.0
    assert not health.unknown_components
    assert health.meets_threshold is True


def test_health_partial_data_does_not_inflate() -> None:
    """A component with unknown machines contributes None, not a guess."""
    health = compute_health(AssuranceInputs(machine_maturity={"sales_autopilot": 5}))
    assert "sales" not in health.unknown_components
    assert "marketing" in health.unknown_components
    assert health.total == 20.0  # only the sales component counted
    assert health.meets_threshold is False  # unknowns block the threshold


def test_seven_no_scale_conditions() -> None:
    health = compute_health(AssuranceInputs())
    conditions = evaluate_no_scale_conditions(AssuranceInputs(), health)
    assert len(conditions) == 7
    by_id = {c.id: c.satisfied for c in conditions}
    # high-risk auto-send is read live from the (empty) approval store, so
    # it is genuinely known to be True; every other condition is unknown.
    assert by_id["high_risk_auto_send"] is True
    assert all(
        v is None for cid, v in by_id.items() if cid != "high_risk_auto_send"
    )


def test_no_scale_conditions_satisfied_when_supplied() -> None:
    inputs = AssuranceInputs(
        machine_maturity=_FULL_MATURITY,
        evidence_completeness_pct=92,
        lead_scoring_coverage_pct=100,
        support_high_risk_escalation_pct=100,
        affiliate_payout_before_payment_count=0,
        approval_compliance_pct=100,
    )
    health = compute_health(inputs)
    conditions = evaluate_no_scale_conditions(inputs, health)
    assert all(c.satisfied is True for c in conditions)


def test_evidence_below_90_fails_condition() -> None:
    inputs = AssuranceInputs(evidence_completeness_pct=80)
    cond = next(
        c for c in evaluate_no_scale_conditions(inputs, compute_health(inputs))
        if c.id == "evidence_completeness"
    )
    assert cond.satisfied is False
