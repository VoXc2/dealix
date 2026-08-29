"""Founder weekly metrics bundle tests."""

from __future__ import annotations

import dealix.commercial_ops.founder_weekly_metrics as weekly_metrics
from dealix.commercial_ops.founder_weekly_metrics import (
    build_founder_weekly_metrics,
    load_truth_matrix_summary,
)


def test_truth_matrix_summary_structure() -> None:
    truth = load_truth_matrix_summary()
    assert truth["exists"]
    assert isinstance(truth["red"], list)
    assert isinstance(truth["blocking_red"], list)
    assert isinstance(truth["green"], list)


def test_approval_gated_live_connectors_stay_red_but_do_not_block_weekly_metrics() -> None:
    truth = load_truth_matrix_summary()
    approval_gated = {"moyasar_live", "whatsapp_business", "gmail_external"}
    assert approval_gated <= set(truth["red"])
    assert approval_gated.isdisjoint(set(truth["blocking_red"]))


def test_weekly_metrics_bundle_has_sources() -> None:
    blob = build_founder_weekly_metrics()
    assert blob["iso_week"]
    assert "kpi_commercial" in blob
    assert "evidence_scorecard" in blob
    assert blob["sources"]["truth_matrix"]


def test_non_blocking_red_truth_does_not_degrade_metrics(monkeypatch) -> None:
    monkeypatch.setattr(
        weekly_metrics,
        "load_kpi_commercial_status",
        lambda: {"pending": []},
    )
    monkeypatch.setattr(
        weekly_metrics,
        "load_truth_matrix_summary",
        lambda: {
            "exists": True,
            "red": ["gmail_external"],
            "blocking_red": [],
            "yellow": [],
            "green": [],
        },
    )
    monkeypatch.setattr(
        weekly_metrics,
        "build_weekly_scorecard",
        lambda **_: {"verdict": "NO_REAL_EVIDENCE_YET"},
    )

    blob = weekly_metrics.build_founder_weekly_metrics()
    assert blob["verdict"] == "READY"
    assert blob["blockers_ar"] == []
    assert blob["truth_matrix"]["red"] == ["gmail_external"]


def test_explicit_blocking_red_truth_still_blocks_metrics(monkeypatch) -> None:
    monkeypatch.setattr(
        weekly_metrics,
        "load_kpi_commercial_status",
        lambda: {"pending": []},
    )
    monkeypatch.setattr(
        weekly_metrics,
        "load_truth_matrix_summary",
        lambda: {
            "exists": True,
            "red": ["required_connector"],
            "blocking_red": ["required_connector"],
            "yellow": [],
            "green": [],
        },
    )
    monkeypatch.setattr(
        weekly_metrics,
        "build_weekly_scorecard",
        lambda **_: {"verdict": "OK"},
    )

    blob = weekly_metrics.build_founder_weekly_metrics()
    assert blob["verdict"] == "BLOCKED"
    assert any("required_connector" in blocker for blocker in blob["blockers_ar"])


def test_legacy_fixed_price_rows_are_not_commercial_authority() -> None:
    truth_path = weekly_metrics._truth_matrix_path()
    assert truth_path is not None
    data = weekly_metrics.yaml.safe_load(truth_path.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in data["ladder"]}

    for row_id in {
        "ops_diagnostic",
        "data_to_revenue_pack_1500",
        "growth_ops_monthly_2999",
        "support_os_addon_1500",
        "executive_command_center_7500",
    }:
        assert rows[row_id]["commercial_authority"] is False
        assert rows[row_id]["price_sar"] == "legacy_not_authorized"

    assert rows["free_mini_diagnostic"]["commercial_authority"] is True
    assert rows["free_mini_diagnostic"]["price_sar"] == "0"
    assert rows["revenue_command_pilot_30d"]["commercial_authority"] is True
    assert rows["revenue_command_pilot_30d"]["price_sar"] == "quote_after_discovery"
