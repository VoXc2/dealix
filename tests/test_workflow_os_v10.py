"""Tests for the workflow_os_v10 state machine.

Pure unit + ASGI tests — no network, no LLM, no DB. Each <2s.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.workflow_os_v10 import (
    ALLOWED_TRANSITIONS,
    GROWTH_STARTER_7_DAY,
    MINI_DIAGNOSTIC,
    PROOF_PACK_ASSEMBLY,
    RetryPolicy,
    WorkflowRun,
    _reset_workflow_buffer,
    advance_workflow,
    compute_next_retry,
    is_duplicate,
    register_definition,
    restore_checkpoint,
    save_checkpoint,
    start_workflow,
)


# ════════════════════ Schemas + transitions ════════════════════


def test_all_workflow_states_present_in_allowed_transitions():
    expected = {
        "pending",
        "running",
        "paused_for_approval",
        "completed",
        "blocked",
        "failed",
        "retrying",
    }
    assert set(ALLOWED_TRANSITIONS) == expected


def test_terminal_states_have_no_or_minimal_outgoing():
    # blocked + completed are terminal
    assert ALLOWED_TRANSITIONS["blocked"] == set()
    assert ALLOWED_TRANSITIONS["completed"] == set()


def test_pending_can_only_transition_to_running_or_blocked():
    assert ALLOWED_TRANSITIONS["pending"] == {"running", "blocked"}


# ════════════════════ Idempotency ════════════════════


def test_same_idempotency_key_replayed_is_noop():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="alpha")
    run = advance_workflow(
        run,
        step_name="intake_payload_parse",
        idempotency_key="key-A",
        result={"ok": True},
    )
    history_len_after_first = len(run.step_history)

    # Replay 5 times with the SAME key — should be a no-op every time.
    for _ in range(5):
        run = advance_workflow(
            run,
            step_name="intake_payload_parse",
            idempotency_key="key-A",
            result={"ok": "second-effect"},
        )
    assert len(run.step_history) == history_len_after_first
    # Result must reflect the FIRST call only.
    assert run.step_history[0].result == {"ok": True}
    assert is_duplicate(run, "key-A") is True


def test_different_idempotency_keys_each_run_once():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="bravo")
    run = advance_workflow(run, "intake_payload_parse", "k1", {"x": 1})
    run = advance_workflow(run, "icp_match_score", "k2", {"x": 2})
    assert len(run.step_history) == 2


# ════════════════════ Retry policy ════════════════════


def test_compute_next_retry_exponential_backoff():
    policy = RetryPolicy(max_retries=3, backoff_factor=2.0, initial_delay_seconds=60)
    # attempt=0 → 60 * 2**0 = 60
    assert compute_next_retry(0, policy) == 60
    # attempt=1 → 60 * 2 = 120
    assert compute_next_retry(1, policy) == 120
    # attempt=2 → 60 * 4 = 240
    assert compute_next_retry(2, policy) == 240


def test_workflow_exhausts_retries_marks_failed():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="charlie")
    policy = RetryPolicy(max_retries=2, backoff_factor=2.0, initial_delay_seconds=10)
    # First failed attempt → retrying
    run = advance_workflow(
        run,
        "intake_payload_parse",
        "k-fail-1",
        policy=policy,
        simulate_failure=True,
    )
    assert run.state == "retrying"
    # Second failed attempt → exhausted → failed
    run = advance_workflow(
        run,
        "intake_payload_parse",
        "k-fail-2",
        policy=policy,
        simulate_failure=True,
    )
    assert run.state == "failed"


# ════════════════════ Disallowed transitions ════════════════════


def test_disallowed_transition_raises_or_blocks():
    """Forcing a completed run back to running must raise."""
    from auto_client_acquisition.workflow_os_v10.state_machine import (
        _transition_state,
    )

    run = WorkflowRun(workflow_id="wf_test", state="completed")
    with pytest.raises(ValueError):
        _transition_state(run, "running")


# ════════════════════ Checkpoint roundtrip ════════════════════


def test_checkpoint_roundtrip_preserves_run_state():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="delta")
    run = advance_workflow(run, "intake_payload_parse", "k1", {"v": 1})
    snapshot = save_checkpoint(run)
    restored = restore_checkpoint(snapshot)
    assert restored.run_id == run.run_id
    assert restored.workflow_id == run.workflow_id
    assert restored.customer_handle == run.customer_handle
    assert restored.state == run.state
    assert len(restored.step_history) == len(run.step_history)
    assert "k1" in restored.idempotency_keys_seen


# ════════════════════ Pre-defined definitions ════════════════════


def test_growth_starter_workflow_has_at_least_seven_steps():
    assert len(GROWTH_STARTER_7_DAY.steps) >= 7


def test_proof_pack_workflow_defined():
    assert PROOF_PACK_ASSEMBLY.name == "proof_pack_assembly"
    assert len(PROOF_PACK_ASSEMBLY.steps) >= 3


def test_mini_diagnostic_defined():
    assert MINI_DIAGNOSTIC.name == "mini_diagnostic"
    assert len(MINI_DIAGNOSTIC.steps) >= 3


# ════════════════════ API endpoints ════════════════════


@pytest.mark.asyncio
async def test_status_endpoint_advertises_canonical_guardrails():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/workflow-os-v10/status")
    assert r.status_code == 200
    body = r.json()
    assert body["module"] == "workflow_os_v10"
    g = body["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_live_charge"] is True
    assert g["idempotency_enforced"] is True
    assert g["retry_budget_enforced"] is True
    assert g["checkpoint_supported"] is True


@pytest.mark.asyncio
async def test_definitions_endpoint_returns_predefined_workflows():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/workflow-os-v10/definitions")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 3
    names = {d["name"] for d in body["definitions"]}
    assert "growth_starter_7_day" in names
    assert "proof_pack_assembly" in names
    assert "mini_diagnostic" in names


@pytest.mark.asyncio
async def test_start_endpoint_with_valid_body_returns_200():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/workflow-os-v10/start",
            json={
                "workflow_id": MINI_DIAGNOSTIC.workflow_id,
                "customer_handle": "echo-handle",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["workflow_id"] == MINI_DIAGNOSTIC.workflow_id
    assert body["state"] == "pending"


@pytest.mark.asyncio
async def test_start_with_empty_workflow_id_returns_422():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/workflow-os-v10/start",
            json={"workflow_id": "", "customer_handle": "x"},
        )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_advance_with_duplicate_idempotency_key_is_noop():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. start a run
        r = await client.post(
            "/api/v1/workflow-os-v10/start",
            json={
                "workflow_id": MINI_DIAGNOSTIC.workflow_id,
                "customer_handle": "foxtrot",
            },
        )
        run_id = r.json()["run_id"]

        # 2. advance once
        r1 = await client.post(
            f"/api/v1/workflow-os-v10/{run_id}/advance",
            json={
                "step_name": "intake_payload_parse",
                "idempotency_key": "dup-key",
                "result": {"first": True},
            },
        )
        assert r1.status_code == 200
        len_after_1 = len(r1.json()["step_history"])

        # 3. replay with same key
        r2 = await client.post(
            f"/api/v1/workflow-os-v10/{run_id}/advance",
            json={
                "step_name": "intake_payload_parse",
                "idempotency_key": "dup-key",
                "result": {"second": True},
            },
        )
        assert r2.status_code == 200
        len_after_2 = len(r2.json()["step_history"])

    assert len_after_1 == len_after_2  # no-op replay
