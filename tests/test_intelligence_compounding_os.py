"""Smoke tests for intelligence_compounding_os — deterministic gates only."""

from __future__ import annotations

import pytest

from auto_client_acquisition.intelligence_compounding_os import (
    CompoundingDecision,
    INTELLIGENCE_DASHBOARD_SIGNALS,
    INTELLIGENCE_EVENT_STREAMS,
    INTELLIGENCE_QUALITY_CONTROLS,
    MarketSignalRecord,
    ProductIntelligenceVerdict,
    arabic_intelligence_coverage_score,
    benchmark_candidate_eligible,
    client_intelligence_coverage_score,
    data_pattern_actionable,
    governance_intelligence_coverage_score,
    intelligence_dashboard_coverage_score,
    intelligence_event_stream_valid,
    intelligence_quality_controls_met,
    market_pattern_actionable_repeats,
    market_signal_record_valid,
    pattern_confidence_band,
    product_intelligence_verdict,
    suggest_compounding_decision,
    workflow_productization_candidate,
)


def test_package_import_surface() -> None:
    assert "market" in INTELLIGENCE_EVENT_STREAMS
    assert INTELLIGENCE_DASHBOARD_SIGNALS[0] == "top_market_pains"


def test_intelligence_event_stream_valid() -> None:
    assert intelligence_event_stream_valid("governance") is True
    assert intelligence_event_stream_valid("unknown") is False


def test_market_signal_record_valid() -> None:
    ok = MarketSignalRecord(
        signal_id="MKT-001",
        source="sales_call",
        sector="B2B services",
        pain="messy leads",
        buyer="founder",
        recommended_offer="Revenue Intelligence Sprint",
        confidence="high",
    )
    assert market_signal_record_valid(ok) is True
    bad = MarketSignalRecord(
        signal_id="",
        source="sales_call",
        sector="x",
        pain="y",
        buyer="z",
        recommended_offer="o",
        confidence="c",
    )
    assert market_signal_record_valid(bad) is False


def test_market_pattern_actionable_repeats() -> None:
    assert market_pattern_actionable_repeats(2) is False
    assert market_pattern_actionable_repeats(3) is True


def test_pattern_confidence_and_data_actionable() -> None:
    assert pattern_confidence_band(1) == "low"
    assert pattern_confidence_band(3) == "medium"
    assert pattern_confidence_band(6) == "high"
    assert data_pattern_actionable(2) is False
    assert data_pattern_actionable(3) is True


def test_coverage_scores() -> None:
    assert client_intelligence_coverage_score(frozenset()) == 0
    full_client = frozenset(
        (
            "client_health_score",
            "adoption_score",
            "proof_score",
            "governance_alignment",
            "expansion_readiness",
            "data_readiness",
            "stakeholder_engagement",
        ),
    )
    assert client_intelligence_coverage_score(full_client) == 100
    assert governance_intelligence_coverage_score(frozenset({"blocked_actions"})) > 0
    assert arabic_intelligence_coverage_score(frozenset({"executive_tone"})) > 0
    assert intelligence_dashboard_coverage_score(frozenset(INTELLIGENCE_DASHBOARD_SIGNALS)) == 100


def test_workflow_productization_candidate() -> None:
    assert (
        workflow_productization_candidate(
            manual_step_repeats=3,
            hours_per_project=2.0,
            revenue_linked=True,
            risk_reducing=True,
            testable=True,
            reusable=True,
        )
        is True
    )
    assert (
        workflow_productization_candidate(
            manual_step_repeats=2,
            hours_per_project=2.0,
            revenue_linked=True,
            risk_reducing=True,
            testable=True,
            reusable=True,
        )
        is False
    )


def test_product_intelligence_verdict() -> None:
    assert (
        product_intelligence_verdict(
            usage_high=True,
            delivery_hours_saved_high=True,
            client_demand_high=True,
            governance_risk_low=True,
            maintenance_high=False,
            repetition_low=False,
        )
        == ProductIntelligenceVerdict.BUILD
    )
    assert (
        product_intelligence_verdict(
            usage_high=False,
            delivery_hours_saved_high=False,
            client_demand_high=False,
            governance_risk_low=True,
            maintenance_high=True,
            repetition_low=False,
        )
        == ProductIntelligenceVerdict.KILL
    )
    assert (
        product_intelligence_verdict(
            usage_high=True,
            delivery_hours_saved_high=True,
            client_demand_high=True,
            governance_risk_low=True,
            maintenance_high=False,
            repetition_low=True,
        )
        == ProductIntelligenceVerdict.HOLD
    )


def test_suggest_compounding_decision() -> None:
    assert suggest_compounding_decision(
        pattern_occurrences=10,
        avg_proof_score=90.0,
        retainer_path_exists=True,
        governance_risk_low=False,
    ) == CompoundingDecision.HOLD
    assert suggest_compounding_decision(
        pattern_occurrences=10,
        avg_proof_score=90.0,
        retainer_path_exists=True,
        governance_risk_low=True,
    ) == CompoundingDecision.SCALE
    assert suggest_compounding_decision(
        pattern_occurrences=4,
        avg_proof_score=85.0,
        retainer_path_exists=False,
        governance_risk_low=True,
    ) == CompoundingDecision.CREATE_PLAYBOOK
    assert suggest_compounding_decision(
        pattern_occurrences=6,
        avg_proof_score=50.0,
        retainer_path_exists=False,
        governance_risk_low=True,
    ) == CompoundingDecision.CREATE_BENCHMARK


@pytest.mark.parametrize(
    ("occurrences", "eligible"),
    (
        (5, False),
        (6, True),
    ),
)
def test_benchmark_candidate_eligible(occurrences: int, eligible: bool) -> None:
    ok, errs = benchmark_candidate_eligible(
        occurrences=occurrences,
        no_client_identifiers=True,
        no_pii=True,
        methodology_disclosed=True,
        limitations_stated=True,
    )
    assert ok is eligible
    if not eligible:
        assert "pattern_confidence_below_high" in errs


def test_intelligence_quality_controls_met() -> None:
    ok, missing = intelligence_quality_controls_met(frozenset(INTELLIGENCE_QUALITY_CONTROLS))
    assert ok is True
    assert missing == ()
    partial = frozenset(INTELLIGENCE_QUALITY_CONTROLS[:2])
    ok2, missing2 = intelligence_quality_controls_met(partial)
    assert ok2 is False
    assert len(missing2) > 0
