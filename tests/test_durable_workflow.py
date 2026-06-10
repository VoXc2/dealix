"""Smoke tests for durable workflow engine."""

from __future__ import annotations

import pytest

from auto_client_acquisition.orchestrator.durable_workflow import (
    WorkflowStatus,
    advance_workflow,
    approve_human_step,
    get_workflow,
    start_workflow,
    use_in_memory_store,
)


@pytest.fixture(autouse=True)
def _memory_store() -> None:
    use_in_memory_store(True)
    yield
    use_in_memory_store(False)


def test_start_advances_run_steps_until_human_gate() -> None:
    state = start_workflow("gtm_touch_cycle", {})
    assert state.step >= 2
    assert state.status == WorkflowStatus.NEEDS_APPROVAL.value
    assert state.human_approval_id


def test_approve_human_step_completes_workflow() -> None:
    state = start_workflow("gtm_touch_cycle", {})
    approval_id = state.human_approval_id
    assert approval_id
    done = approve_human_step(state.id, approval_id)
    assert done.status == WorkflowStatus.COMPLETED.value
    assert done.step >= 5


def test_run_step_retry_cap_fails() -> None:
    def boom(_ctx: dict) -> None:
        raise RuntimeError("step failed")

    state = start_workflow(
        "custom",
        {"step_handlers": {"only": boom}},
        steps=({"node": "run_step", "step_key": "only"},),
        max_iterations=2,
    )
    assert state.status == WorkflowStatus.FAILED.value
    assert state.retries >= 2


def test_wait_until_blocks_then_advances() -> None:
    state = start_workflow(
        "wait_test",
        {},
        steps=(
            {"node": "wait_until", "wait_seconds": 86400},
            {"node": "run_step", "step_key": "after_wait"},
        ),
    )
    assert state.status == WorkflowStatus.WAITING.value
    assert state.wait_until

    # Force elapsed wait
    loaded = get_workflow(state.id)
    loaded.wait_until = "2000-01-01T00:00:00+00:00"
    from auto_client_acquisition.orchestrator import durable_workflow as mod

    mod._persist(loaded)
    advanced = advance_workflow(state.id)
    assert advanced.step >= 1


def test_get_workflow_roundtrip() -> None:
    state = start_workflow("gtm_touch_cycle", {"foo": "bar"})
    loaded = get_workflow(state.id)
    assert loaded.id == state.id
    assert loaded.context.get("foo") == "bar"
