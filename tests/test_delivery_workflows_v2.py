"""Wave 12.5 §33.2.3 (Engine 7) — Delivery OS workflow + artifact enforcer tests.

Validates:
- All 7 canonical workflow YAMLs load successfully
- Schema enforcement (missing keys raise WorkflowLoadError)
- Daily artifact enforcer: blocks consecutive missing days > grace_days
- Trailing-streak detection (newest gap matters most)
- Article 8 invariant: workflow with proof_target + final_deliverable

All pure-function tests — no I/O beyond reading YAMLs from disk.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

from auto_client_acquisition.delivery_factory.workflow_loader import (
    CANONICAL_WORKFLOWS,
    WorkflowDefinition,
    WorkflowLoadError,
    WorkflowStep,
    check_daily_artifacts,
    load_all_workflows,
    load_workflow,
)


# ─────────────────────────────────────────────────────────────────────
# Workflow YAML load + schema validation (6 tests)
# ─────────────────────────────────────────────────────────────────────


def test_all_7_canonical_workflows_load() -> None:
    """All 7 YAMLs must load without error."""
    workflows = load_all_workflows()
    assert len(workflows) == 7, f"expected 7 workflows; got {len(workflows)}"
    for name in CANONICAL_WORKFLOWS:
        assert name in workflows
        assert isinstance(workflows[name], WorkflowDefinition)


def test_each_workflow_has_proof_target_and_final_deliverable() -> None:
    """Article 8: every workflow MUST declare proof_target +
    final_deliverable (no 'we worked on it' deliverables)."""
    workflows = load_all_workflows()
    for name, wf in workflows.items():
        assert wf.proof_target, f"{name} missing proof_target"
        assert wf.final_deliverable, f"{name} missing final_deliverable"
        assert wf.duration_days >= 1


def test_each_workflow_step_has_owner_and_artifact_kind() -> None:
    """Every step MUST have owner + artifact_kind + next_action_kind."""
    workflows = load_all_workflows()
    for name, wf in workflows.items():
        assert wf.steps, f"{name} has no steps"
        for step in wf.steps:
            assert step.owner, f"{name}/{step.step_id} missing owner"
            assert step.artifact_kind, f"{name}/{step.step_id} missing artifact_kind"
            assert step.next_action_kind, \
                f"{name}/{step.step_id} missing next_action_kind"


def test_unknown_workflow_name_raises() -> None:
    """Loading a non-canonical workflow name → WorkflowLoadError."""
    with pytest.raises(WorkflowLoadError, match="unknown workflow"):
        load_workflow("totally_made_up_workflow")  # type: ignore[arg-type]


def test_missing_yaml_file_raises(tmp_path: Path) -> None:
    """Missing YAML file → WorkflowLoadError."""
    with pytest.raises(WorkflowLoadError, match="missing"):
        load_workflow("onboarding", base_dir=tmp_path)


def test_malformed_yaml_raises(tmp_path: Path) -> None:
    """Malformed YAML → WorkflowLoadError."""
    bad = tmp_path / "onboarding.yaml"
    bad.write_text("not: valid: yaml: : {", encoding="utf-8")
    with pytest.raises(WorkflowLoadError, match="malformed"):
        load_workflow("onboarding", base_dir=tmp_path)


# ─────────────────────────────────────────────────────────────────────
# Step-level invariants (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_diagnostic_workflow_has_arabic_message_step() -> None:
    """diagnostic.yaml must have a step that produces an Arabic message."""
    wf = load_workflow("diagnostic")
    assert any("arabic" in s.artifact_kind.lower() for s in wf.steps), \
        "diagnostic workflow must produce an Arabic message"


def test_proof_pack_workflow_has_publish_gate_step() -> None:
    """proof_pack.yaml must have a publish_gate step (Article 8)."""
    wf = load_workflow("proof_pack")
    publish_gate_steps = [s for s in wf.steps if "publish_gate" in s.step_id or "publish" in s.artifact_kind.lower()]
    assert publish_gate_steps, "proof_pack must have publish_gate enforcement"


def test_no_workflow_step_owner_is_unsafe() -> None:
    """Step owners are limited to the canonical 5: founder/csm/sales_rep/
    customer/system_auto. No 'public_robot' / 'auto_send_bot' / etc."""
    valid_owners = {"founder", "csm", "sales_rep", "customer", "system_auto"}
    workflows = load_all_workflows()
    for name, wf in workflows.items():
        for step in wf.steps:
            assert step.owner in valid_owners, \
                f"{name}/{step.step_id} has non-canonical owner={step.owner!r}"


# ─────────────────────────────────────────────────────────────────────
# Daily artifact enforcer (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_enforcer_pass_when_all_days_have_artifacts() -> None:
    """Session 5 days in with artifacts every day → not blocked."""
    today = date(2026, 5, 15)
    started = today - timedelta(days=4)  # 5 days ago (5 days elapsed)
    report = check_daily_artifacts(
        session_id="sess_001", workflow_name="lead_radar",
        started_at=started,
        recorded_artifact_days=[1, 2, 3, 4, 5],
        on_date=today, grace_days=1,
    )
    assert report.blocked is False
    assert report.missing_artifact_days == ()


def test_enforcer_blocks_consecutive_missing_above_grace() -> None:
    """3 consecutive missing days with grace=1 → blocked."""
    today = date(2026, 5, 15)
    started = today - timedelta(days=4)  # 5 days elapsed
    report = check_daily_artifacts(
        session_id="sess_002", workflow_name="lead_radar",
        started_at=started,
        recorded_artifact_days=[1, 2],  # missing 3, 4, 5
        on_date=today, grace_days=1,
    )
    assert report.blocked is True
    # Bilingual blocker reason — check actual substrings (Article 8)
    assert "بدون مخرَج" in report.blocker_reason_ar
    assert "without an artifact" in report.blocker_reason_en
    assert report.missing_artifact_days == (3, 4, 5)


def test_enforcer_grace_period_allows_single_missing_day() -> None:
    """1 missing day at end + grace=1 → not blocked yet."""
    today = date(2026, 5, 15)
    started = today - timedelta(days=2)  # 3 days elapsed
    report = check_daily_artifacts(
        session_id="sess_003", workflow_name="lead_radar",
        started_at=started,
        recorded_artifact_days=[1, 2],  # missing day 3 (today)
        on_date=today, grace_days=1,
    )
    assert report.blocked is False
    assert report.missing_artifact_days == (3,)


def test_enforcer_only_trailing_streak_counts() -> None:
    """Old missing day in middle but trailing days have artifacts → not blocked."""
    today = date(2026, 5, 15)
    started = today - timedelta(days=4)
    report = check_daily_artifacts(
        session_id="sess_004", workflow_name="lead_radar",
        started_at=started,
        recorded_artifact_days=[1, 3, 4, 5],  # missing day 2 only
        on_date=today, grace_days=1,
    )
    # Old missing day surfaces but trailing streak is 0 → NOT blocked
    assert report.blocked is False
    assert 2 in report.missing_artifact_days


def test_enforcer_returns_session_metadata() -> None:
    """Report includes session_id + workflow_name for downstream rendering."""
    today = date(2026, 5, 15)
    started = today - timedelta(days=2)
    report = check_daily_artifacts(
        session_id="sess_xyz", workflow_name="onboarding",
        started_at=started,
        recorded_artifact_days=[1, 2, 3],
        on_date=today, grace_days=1,
    )
    assert report.session_id == "sess_xyz"
    assert report.workflow_name == "onboarding"
    assert report.expected_artifacts == 3
    assert report.recorded_artifacts == 3


# ─────────────────────────────────────────────────────────────────────
# Total: 14 tests (6 schema + 3 step invariants + 5 enforcer)
# ─────────────────────────────────────────────────────────────────────
