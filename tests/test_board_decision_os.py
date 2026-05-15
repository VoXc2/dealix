"""Tests for board_decision_os."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os import (
    AgentDecisionGate,
    BOARD_DECISION_INPUT_SIGNALS,
    BOARD_MEMO_SECTIONS,
    ClientScorecardDimensions,
    CompoundingDecision,
    OfferScorecardDimensions,
    ProductizationScorecardDimensions,
    agent_decision_gate_passes,
    board_input_signal_valid,
    board_memo_sections_complete,
    capital_board_bucket,
    ceo_command_center_coverage_score,
    client_scorecard_band,
    client_scorecard_score,
    client_scorecard_strategic_decision,
    offer_scorecard_band,
    offer_scorecard_score,
    offer_scorecard_strategic_decision,
    productization_scorecard_band,
    productization_scorecard_score,
    productization_scorecard_strategic_decision,
    risk_register_code_valid,
    risk_to_mitigation_decision,
    strategic_bet_type_valid,
    suggest_compounding_decision,
)


def test_offer_scorecard_and_strategic_decision() -> None:
    d = OfferScorecardDimensions(90, 88, 92, 88, 85, 90, 80)
    s = offer_scorecard_score(d)
    assert s >= 85
    assert offer_scorecard_band(s) == "scale"
    assert offer_scorecard_strategic_decision(s, governance_safe=True) == CompoundingDecision.SCALE
    assert offer_scorecard_strategic_decision(s, governance_safe=False) == CompoundingDecision.HOLD


def test_client_scorecard_strategic() -> None:
    c = ClientScorecardDimensions(90, 90, 85, 88, 82, 87, 80)
    sc = client_scorecard_score(c)
    assert client_scorecard_band(sc) == "strategic_account"
    assert client_scorecard_strategic_decision(sc) == CompoundingDecision.CREATE_BUSINESS_UNIT


def test_productization_scorecard() -> None:
    p = ProductizationScorecardDimensions(92, 92, 90, 85, 88, 82)
    ps = productization_scorecard_score(p)
    assert productization_scorecard_band(ps) == "build_now"
    assert productization_scorecard_strategic_decision(ps) == CompoundingDecision.BUILD


def test_suggest_compounding_delegation() -> None:
    assert (
        suggest_compounding_decision(
            pattern_occurrences=6,
            avg_proof_score=90.0,
            retainer_path_exists=True,
            governance_risk_low=True,
        )
        == CompoundingDecision.SCALE
    )


def test_agent_gate() -> None:
    ok, _ = agent_decision_gate_passes(
        AgentDecisionGate(
            True, True, True, True, True, True, True,
        ),
    )
    assert ok


def test_risk_mitigation() -> None:
    assert risk_register_code_valid("R1_agency_trap")
    assert risk_to_mitigation_decision("R1_agency_trap") == "enforce_productization_ledger"


def test_capital_board_bucket() -> None:
    assert capital_board_bucket("approval_center") == "should_test"
    assert capital_board_bucket("cold_whatsapp_automation") == "kill"
    assert capital_board_bucket("unknown_investment") is None


def test_memo_and_ceo_coverage() -> None:
    ok, missing = board_memo_sections_complete(frozenset(BOARD_MEMO_SECTIONS))
    assert ok and not missing
    assert ceo_command_center_coverage_score(frozenset()) == 0


def test_strategic_bet_type() -> None:
    assert strategic_bet_type_valid("trust_bet")
    assert not strategic_bet_type_valid("fantasy_bet")


def test_board_input_signals() -> None:
    assert len(BOARD_DECISION_INPUT_SIGNALS) == 10
    assert board_input_signal_valid("proof_signals")
    assert not board_input_signal_valid("random_signal")
