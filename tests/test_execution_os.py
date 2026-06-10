"""Tests for execution_os."""

from __future__ import annotations

from auto_client_acquisition.execution_os import (
    CapitalReviewOutputs,
    ExecutionAntiPattern,
    ExecutionGate,
    ExpansionEntry,
    ProjectScorecard,
    all_gates_pass,
    average_project_score,
    capital_review_complete,
    detect_anti_patterns,
    evaluate_gate,
    execution_work_tier,
    expansion_path,
    recommend_decisions,
)


def test_market_pain_gate_passes() -> None:
    r = evaluate_gate(
        ExecutionGate.MARKET_PAIN,
        {
            "client_describes_pain_without_long_training": True,
            "pain_repeats_across_clients": True,
            "pain_near_money_time_or_risk": True,
        },
    )
    assert r.passed


def test_market_pain_gate_fails_missing() -> None:
    r = evaluate_gate(
        ExecutionGate.MARKET_PAIN,
        {"client_describes_pain_without_long_training": True},
    )
    assert not r.passed
    assert r.missing_keys


def test_all_gates_subset() -> None:
    ok = all_gates_pass(
        {
            int(ExecutionGate.MARKET_PAIN): {
                "client_describes_pain_without_long_training": True,
                "pain_repeats_across_clients": True,
                "pain_near_money_time_or_risk": True,
            },
        },
        gates=(ExecutionGate.MARKET_PAIN,),
    )
    assert ok


def test_execution_work_tier() -> None:
    assert execution_work_tier(frozenset()) == "stop"
    assert execution_work_tier(frozenset({"revenue"})) == "cautious"
    assert execution_work_tier(frozenset({"revenue", "proof"})) == "moderate"
    assert execution_work_tier(frozenset({"revenue", "proof", "trust"})) == "priority"


def test_project_scorecard_average() -> None:
    card = ProjectScorecard(*(50,) * 8)
    assert average_project_score(card) == 50


def test_recommend_decisions_data_quality() -> None:
    d = recommend_decisions(data_quality_score=40)
    assert d[0].decision == "DATA_READINESS_FIRST"


def test_recommend_decisions_retainer() -> None:
    d = recommend_decisions(proof_strength=90, client_health=80)
    assert any(x.decision == "RECOMMEND_RETAINER" for x in d)


def test_capital_review() -> None:
    full = CapitalReviewOutputs(True, True, True, True, True)
    assert capital_review_complete(full)
    partial = CapitalReviewOutputs(True, False, True, True, True)
    assert not capital_review_complete(partial)


def test_expansion_path() -> None:
    p = expansion_path(ExpansionEntry.REVENUE_INTELLIGENCE)
    assert p[0] == "revenue_intelligence_sprint"
    assert "client_workspace" in p


def test_anti_pattern_detection() -> None:
    hits = detect_anti_patterns(
        founder_only_critical_path=True,
        delivery_without_proof_pack=True,
    )
    kinds = {h.pattern for h in hits}
    assert ExecutionAntiPattern.FOUNDER_HERO in kinds
    assert ExecutionAntiPattern.PROOF_WEAKNESS in kinds
