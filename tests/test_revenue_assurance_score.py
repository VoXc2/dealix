"""Revenue Assurance Score — aggregate never inflates, never raises."""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.assurance_score import (
    CATEGORY_WEIGHTS,
    compute_assurance_score,
    readiness_label,
)


def test_weights_sum_to_100() -> None:
    assert sum(CATEGORY_WEIGHTS.values()) == 100


def test_score_never_exceeds_max() -> None:
    result = compute_assurance_score()
    assert 0 <= result["score"] <= result["max_score"] == 100


def test_live_signals_drive_score() -> None:
    full = dict.fromkeys(CATEGORY_WEIGHTS, 1.0)
    assert compute_assurance_score(full)["score"] == 100
    empty = dict.fromkeys(CATEGORY_WEIGHTS, 0.0)
    assert compute_assurance_score(empty)["score"] == 0


def test_missing_signal_is_not_fake_green() -> None:
    result = compute_assurance_score({"governance_readiness": 0.0})
    gov = next(b for b in result["breakdown"] if b["category"] == "governance_readiness")
    assert gov["achieved"] == 0
    assert "no_fake_green" in result["safety_summary"]


def test_readiness_label_thresholds() -> None:
    assert readiness_label(95) == "Assured"
    assert readiness_label(80) == "Customer-Ready with Manual Ops"
    assert readiness_label(65) == "Diagnostic Only"
    assert readiness_label(10) == "Internal Only"
