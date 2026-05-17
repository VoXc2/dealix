"""Revenue Ops Machine — A/B/C/D lead scorer."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_ops_machine.abcd_scorer import (
    ABCDSignals,
    abcd_score,
    abcd_to_funnel_state,
    classify,
    recommend_offer,
    score_form,
    signals_from_form,
)
from auto_client_acquisition.revenue_ops_machine.funnel_state import FunnelState


def test_all_positive_signals_score_15_grade_a() -> None:
    signals = ABCDSignals(
        is_decision_maker=True,
        uses_crm=True,
        has_ai_revenue_automation=True,
        is_gcc_b2b=True,
        urgency_within_30d=True,
        budget_5k_plus_sar=True,
    )
    assert abcd_score(signals) == 15
    assert classify(abcd_score(signals)) == "A"


def test_negative_weights_subtract() -> None:
    signals = ABCDSignals(
        is_decision_maker=True,  # +3
        is_student_or_jobseeker=True,  # -3
        vague_curiosity=True,  # -2
    )
    assert abcd_score(signals) == -2
    assert classify(abcd_score(signals)) == "D"


@pytest.mark.parametrize(
    "score,grade",
    [
        (15, "A"),
        (10, "A"),
        (9, "B"),
        (6, "B"),
        (5, "C"),
        (3, "C"),
        (2, "D"),
        (0, "D"),
        (-5, "D"),
    ],
)
def test_classify_thresholds(score: int, grade: str) -> None:
    assert classify(score) == grade


def test_score_10_is_grade_a_boundary() -> None:
    # decision(+3) + crm(+3) + gcc(+2) + urgency(+2) = 10
    signals = ABCDSignals(
        is_decision_maker=True,
        uses_crm=True,
        is_gcc_b2b=True,
        urgency_within_30d=True,
    )
    assert abcd_score(signals) == 10
    assert classify(abcd_score(signals)) == "A"


def test_score_9_is_grade_b_boundary() -> None:
    # decision(+3) + crm(+3) + ai(+3) = 9
    signals = ABCDSignals(
        is_decision_maker=True,
        uses_crm=True,
        has_ai_revenue_automation=True,
    )
    assert abcd_score(signals) == 9
    assert classify(abcd_score(signals)) == "B"


def test_abcd_to_funnel_state_routing() -> None:
    assert abcd_to_funnel_state("A") == FunnelState.qualified_A
    assert abcd_to_funnel_state("B") == FunnelState.qualified_B
    assert abcd_to_funnel_state("C") == FunnelState.nurture
    assert abcd_to_funnel_state("D") == FunnelState.nurture


def test_signals_from_form_infers_a_grade_lead() -> None:
    form = {
        "company": "Acme Trading Co",
        "role": "Founder",
        "current_crm": "HubSpot",
        "ai_usage": "chatbot pilot",
        "region": "Riyadh",
        "urgency": "asap",
        "budget": 6000,
    }
    result = score_form(form)
    assert result.grade == "A"
    assert result.score >= 10


def test_signals_from_form_flags_jobseeker_with_no_company() -> None:
    form = {"role": "student looking for a job", "ai_usage": "just curious"}
    signals = signals_from_form(form)
    assert signals.is_student_or_jobseeker is True
    assert signals.has_no_company is True
    assert classify(abcd_score(signals)) == "D"


def test_explicit_booleans_override_inference() -> None:
    form = {"company": "Co", "is_decision_maker": True, "budget_5k_plus_sar": True}
    signals = signals_from_form(form)
    assert signals.is_decision_maker is True
    assert signals.budget_5k_plus_sar is True


def test_recommend_offer_routes_to_existing_ladder_only() -> None:
    assert recommend_offer("A") == "revenue_proof_sprint_499"
    assert recommend_offer("B") == "free_mini_diagnostic"
    assert recommend_offer("C") == "free_mini_diagnostic"
    assert recommend_offer("D") == "free_mini_diagnostic"
