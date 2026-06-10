"""Motion A/B/C/D pipeline builders."""

from __future__ import annotations

from dealix.commercial_ops.motion_pipelines import (
    build_all_motions_summary,
    build_motion_pipeline_plan,
)


def test_build_motion_a_plan():
    plan = build_motion_pipeline_plan(motion="A", top_n=3)
    assert plan["motion"] == "A"
    assert plan["motion_active"] is True
    assert isinstance(plan.get("targets"), list)


def test_all_motions_summary():
    summary = build_all_motions_summary(top_n=2)
    assert summary["first_paid_verdict"] in ("CLOSED", "IN_PROGRESS", "PIPELINE_OPEN")
    assert set(summary["motions"].keys()) == {"A", "B", "C", "D"}
