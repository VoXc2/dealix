"""Founder integration truth matrix — YAML loader."""

from __future__ import annotations

from dealix.business_now.commercial_strategy import build_commercial_strategy_snapshot
from dealix.business_now.integration_truth import build_integration_truth_summary


def test_integration_truth_summary_structure() -> None:
    s = build_integration_truth_summary()
    assert s["overall_status"] in ("green", "yellow", "red")
    assert "counts" in s
    assert len(s.get("ladder") or []) >= 5
    assert len(s.get("integrations") or []) >= 3


def test_integration_truth_in_commercial_strategy() -> None:
    snap = build_commercial_strategy_snapshot(
        commercial_kpi_pending=0,
        transformation_verdict="PASS",
        all_pilots_template_ready=False,
    )
    truth = snap.get("integration_truth_summary") or {}
    assert truth.get("overall_status")
    assert truth.get("doc_matrix")
