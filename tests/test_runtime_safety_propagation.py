"""Runtime safety propagation tests."""

from __future__ import annotations

from auto_client_acquisition.control_plane_os import ControlPlaneRepository
from auto_client_acquisition.runtime_safety_os import RuntimeSafetyRepository


def test_kill_switch_pauses_control_plane_run() -> None:
    control = ControlPlaneRepository()
    run = control.register_run(tenant_id="tenant-a", workflow_id="wf-1", actor="ops")

    safety = RuntimeSafetyRepository()
    safety.engage_kill_switch(tenant_id="tenant-a", target_id="sales_agent", reason="manual")
    safety.propagate_kill_switch_to_control_plane(
        tenant_id="tenant-a",
        target_id="sales_agent",
        run_id=run.run_id,
        control_plane=control,
    )

    paused = control.get_run(tenant_id="tenant-a", run_id=run.run_id)
    assert paused.state == "paused"


def test_circuit_breaker_opens_after_threshold_failures() -> None:
    safety = RuntimeSafetyRepository(breaker_threshold=3)
    state1 = safety.register_failure(tenant_id="tenant-a", key="whatsapp.send_message")
    state2 = safety.register_failure(tenant_id="tenant-a", key="whatsapp.send_message")
    state3 = safety.register_failure(tenant_id="tenant-a", key="whatsapp.send_message")
    assert state1.is_open is False
    assert state2.is_open is False
    assert state3.is_open is True
