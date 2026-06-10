"""Autonomous founder strongest ops — briefs and task selection."""

from __future__ import annotations

from dealix.commercial_ops.founder_strongest_ops import (
    build_strongest_ops_snapshot,
    select_tasks_for_mode,
    write_strongest_ops_brief,
)


def test_select_tasks_morning_non_empty() -> None:
    tasks = select_tasks_for_mode("morning")
    assert len(tasks) >= 10
    sections = {t.get("section") for t in tasks}
    assert "daily" in sections


def test_strongest_ops_snapshot_has_verdict() -> None:
    snap = build_strongest_ops_snapshot(mode="morning", run_checks=False)
    assert snap["verdict"] in ("OK", "ATTENTION", "FOCUS_PHASE_01", "LOG_EVIDENCE", "FAIL_WIRING")
    assert snap["tasks_today_count"] == len(snap.get("tasks_today") or [])
    assert snap.get("research_benchmarks_ar")


def test_write_strongest_ops_brief_paths() -> None:
    paths = write_strongest_ops_brief(mode="morning", run_checks=False)
    assert paths["markdown"].startswith("data/founder_briefs/strongest_ops_")
    assert paths["json"].endswith(".json")
