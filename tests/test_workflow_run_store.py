"""Tests for the workflow_os_v10 run store abstraction.

Pure unit tests — no network, no LLM, no DB. The Postgres backend
(``pg_run_store``) is exercised via the lossless checkpoint round-trip
that it relies on, without requiring a live database.
"""

from __future__ import annotations

from auto_client_acquisition.workflow_os_v10 import (
    MINI_DIAGNOSTIC,
    InMemoryWorkflowRunStore,
    _reset_workflow_buffer,
    advance_workflow,
    get_run,
    get_run_store,
    register_definition,
    reset_run_store,
    restore_checkpoint,
    save_checkpoint,
    set_run_store,
    start_workflow,
)

# ════════════════════ InMemoryWorkflowRunStore ════════════════════


def test_in_memory_store_save_get_delete():
    store = InMemoryWorkflowRunStore()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="alpha")
    store.save(run)
    assert store.get(run.run_id) is run
    assert run.run_id in store.list_ids()
    store.delete(run.run_id)
    assert store.get(run.run_id) is None


def test_in_memory_store_get_unknown_id_returns_none():
    store = InMemoryWorkflowRunStore()
    assert store.get("run_does_not_exist") is None


def test_in_memory_store_clear_removes_all_runs():
    store = InMemoryWorkflowRunStore()
    register_definition(MINI_DIAGNOSTIC)
    store.save(start_workflow(MINI_DIAGNOSTIC, customer_handle="a"))
    store.save(start_workflow(MINI_DIAGNOSTIC, customer_handle="b"))
    assert len(store.list_ids()) == 2
    store.clear()
    assert store.list_ids() == []


# ════════════════════ State machine ↔ active store ════════════════════


def test_state_machine_persists_run_through_active_store():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="bravo")
    # start_workflow must persist the run into the active store.
    assert get_run(run.run_id).run_id == run.run_id

    run = advance_workflow(run, "intake_payload_parse", "k1", {"v": 1})
    # advance_workflow must persist the mutated run.
    stored = get_run(run.run_id)
    assert stored.state == run.state
    assert len(stored.step_history) == 1


def test_reset_run_store_clears_persisted_runs():
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="charlie")
    assert get_run_store().get(run.run_id) is not None
    reset_run_store()
    assert get_run_store().get(run.run_id) is None


def test_set_run_store_swaps_backend():
    original = get_run_store()
    try:
        custom = InMemoryWorkflowRunStore()
        set_run_store(custom)
        assert get_run_store() is custom
        register_definition(MINI_DIAGNOSTIC)
        run = start_workflow(MINI_DIAGNOSTIC, customer_handle="delta")
        assert custom.get(run.run_id) is run
    finally:
        set_run_store(original)
        reset_run_store()


# ════════════════════ Durable round-trip (pg_run_store contract) ════


def test_run_survives_serialized_round_trip_via_store():
    """A run dropped from memory can be rehydrated from its checkpoint.

    This is exactly what pg_run_store does: save_checkpoint → JSONB →
    restore_checkpoint.
    """
    _reset_workflow_buffer()
    register_definition(MINI_DIAGNOSTIC)
    run = start_workflow(MINI_DIAGNOSTIC, customer_handle="echo")
    run = advance_workflow(run, "intake_payload_parse", "k1", {"v": 1})

    snapshot = save_checkpoint(run)
    reset_run_store()  # simulate a process restart — memory is gone
    assert get_run_store().get(run.run_id) is None

    restored = restore_checkpoint(snapshot)
    get_run_store().save(restored)

    rehydrated = get_run(run.run_id)
    assert rehydrated.run_id == run.run_id
    assert rehydrated.workflow_id == run.workflow_id
    assert rehydrated.state == run.state
    assert len(rehydrated.step_history) == 1
    assert "k1" in rehydrated.idempotency_keys_seen
