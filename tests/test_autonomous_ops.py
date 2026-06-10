"""Governed full autonomous ops status and benchmark."""

from __future__ import annotations

from dealix.commercial_ops.autonomous_ops import (
    BENCHMARK_COMPARISON_AR,
    build_autonomous_ops_status,
    render_autonomous_ops_markdown,
    save_last_autonomous_run,
)


def test_autonomous_ops_status_shape():
    blob = build_autonomous_ops_status()
    assert blob["mode"] == "governed_autonomous_max"
    assert len(blob["benchmark_comparison_ar"]) >= 4
    assert blob.get("technical_expansion_ready") in (True, False)
    assert "expansion" in blob
    assert blob["ops_ui"]["approvals"] == "/ar/ops/approvals"


def test_save_and_render_autonomous_report():
    payload = {
        "date": "2026-05-18",
        "policy_ar": "test",
        "verdict": "PASS",
        "generated_at": "2026-05-18T00:00:00+00:00",
        "benchmark_comparison_ar": BENCHMARK_COMPARISON_AR[:2],
        "human_only_ar": ["يدوي"],
        "phases": [{"id": "expand", "label": "x", "exit_code": 0, "verdict": "OK"}],
    }
    save_last_autonomous_run(payload)
    md = render_autonomous_ops_markdown(payload)
    assert "Autonomous Ops Report" in md
    assert "مقارنة" in md
