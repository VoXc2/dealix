"""Tenant isolation checks across systems 26–35 hardening modules."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_mesh_os.repositories import InMemoryAgentMeshRepository
from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor
from auto_client_acquisition.assurance_contract_os.repositories import InMemoryAssuranceContractRepository
from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract
from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.value_engine_os.repositories import InMemoryValueEngineRepository


def test_run_and_trace_are_tenant_scoped(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    repo = InMemoryControlPlaneRepository()
    run = repo.register_run(tenant_id="t1", workflow_id="lead_flow", actor="system")

    with pytest.raises(ValueError):
        repo.get_run(tenant_id="t2", run_id=run.run_id)

    assert repo.trace_run(tenant_id="t2", run_id=run.run_id) == []
    assert repo.trace_run(tenant_id="t1", run_id=run.run_id)


def test_agent_routing_enforces_tenant_boundary() -> None:
    mesh = InMemoryAgentMeshRepository()
    mesh.register_agent(
        AgentDescriptor(
            agent_id="sales_a",
            tenant_id="t1",
            name="sales",
            owner="owner",
            capabilities=["sales"],
            trust_tier="gold",
            status="active",
            autonomy_level=2,
            composite_score=0.9,
        )
    )
    mesh.register_agent(
        AgentDescriptor(
            agent_id="sales_b",
            tenant_id="t2",
            name="sales",
            owner="owner",
            capabilities=["sales"],
            trust_tier="gold",
            status="active",
            autonomy_level=2,
            composite_score=0.99,
        )
    )
    routed = mesh.route_agent(tenant_id="t1", capability="sales", max_autonomy=3)
    assert routed.agent_id == "sales_a"


def test_contract_and_value_metrics_remain_tenant_scoped(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    contracts = InMemoryAssuranceContractRepository()
    contracts.register_contract(
        AssuranceContract(
            contract_id="c1",
            tenant_id="t1",
            contract_type="execution",
            agent_id="sales_a",
            action_type="whatsapp.send_message",
            is_external=True,
        )
    )
    assert contracts.find_contract(tenant_id="t2", agent_id="sales_a", action_type="whatsapp.send_message") is None

    control = InMemoryControlPlaneRepository()
    run = control.register_run(tenant_id="t1", workflow_id="lead_flow", actor="system")
    value = InMemoryValueEngineRepository()
    value.add_metric(
        tenant_id="t1",
        run_id=run.run_id,
        metric_name="pipeline_roi",
        metric_type="measured",
        value=1200,
        source_ref="invoice#1",
    )
    assert value.list_metrics(tenant_id="t2", run_id=run.run_id) == []
