"""Revenue Autopilot lead scorer — point system + tier boundaries."""
from __future__ import annotations

from auto_client_acquisition.revenue_autopilot.lead_scorer import (
    LeadSignals,
    score_lead,
    tier_for_points,
)


def test_each_positive_rule_contributes_its_points():
    cases = {
        "is_decision_maker": 3,
        "is_b2b_company": 3,
        "has_revenue_workflow": 3,
        "uses_or_plans_ai": 3,
        "is_saudi_or_gcc": 2,
        "urgency_within_30_days": 2,
        "budget_5k_plus": 2,
    }
    for field, pts in cases.items():
        score = score_lead(LeadSignals(**{field: True}))
        assert score.points == pts, f"{field} should add {pts}"


def test_each_negative_rule_subtracts_its_points():
    cases = {
        "no_company": -3,
        "is_student_or_job_seeker": -3,
        "vague_curiosity_only": -2,
    }
    for field, pts in cases.items():
        score = score_lead(LeadSignals(**{field: True}))
        assert score.points == pts, f"{field} should subtract {abs(pts)}"


def test_full_positive_signal_set_totals_18_qualified_a():
    score = score_lead(LeadSignals(
        is_decision_maker=True, is_b2b_company=True, has_revenue_workflow=True,
        uses_or_plans_ai=True, is_saudi_or_gcc=True, urgency_within_30_days=True,
        budget_5k_plus=True,
    ))
    assert score.points == 18
    assert score.tier == "qualified_A"
    assert len(score.breakdown) == 7


def test_tier_boundaries():
    assert tier_for_points(4) == "closed_lost"
    assert tier_for_points(5) == "nurture"
    assert tier_for_points(7) == "nurture"
    assert tier_for_points(8) == "qualified_B"
    assert tier_for_points(11) == "qualified_B"
    assert tier_for_points(12) == "qualified_A"


def test_negatives_can_drop_a_lead_to_closed_lost():
    score = score_lead(LeadSignals(
        is_saudi_or_gcc=True,  # +2
        no_company=True,       # -3
        vague_curiosity_only=True,  # -2
    ))
    assert score.points == -3
    assert score.tier == "closed_lost"


def test_breakdown_is_signed_and_human_readable():
    score = score_lead(LeadSignals(is_decision_maker=True, no_company=True))
    assert "decision maker:+3" in score.breakdown
    assert "no company:-3" in score.breakdown


def test_scorer_is_deterministic():
    signals = LeadSignals(is_b2b_company=True, uses_or_plans_ai=True)
    assert score_lead(signals).points == score_lead(signals).points == 6
