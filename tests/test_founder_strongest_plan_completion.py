"""Strongest plan task completion inference."""

from __future__ import annotations

from dealix.commercial_ops.founder_strongest_plan_completion import (
    build_completion_context,
    enrich_checklist_with_completion,
    infer_task_completion,
)


def test_completion_context_keys() -> None:
    ctx = build_completion_context()
    assert "evidence_today" in ctx
    assert "weekly_decision_ok" in ctx


def test_enrich_checklist_summary() -> None:
    blob = enrich_checklist_with_completion()
    summary = blob.get("summary") or {}
    assert summary.get("total", 0) >= 100
    assert "percent_done" in summary


def test_infer_task_t08_evidence() -> None:
    ctx = {"evidence_logged_today": True, "evidence_today": 1, "weekday": 1}
    task = {"id": "t08", "section": "daily", "title_ar": "أدلة"}
    comp = infer_task_completion(task, ctx)
    assert comp["done"] is True
    assert comp["status"] == "done"
