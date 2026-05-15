"""Strategy OS — use case scoring."""

from __future__ import annotations

import pytest

from auto_client_acquisition.strategy_os import (
    UseCaseScores,
    composite_score,
    rank_use_cases,
    roadmap_buckets,
)


def test_composite_score_weights_order() -> None:
    high = UseCaseScores(
        name="A",
        revenue_impact=1.0,
        time_save=0.0,
        data_readiness=0.0,
        ease=0.0,
        low_risk=0.0,
    )
    low = UseCaseScores(
        name="B",
        revenue_impact=0.0,
        time_save=0.0,
        data_readiness=0.0,
        ease=0.0,
        low_risk=1.0,
    )
    assert composite_score(high) > composite_score(low)


def test_rank_use_cases_descending() -> None:
    cases = [
        UseCaseScores("low", 0.2, 0.2, 0.2, 0.2, 0.2),
        UseCaseScores("high", 0.9, 0.9, 0.9, 0.9, 0.9),
    ]
    r = rank_use_cases(cases)
    assert r[0][0] == "high"


def test_roadmap_buckets_splits_nine() -> None:
    names = [f"u{i}" for i in range(9)]
    b = roadmap_buckets(names)
    assert len(b["days_30"]) == 3 and len(b["days_60"]) == 3 and len(b["days_90"]) == 3


def test_scores_must_be_in_unit_interval() -> None:
    with pytest.raises(ValueError, match="revenue_impact_out_of_range"):
        UseCaseScores("x", 1.5, 0, 0, 0, 0)
