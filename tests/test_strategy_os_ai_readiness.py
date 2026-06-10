"""Tests for strategy_os.ai_readiness."""

from __future__ import annotations

from auto_client_acquisition.strategy_os.ai_readiness import (
    RecommendedNextService,
    compute_ai_readiness,
)


def test_readiness_score_weighted() -> None:
    out = compute_ai_readiness(
        {"data": 1.0, "process": 1.0, "governance": 1.0, "people": 1.0, "tech": 1.0}
    )
    assert out["readiness_score"] == 1.0
    assert out["recommended_next_service"] == RecommendedNextService.SUPPORT_DESK_SPRINT.value


def test_low_data_recommends_lead_intelligence() -> None:
    out = compute_ai_readiness(
        {"data": 0.2, "process": 0.8, "governance": 0.8, "people": 0.5, "tech": 0.5}
    )
    assert out["recommended_next_service"] == RecommendedNextService.LEAD_INTELLIGENCE_SPRINT.value


def test_low_process_recommends_quick_win() -> None:
    out = compute_ai_readiness(
        {"data": 0.8, "process": 0.2, "governance": 0.8, "people": 0.5, "tech": 0.5}
    )
    assert out["recommended_next_service"] == RecommendedNextService.QUICK_WIN_OPS.value
