"""Tests for Strategy Office scoring (DCI, DTG, strategy decision)."""

from __future__ import annotations

from auto_client_acquisition.intelligence_os.benchmark_engine import (
    B2B_SERVICES_COMMON_GAPS,
    b2b_services_starting_offer_hint,
)
from auto_client_acquisition.intelligence_os.capability_index import (
    CapabilityScores,
    compute_dci,
)
from auto_client_acquisition.intelligence_os.strategy_decision import (
    StrategyDecisionBand,
    StrategySignalInputs,
    compute_strategy_decision_score,
    strategy_decision_band,
)
from auto_client_acquisition.intelligence_os.transformation_gap import (
    SprintOpportunity,
    classify_sprint_opportunity,
    transformation_gap,
)


def test_strategy_decision_lead_intel_example() -> None:
    s = StrategySignalInputs(90, 80, 90, 85, 80, 85, 85)
    score = compute_strategy_decision_score(s)
    assert score >= 85
    assert strategy_decision_band(score) == StrategyDecisionBand.SCALE


def test_strategy_decision_chatbot_example() -> None:
    s = StrategySignalInputs(50, 40, 30, 25, 45, 20, 20)
    score = compute_strategy_decision_score(s)
    assert strategy_decision_band(score) == StrategyDecisionBand.KILL


def test_dci() -> None:
    c = CapabilityScores(50, 50, 50, 50, 50, 50, 50)
    assert compute_dci(c) == 50.0


def test_transformation_gap_and_sprint() -> None:
    assert transformation_gap(32, 48) == 16.0
    assert classify_sprint_opportunity(gap=70, feasibility=80) == SprintOpportunity.BEST_SPRINT
    assert classify_sprint_opportunity(gap=70, feasibility=40) == SprintOpportunity.DIAGNOSTIC_FIRST


def test_benchmark_engine_constants() -> None:
    assert "duplicate_leads" in B2B_SERVICES_COMMON_GAPS
    assert "Lead" in b2b_services_starting_offer_hint()
