"""Runtime safety kill-switch propagation tests."""

from __future__ import annotations

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.runtime_safety_os.repositories import InMemoryRuntimeSafetyRepository


def test_kill_switch_isolates_agent_and_pauses_run() -> None:
    control_plane = InMemoryControlPlaneRepository()
    run = control_plane.register_workflow_run(
        tenant_id="tenant-a",
        workflow_id="revenue-workflow",
    )
    safety = InMemoryRuntimeSafetyRepository()

    state = safety.isolate_agent_and_pause_run(
        tenant_id="tenant-a",
        agent_id="sales-agent",
        run_id=run.run_id,
        reason="circuit breaker open",
        triggered_by="ops-on-call",
        control_plane=control_plane,
    )
    assert state.isolated
    assert safety.is_agent_isolated(tenant_id="tenant-a", agent_id="sales-agent")
    assert control_plane.get_run(tenant_id="tenant-a", run_id=run.run_id).state == "paused"
    trace_types = {event.event_type for event in control_plane.trace(tenant_id="tenant-a", run_id=run.run_id)}
    assert "runtime_safety.kill_switch.activated" in trace_types
