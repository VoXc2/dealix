"""Tests for System 26 — control_plane_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.approval_gate import (
    get_approval_gate,
    reset_approval_gate,
)
from auto_client_acquisition.control_plane_os.core import (
    ControlPlaneError,
    get_control_plane,
    reset_control_plane,
)
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_approval_gate()
    reset_control_plane()


def test_register_and_monitor() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1", correlation_id="x1")
    status = cp.monitor(run.run_id)
    assert status.run.run_id == run.run_id
    assert status.events_count >= 1


def test_pause_resume_records_events() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    cp.pause(run.run_id, actor="founder")
    cp.resume(run.run_id, actor="founder")
    trace = cp.trace(run.run_id)
    types = {e["event_type"] for e in trace.timeline}
    # every state change is on the ledger — no_unaudited_changes
    assert "run_paused" in types
    assert "run_resumed" in types


def test_reroute_links_parent() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    child = cp.reroute(run.run_id, new_workflow_id="wf2")
    assert child.parent_run_id == run.run_id
    assert cp.get_run(run.run_id).state == "rerouted"


def test_monitor_unknown_run_raises() -> None:
    with pytest.raises(ControlPlaneError):
        get_control_plane().monitor("run_does_not_exist")


def test_rollback_then_finalize() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    ticket = cp.rollback(run.run_id, actor="founder", reason="bad data")
    get_approval_gate().grant(ticket.ticket_id, "founder")
    finalized = cp.finalize_rollback(run.run_id, ticket.ticket_id)
    assert finalized.state == "rolled_back"
