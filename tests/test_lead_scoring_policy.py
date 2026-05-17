"""Lead scoring — YAML-driven heuristic matches the prior hardcoded formula.

Golden vectors are the pre-migration formula computed by hand; any drift in the
config weights or the evaluator fails here.
"""

from __future__ import annotations

import pytest

from dealix.intelligence.lead_scorer import LeadFeatures, LeadScorer


def _score(**kwargs):
    return LeadScorer().score(LeadFeatures(**kwargs))


def test_hot_golden_vector() -> None:
    # 0.20 + 0.25 + 0.20 + 0.08 + 0.04 + 0.08 + 0.15*0.9 = 0.985
    result = _score(
        company_size=100,
        budget_usd=50000,
        urgency_score=0.9,
        has_company_email=True,
        has_phone=True,
        pain_points_count=3,
        sector_fit=0.9,
    )
    assert result.score == 0.985
    assert result.tier == "hot"
    assert result.model == "heuristic"


def test_cold_zero_vector() -> None:
    result = _score()
    assert result.score == 0.0
    assert result.tier == "cold"


def test_warm_golden_vector() -> None:
    # 0.20 + 0.12 + 0.10 + 0.15*0.6 = 0.51
    result = _score(company_size=60, budget_usd=5000, urgency_score=0.5, sector_fit=0.6)
    assert result.score == 0.51
    assert result.tier == "warm"


def test_tier_thresholds_come_from_config() -> None:
    from auto_client_acquisition.policy_config import load_policy

    tiers = load_policy("lead_scoring")["tiers"]
    assert tiers == {"hot": 0.7, "warm": 0.45}


def test_clearly_warm_vector() -> None:
    # 0.20 + 0.25 + 0.10 = 0.55 -> warm
    result = _score(company_size=60, budget_usd=15000, urgency_score=0.5)
    assert result.score == 0.55
    assert result.tier == "warm"


def test_just_below_warm_is_cold() -> None:
    # 0.10 + 0.12 + 0.10 = 0.32 -> cold
    result = _score(company_size=10, budget_usd=2000, urgency_score=0.4)
    assert result.score == 0.32
    assert result.tier == "cold"


@pytest.mark.parametrize(
    ("kwargs", "needle"),
    [
        ({"company_size": 80}, "حجم"),
        ({"budget_usd": 20000}, "ميزانية"),
        ({"urgency_score": 0.8}, "عاجل"),
        ({"sector_fit": 0.9}, "قطاع"),
    ],
)
def test_reason_strings_fire_on_strong_signals(kwargs, needle) -> None:
    result = _score(**kwargs)
    assert any(needle in r for r in result.reasons)
