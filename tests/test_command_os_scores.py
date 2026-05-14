"""Tests for Sovereign Command System (command_os) helpers."""

from __future__ import annotations

from auto_client_acquisition.command_os import (
    BusinessUnitMaturityBand,
    BusinessUnitMaturityInputs,
    GovernanceRiskBand,
    GovernanceRiskInputs,
    KillMarketSignals,
    KillServiceSignals,
    MarketAuthorityInputs,
    OperatingCapabilityBand,
    OperatingCapabilityInputs,
    ProofPackUseTier,
    ProofStrengthInputs,
    RedTeamVerdict,
    business_unit_maturity_band,
    compute_business_unit_maturity_score,
    compute_governance_risk_index,
    compute_market_authority_score,
    compute_operating_capability_score,
    compute_proof_strength_score,
    decision_right_for_key,
    governance_risk_band,
    kill_feature_recommended,
    kill_market_recommended,
    kill_service_recommended,
    meets_minimum_capital_creation,
    operating_capability_band,
    proof_pack_use_tier,
    red_team_verdict,
)
from auto_client_acquisition.command_os.metrics_tree import (
    NORTH_STAR_METRIC,
    SUPPORTING_METRICS,
)


def test_metrics_tree_constants() -> None:
    assert "Proof-backed" in NORTH_STAR_METRIC
    assert "proof_packs_delivered" in SUPPORTING_METRICS


def test_decision_right_lookup() -> None:
    row = decision_right_for_key("sell_service")
    assert row is not None
    assert row.gate == "Service Readiness"


def test_operating_capability() -> None:
    o = OperatingCapabilityInputs(85, 85, 85, 85, 85, 85, 85)
    s = compute_operating_capability_score(o)
    assert s >= 85
    assert operating_capability_band(s) == OperatingCapabilityBand.STRONG


def test_proof_strength_tiers() -> None:
    p = ProofStrengthInputs(90, 90, 90, 90, 90, 90)
    s = compute_proof_strength_score(p)
    assert proof_pack_use_tier(s) == ProofPackUseTier.CASE_CANDIDATE


def test_governance_risk_bands() -> None:
    g = GovernanceRiskInputs(10, 10, 10, 10, 10, 10, 10)
    assert governance_risk_band(compute_governance_risk_index(g)) == GovernanceRiskBand.LOW


def test_business_unit_maturity() -> None:
    b = BusinessUnitMaturityInputs(90, 90, 90, 90, 90, 90, 90)
    sc = compute_business_unit_maturity_score(b)
    assert business_unit_maturity_band(sc) == BusinessUnitMaturityBand.VENTURE_CANDIDATE


def test_market_authority_average() -> None:
    m = MarketAuthorityInputs(60, 60, 60, 60, 60, 60)
    assert compute_market_authority_score(m) == 60.0


def test_capital_creation_minimum() -> None:
    assert meets_minimum_capital_creation(
        trust_assets=1, product_assets=1, knowledge_assets=0, expansion_paths=1
    )
    assert not meets_minimum_capital_creation(
        trust_assets=0, product_assets=1, knowledge_assets=1, expansion_paths=1
    )


def test_red_team_reject_on_overclaim() -> None:
    assert (
        red_team_verdict(over_claim=True, real_proof=False) == RedTeamVerdict.REJECT
    )


def test_kill_service_and_feature() -> None:
    good = KillServiceSignals(
        win_rate=55,
        margin=45,
        scope_creep_index=30,
        proof_strength=80,
        retainer_path=True,
        governance_risk=20,
        repeatability=75,
    )
    assert not kill_service_recommended(good)
    assert kill_feature_recommended(
        reused=False, saves_time=True, revenue_linked=True, maintenance_drag_high=False
    )
    assert kill_feature_recommended(
        reused=True,
        saves_time=True,
        revenue_linked=True,
        maintenance_drag_high=False,
        reduces_delivery_effort=False,
    )
    assert not kill_feature_recommended(
        reused=True, saves_time=True, revenue_linked=True, maintenance_drag_high=False
    )


def test_kill_market() -> None:
    bad = KillMarketSignals(
        buyers_clear=False,
        data_risky=False,
        budget_strong=True,
        sales_cycle_months=4,
        proof_path=True,
    )
    assert kill_market_recommended(bad)
