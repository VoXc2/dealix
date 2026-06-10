"""Founder weekly metrics bundle tests."""

from __future__ import annotations

from dealix.commercial_ops.founder_weekly_metrics import (
    build_founder_weekly_metrics,
    load_truth_matrix_summary,
)


def test_truth_matrix_summary_structure() -> None:
    truth = load_truth_matrix_summary()
    assert truth["exists"]
    assert isinstance(truth["red"], list)
    assert isinstance(truth["green"], list)


def test_weekly_metrics_bundle_has_sources() -> None:
    blob = build_founder_weekly_metrics()
    assert blob["iso_week"]
    assert "kpi_commercial" in blob
    assert "evidence_scorecard" in blob
    assert blob["sources"]["truth_matrix"]
