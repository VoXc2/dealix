"""Tenant isolation sweep tests for enterprise control-plane schemas."""

from __future__ import annotations

from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor, TrustBoundary
from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract
from auto_client_acquisition.control_plane_os.schemas import ControlEvent, WorkflowRun
from auto_client_acquisition.human_ai_os.schemas import Delegation, Escalation
from auto_client_acquisition.org_graph_os.schemas import GraphNode
from auto_client_acquisition.org_simulation_os.schemas import SimulationScenario
from auto_client_acquisition.runtime_safety_os.schemas import CanaryRollout
from auto_client_acquisition.sandbox_os.schemas import SandboxRun
from auto_client_acquisition.self_evolving_os.schemas import ImprovementProposal
from auto_client_acquisition.value_engine_os.schemas import WorkflowValueMetric


def test_operational_schemas_require_tenant_id() -> None:
    run = WorkflowRun(tenant_id="tenant-a", workflow_id="wf")
    event = ControlEvent(
        tenant_id="tenant-a",
        event_type="evt",
        source_module="module",
        actor="actor",
    )
    agent = AgentDescriptor(
        agent_id="agent-1",
        tenant_id="tenant-a",
        name="Agent",
        owner="Owner",
    )
    boundary = TrustBoundary(tenant_id="tenant-a", boundary_id="tb-1")
    contract = AssuranceContract(
        tenant_id="tenant-a",
        agent_id="agent-1",
        action_type="whatsapp.send_message",
    )
    sandbox = SandboxRun(tenant_id="tenant-a", run_id=run.run_id)
    graph = GraphNode(tenant_id="tenant-a", node_id="n1", node_type="agent")
    scenario = SimulationScenario(tenant_id="tenant-a", name="baseline")
    delegation = Delegation(
        tenant_id="tenant-a",
        run_id=run.run_id,
        delegated_by="founder",
        delegated_to="ops",
    )
    escalation = Escalation(
        tenant_id="tenant-a",
        run_id=run.run_id,
        reason="high_risk",
        escalated_by="ops",
    )
    metric = WorkflowValueMetric(
        tenant_id="tenant-a",
        run_id=run.run_id,
        metric_name="value",
    )
    proposal = ImprovementProposal(
        tenant_id="tenant-a",
        run_id=run.run_id,
        title="Improve process",
    )
    rollout = CanaryRollout(
        tenant_id="tenant-a",
        rollout_id="canary-1",
        target_module="agent_mesh",
    )

    assert all(
        row.tenant_id == "tenant-a"
        for row in (
            run,
            event,
            agent,
            boundary,
            contract,
            sandbox,
            graph,
            scenario,
            delegation,
            escalation,
            metric,
            proposal,
            rollout,
        )
    )
