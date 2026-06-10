"""Founder daily five metrics."""

from __future__ import annotations

from scripts.founder_daily_five_metrics import build_daily_five_metrics


def test_build_daily_five_metrics_structure():
    blob = build_daily_five_metrics()
    assert "metrics" in blob
    m = blob["metrics"]
    assert "1_new_paid_revenue_events_today" in m
    assert "5_production_layers_pct" in m
    assert blob["phase_0_1_verdict"] in {"CLOSED", "IN_PROGRESS", "PIPELINE_OPEN"}
