"""Founder strongest plan checklist and doc wiring."""

from __future__ import annotations

from pathlib import Path

from dealix.commercial_ops.founder_strongest_plan import (
    load_strongest_plan_checklist,
    strongest_plan_snapshot,
    strongest_plan_status,
)

REPO = Path(__file__).resolve().parents[1]


def test_strongest_plan_status_pass() -> None:
    st = strongest_plan_status()
    min_expected = int(st.get("min_task_count") or 50)
    assert min_expected >= 50
    assert st["ok"] is True
    assert st["task_count"] >= min_expected
    assert st["phase_count"] == 6
    assert st["section_count"] >= 16
    assert st["missing_paths"] == []
    assert st["version"] == "2"


def test_checklist_has_core_tasks() -> None:
    data = load_strongest_plan_checklist()
    tasks = [t for t in data.get("tasks") or [] if isinstance(t, dict)]
    ids = {t["id"] for t in tasks}
    min_expected = int(data.get("min_task_count") or 50)
    assert min_expected >= 50
    assert "t01" in ids
    assert "t28" in ids
    assert "t50" in ids
    assert "t108" in ids
    assert "t122" in ids
    assert "t134" in ids
    assert "t138" in ids
    assert len(ids) == len(tasks)
    assert len(ids) >= min_expected
    assert (REPO / "docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md").is_file()


def test_weekly_one_decision_template() -> None:
    p = REPO / "dealix/config/founder_weekly_one_decision.yaml"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "active_phase" in text
    assert "one_decision_ar" in text


def test_strongest_plan_snapshot_groups_tasks() -> None:
    snap = strongest_plan_snapshot()
    sections = snap.get("sections") or []
    total = sum(len(s.get("tasks") or []) for s in sections)
    expected = snap["status"]["task_count"]
    assert total == expected
    assert expected >= 50
    assert snap["status"]["ok"] is True
    section_ids = {s["id"] for s in sections}
    assert "presentations" in section_ids
    assert "dogfood" in section_ids
    assert "autonomous_ops" in section_ids
    assert "integrations" in section_ids
    assert "finance_unit" in section_ids
    assert "research" in section_ids
    bridge = snap.get("full_ops_bridge")
    assert bridge is None or isinstance(bridge, dict)
    completion = snap.get("completion")
    assert completion is None or isinstance(completion, dict)
