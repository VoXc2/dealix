"""Runtime safety propagation tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_mesh_os.repositories import InMemoryAgentMeshRepository
from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor
from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.runtime_safety_os.repositories import InMemoryRuntimeSafetyRepository


def test_kill_switch_isolates_agent_and_pauses_run(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    control = InMemoryControlPlaneRepository()
    mesh = InMemoryAgentMeshRepository()
    safety = InMemoryRuntimeSafetyRepository()

    mesh.register_agent(
        AgentDescriptor(
            agent_id="sales_agent",
            tenant_id="tenant_a",
            name="sales_agent",
            owner="owner",
            capabilities=["sales"],
            trust_tier="gold",
            status="active",
            autonomy_level=2,
            composite_score=0.9,
        )
    )
    run = control.register_run(tenant_id="tenant_a", workflow_id="lead_flow", actor="system")
    safety.engage_kill_switch(
        tenant_id="tenant_a",
        agent_id="sales_agent",
        actor="sre",
        reason="incident",
        agent_repo=mesh,
        control_repo=control,
        run_id=run.run_id,
    )

    assert mesh.get_agent(tenant_id="tenant_a", agent_id="sales_agent").status == "isolated"
    assert control.get_run(tenant_id="tenant_a", run_id=run.run_id).state == "paused"


def test_circuit_breaker_opens_after_threshold_failures() -> None:
    safety = InMemoryRuntimeSafetyRepository()
    for _ in range(2):
        state = safety.record_failure(tenant_id="tenant_a", breaker_key="whatsapp", threshold=3)
        assert state.status == "closed"
    state = safety.record_failure(tenant_id="tenant_a", breaker_key="whatsapp", threshold=3)
    assert state.status == "open"
    assert safety.is_circuit_open(tenant_id="tenant_a", breaker_key="whatsapp") is True
