"""Founder full autopilot — queue, verdict, stage bands, PLS readiness."""

from __future__ import annotations

from dealix.commercial_ops.founder_full_autopilot import (
    analyze_customer_stage_band,
    analyze_pls_readiness,
    build_autopilot_queue,
    build_autopilot_snapshot,
    compute_autopilot_verdict,
    render_autopilot_brief_markdown,
)
from dealix.commercial_ops.full_ops_autopilot import build_full_autonomous_ops_snapshot


def test_customer_stage_band_defaults():
    stage = analyze_customer_stage_band()
    assert stage["band"] in ("1_10", "10_40", "40_plus")
    assert "focus_ar" in stage


def test_pls_readiness_structure():
    pls = analyze_pls_readiness()
    assert pls["verdict"] in ("NOT_YET", "WATCH", "READY")
    assert len(pls["signals"]) == 3


def test_autopilot_queue_non_empty():
    q = build_autopilot_queue()
    assert len(q) >= 1
    assert q[0].get("priority") == 1


def test_autopilot_verdict_levels():
    v = compute_autopilot_verdict()
    assert v["level"] in ("GREEN", "YELLOW", "RED")


def test_brief_markdown_contains_verdict():
    snap = build_autopilot_snapshot()
    md = render_autopilot_brief_markdown(snap)
    assert "Founder Full Autopilot Brief" in md
    assert (snap.get("verdict") or {}).get("level") in md


def test_full_ops_includes_founder_autopilot(monkeypatch):
    monkeypatch.setattr(
        "dealix.commercial_ops.gtm_stack.build_gtm_stack_snapshot",
        lambda **_: {"dual_track": {"recommended_track": "A", "high_priority_stale": 0}},
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.expansion_status.build_expansion_status",
        lambda **_: {"targeting": {}},
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_comprehensive_plan.build_comprehensive_status",
        lambda: {
            "daily_cadence": {"evidence_logged_today": True},
            "phase_0_1_gate": {"verdict": "BLOCKED"},
        },
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.value_plan.build_value_plan_snapshot",
        lambda **_: {"warnings_ar": []},
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_strongest_ops.build_strongest_ops_snapshot",
        lambda **_: {"mode": "morning"},
    )
    monkeypatch.setattr(
        "dealix.commercial_ops.founder_full_autopilot.build_autopilot_snapshot",
        lambda: {
            "verdict": {"level": "YELLOW", "summary_ar": "test"},
            "queue": [{"priority": 1, "title_ar": "x"}],
            "customer_stage": {"band": "1_10"},
            "pls_readiness": {"verdict": "NOT_YET"},
            "benchmark_ar": "bench",
        },
    )

    snap = build_full_autonomous_ops_snapshot(top_n=5, include_nested=False)
    fa = snap.get("founder_autopilot") or {}
    assert fa.get("verdict")
    assert "queue" in fa
    assert snap.get("schema_version") == "1.1"
