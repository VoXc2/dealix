"""Tests for Board Decision OS scorecards, CEO decisions, and agent gate."""

from __future__ import annotations

import pytest

from auto_client_acquisition.board_decision_os import (
    band_from_total_generic,
    build_top_decisions,
    classify_initiative,
    default_capital_allocation,
    evaluate_agent_gate,
    score_client,
    score_offer,
    score_productization,
    validate_monthly_bets,
)
from auto_client_acquisition.board_decision_os.schemas import (
    AgentGateInput,
    CEOSignals,
    ClientScorecardInput,
    OfferScorecardInput,
    ProductizationScorecardInput,
    StrategicBet,
    StrategicBetsInput,
)
from auto_client_acquisition.board_decision_os.strategic_bets import StrategicBetsError


def test_offer_scorecard_scale_band() -> None:
    inp = OfferScorecardInput(
        win_rate=90,
        gross_margin=90,
        proof_strength=90,
        retainer_conversion=90,
        repeatability=90,
        governance_safety=90,
        productization_signal=90,
    )
    r = score_offer(inp)
    assert r.total >= 85
    assert r.band == "top"


def test_offer_scorecard_hold() -> None:
    inp = OfferScorecardInput(
        win_rate=40,
        gross_margin=40,
        proof_strength=40,
        retainer_conversion=40,
        repeatability=40,
        governance_safety=40,
        productization_signal=40,
    )
    r = score_offer(inp)
    assert r.total < 55
    assert r.band == "low"


def test_client_band_thresholds() -> None:
    hi = ClientScorecardInput(
        clear_pain=90,
        executive_sponsor=90,
        data_readiness=90,
        governance_alignment=90,
        adoption_score=90,
        proof_score=90,
        expansion_potential=90,
    )
    assert score_client(hi).band == "top"
    mid = ClientScorecardInput(
        clear_pain=60,
        executive_sponsor=60,
        data_readiness=60,
        governance_alignment=60,
        adoption_score=60,
        proof_score=60,
        expansion_potential=60,
    )
    assert score_client(mid).band == "mid"


def test_productization_mvp_band() -> None:
    inp = ProductizationScorecardInput(
        repeated_pain=75,
        delivery_hours_saved=75,
        revenue_linkage=75,
        risk_reduction=75,
        client_pull=75,
        build_simplicity=75,
    )
    r = score_productization(inp)
    assert 70 <= r.total < 85
    assert r.band == "strong"


def test_band_from_total_generic() -> None:
    assert band_from_total_generic(85) == "top"
    assert band_from_total_generic(70) == "strong"
    assert band_from_total_generic(55) == "mid"
    assert band_from_total_generic(54.9) == "low"


def test_ceo_top_decisions_bad_revenue_first() -> None:
    sig = CEOSignals(
        bad_revenue_unsafe_channel=True,
        proof_score=90,
        adoption_score=80,
        monthly_workflow_exists=True,
    )
    d = build_top_decisions(sig, limit=5)
    assert d[0].decision == "REJECT_BAD_REVENUE"


def test_ceo_retainer_when_no_bad_revenue() -> None:
    sig = CEOSignals(
        proof_score=85,
        adoption_score=75,
        monthly_workflow_exists=True,
        cold_whatsapp_automation_request=False,
    )
    d = build_top_decisions(sig, limit=5)
    codes = {x.decision for x in d}
    assert "OFFER_RETAINER" in codes


def test_agent_gate_rejects_high_autonomy() -> None:
    inp = AgentGateInput(
        purpose="Score accounts and draft follow-ups",
        owner="founder",
        allowed_tools=["read_crm", "llm_summarize"],
        forbidden_actions=["no_cold_whatsapp", "no_scrape_web", "no_send_messages"],
        autonomy_level=4,
        audit_required=True,
        decommission_rule="Retire if unused 90 days",
    )
    r = evaluate_agent_gate(inp)
    assert r.approved is False


def test_agent_gate_approves_mvp() -> None:
    inp = AgentGateInput(
        purpose="Summarize accounts for founder review",
        owner="founder",
        allowed_tools=["read_crm", "llm_summarize"],
        forbidden_actions=["no_cold_whatsapp", "no_scrape_web", "no_send_messages"],
        autonomy_level=2,
        audit_required=True,
        decommission_rule="Retire if unused 90 days",
    )
    r = evaluate_agent_gate(inp)
    assert r.approved is True


def test_strategic_bets_max() -> None:
    bets = [
        StrategicBet(bet_type="revenue", title="Bet A", rationale="r" * 15),
        StrategicBet(bet_type="product", title="Bet B", rationale="r" * 15),
        StrategicBet(bet_type="trust", title="Bet C", rationale="r" * 15),
        StrategicBet(bet_type="venture", title="Bet D", rationale="r" * 15),
    ]
    with pytest.raises(StrategicBetsError):
        validate_monthly_bets(StrategicBetsInput(month_label="2026-05", bets=bets))


def test_capital_catalog_contains_must_fund() -> None:
    cat = default_capital_allocation()
    assert "Governance Runtime" in cat["must_fund"]
    assert "Cold WhatsApp automation" in cat["kill"]


def test_classify_initiative() -> None:
    assert classify_initiative("We need a Scraping engine") == "kill"
    assert classify_initiative("Board Memo Generator rollout") == "must_fund"
