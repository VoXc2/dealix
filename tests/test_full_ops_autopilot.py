"""Full autonomous commercial ops snapshot."""

from __future__ import annotations

from dealix.commercial_ops.full_ops_autopilot import (
    RESEARCH_ALIGNMENT_AR,
    build_full_autonomous_ops_snapshot,
    run_morning_core,
)


def test_research_alignment_has_verdict() -> None:
    assert RESEARCH_ALIGNMENT_AR.get("verdict_ar")
    assert len(RESEARCH_ALIGNMENT_AR.get("external_consensus") or []) >= 3
    assert len(RESEARCH_ALIGNMENT_AR.get("sources_2026") or []) >= 2


def test_full_autonomous_snapshot_shape() -> None:
    snap = build_full_autonomous_ops_snapshot(top_n=3)
    assert snap["schema_version"] == "1.1"
    assert snap["value_plan"].get("lightweight") is True
    ar = snap["automation_readiness"]
    assert ar["verdict"] in {"AUTONOMOUS_READY", "NEEDS_FOUNDER", "BLOCKED"}
    assert "gtm_stack" in snap
    assert "comprehensive_plan" in snap
    assert snap["doc_path"].endswith("FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md")


def test_morning_core_runs_without_scripts(tmp_path, monkeypatch) -> None:
    from dealix.commercial_ops import paths

    monkeypatch.setattr(paths, "FOUNDER_BRIEFS_DIR", tmp_path)
    monkeypatch.setattr(paths, "WAR_ROOM_TODAY_JSON", tmp_path / "war_room_today.json")

    result = run_morning_core(top_n=3, run_optional_scripts=False)
    assert result["verdict"] in {"PASS", "PARTIAL", "FAIL"}
    assert len(result["steps"]) >= 4
