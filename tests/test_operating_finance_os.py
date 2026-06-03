"""Tests for operating_finance_os."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os import (
    CAPITAL_REVIEW_OUTPUT_KEYS,
    BadRevenueSignals,
    CapitalAllocationDimensions,
    GoodRevenueSignals,
    HireFocus,
    InvestmentBacklogEntry,
    OperatingBudgetStage,
    capital_allocation_band,
    capital_allocation_score,
    capital_review_outputs_complete,
    financial_metrics_tracking_score,
    good_revenue_green,
    investment_entry_complete,
    is_bad_revenue,
    opportunity_acceptance_ok,
    recommended_hire_focus,
    spend_allowed_for_stage,
)
from auto_client_acquisition.operating_finance_os.financial_metrics import (
    FINANCIAL_CONTROL_METRICS,
)


def test_capital_allocation_score() -> None:
    hi = CapitalAllocationDimensions(90, 90, 90, 85, 85, 88, 80, 95)
    s = capital_allocation_score(hi)
    assert s >= 85
    assert capital_allocation_band(s) == "invest_now"


def test_capital_allocation_score_proof_pack_example() -> None:
    """Worked example: strong offer with solid moat → invest_now band (≈88)."""
    proof_pack = CapitalAllocationDimensions(75, 100, 100, 67, 100, 100, 80, 100)
    assert capital_allocation_score(proof_pack) == 88
    assert capital_allocation_band(88) == "invest_now"


def test_capital_allocation_score_academy_hold() -> None:
    """Premature academy-style bet → hold_or_reject."""
    academy = CapitalAllocationDimensions(45, 40, 40, 70, 50, 50, 50, 50)
    s = capital_allocation_score(academy)
    assert s == 49
    assert capital_allocation_band(s) == "hold_or_reject"


def test_good_revenue_green() -> None:
    full = GoodRevenueSignals(
        True, True, True, True, True, True, True, True,
    )
    ok, missing = good_revenue_green(full)
    assert ok and not missing
    weak = GoodRevenueSignals(
        True, True, True, True, True, False, True, True,
    )
    ok2, missing2 = good_revenue_green(weak)
    assert not ok2
    assert "no_retainer_potential" in missing2


def test_bad_revenue() -> None:
    clean = BadRevenueSignals(
        False, False, False, False, False, False, False, False, False,
    )
    bad, reasons = is_bad_revenue(clean)
    assert not bad and not reasons
    dirty = BadRevenueSignals(
        True, True, False, False, True, False, True, True, True,
    )
    bad2, _r = is_bad_revenue(dirty)
    assert bad2


def test_opportunity_cost() -> None:
    ok, _ = opportunity_acceptance_ok(
        builds_strategic_asset=True,
        buyer_clear=True,
        proof_likely_useful=True,
        likely_annoying_revenue=True,
        playbook_potential=False,
    )
    assert ok


def test_opportunity_cost_sector_not_strategic() -> None:
    ok, blockers = opportunity_acceptance_ok(
        builds_strategic_asset=False,
        buyer_clear=True,
        proof_likely_useful=True,
        likely_annoying_revenue=False,
        playbook_potential=True,
        sector_strategic=False,
    )
    assert not ok
    assert "sector_not_strategic" in blockers


def test_capital_review() -> None:
    full = dict.fromkeys(CAPITAL_REVIEW_OUTPUT_KEYS, "x")
    assert capital_review_outputs_complete(full) == (True, ())


def test_investment_backlog() -> None:
    e = InvestmentBacklogEntry(
        investment_name="Approval Center",
        allocation_score=82,
        decision_band="build_small_mvp",
        owner="product",
        rationale="friction",
        expected_impact="retainer",
        next_condition="mvp",
    )
    assert investment_entry_complete(e)


def test_financial_metrics() -> None:
    assert financial_metrics_tracking_score(frozenset(FINANCIAL_CONTROL_METRICS)) == 100


def test_hiring_triggers() -> None:
    assert (
        recommended_hire_focus(
            founder_delivery_bottleneck=True,
            playbooks_exist=True,
            projects_repeat=True,
            manual_steps_repeat=False,
            retainers_active=False,
            enterprise_governance_load=False,
        )
        == HireFocus.DELIVERY
    )
    assert (
        recommended_hire_focus(
            founder_delivery_bottleneck=False,
            playbooks_exist=True,
            projects_repeat=True,
            manual_steps_repeat=True,
            retainers_active=False,
            enterprise_governance_load=False,
        )
        == HireFocus.PRODUCTIZATION
    )


def test_budget_stage() -> None:
    assert spend_allowed_for_stage(OperatingBudgetStage.FOUNDER_PROOF, "revenue_capture")
    assert not spend_allowed_for_stage(
        OperatingBudgetStage.FOUNDER_PROOF,
        "distribution",
    )
