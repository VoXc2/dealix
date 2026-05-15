"""End-to-end governed workflow test for enterprise control plane hardening."""

from __future__ import annotations

from auto_client_acquisition.agent_mesh_os.repositories import InMemoryAgentMeshRepository
from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor
from auto_client_acquisition.assurance_contract_os.repositories import (
    InMemoryAssuranceContractRepository,
)
from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract
from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.self_evolving_os.repositories import InMemorySelfEvolvingRepository
from auto_client_acquisition.value_engine_os.repositories import InMemoryValueEngineRepository


def test_revenue_os_control_plane_e2e(tmp_path, monkeypatch) -> None:
    """
    Proves one complete governed workflow:
    agent → contract → control plane → approval → value → trace → proposal gate.
    """
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    tenant_id = "tenant_demo"

    mesh = InMemoryAgentMeshRepository()
    contracts = InMemoryAssuranceContractRepository()
    control = InMemoryControlPlaneRepository()
    value_engine = InMemoryValueEngineRepository()
    self_evolving = InMemorySelfEvolvingRepository()

    # 1) register tenant-scoped sales_agent
    mesh.register_agent(
        AgentDescriptor(
            agent_id="sales_agent_1",
            tenant_id=tenant_id,
            name="sales_agent",
            owner="sami",
            capabilities=["sales"],
            trust_tier="gold",
            status="active",
            autonomy_level=2,
            tool_permissions=["whatsapp.send_message"],
            composite_score=0.95,
        )
    )
    routed = mesh.route_agent(tenant_id=tenant_id, capability="sales", max_autonomy=3)
    assert routed.agent_id == "sales_agent_1"

    # 2) register assurance contract for whatsapp.send_message
    contracts.register_contract(
        AssuranceContract(
            contract_id="ctr_1",
            tenant_id=tenant_id,
            contract_type="execution",
            agent_id="sales_agent_1",
            action_type="whatsapp.send_message",
            precondition_checks=["contactable"],
            is_external=True,
            rollback_plan="revert_message_and_notify_owner",
        )
    )

    # 3) register workflow run
    run = control.register_run(
        tenant_id=tenant_id,
        workflow_id="lead_intake",
        customer_id="cust_1",
        actor="sales_agent_1",
    )

    # 4) evaluate contract
    contract_decision = contracts.evaluate_action(
        tenant_id=tenant_id,
        agent_id="sales_agent_1",
        action_type="whatsapp.send_message",
        check_results={"contactable": True},
    )
    assert contract_decision.decision == "escalate"

    # 5) external action escalates
    runtime = decide(
        action_type="whatsapp.send_message",
        context={"risk_score": 0.8},
        actor="sales_agent_1",
    )
    assert runtime.decision == "escalate"
    assert runtime.approval_required is True

    # 6) approval ticket appears in oversight queue
    ticket = control.request_rollback(
        tenant_id=tenant_id,
        run_id=run.run_id,
        actor="sales_agent_1",
        reason="external action execution requires approval",
    )
    queue = control.list_approval_queue(tenant_id=tenant_id, state="pending")
    assert any(item.ticket_id == ticket.ticket_id for item in queue)

    # 7) approval can be granted
    control.grant_approval(tenant_id=tenant_id, ticket_id=ticket.ticket_id, actor="founder")

    # 8) value metric can be recorded with source_ref
    metric = value_engine.add_metric(
        tenant_id=tenant_id,
        run_id=run.run_id,
        metric_name="pipeline_roi",
        metric_type="measured",
        value=2500,
        source_ref="invoice#1001",
        control_repo=control,
    )
    assert metric.source_ref == "invoice#1001"

    # 9) run trace contains control events
    trace = control.trace_run(tenant_id=tenant_id, run_id=run.run_id)
    assert any(evt.event_type == "workflow.registered" for evt in trace)
    assert any(evt.event_type == "approval.granted" for evt in trace)
    assert any(evt.event_type == "value.metric_recorded" for evt in trace)

    # 10) self-evolving proposal cannot apply without approval
    proposal = self_evolving.create_proposal(
        tenant_id=tenant_id,
        title="Optimize qualifier threshold",
        summary="Adjust score cutoff to reduce false positives",
        proposed_by="sales_agent_1",
    )
    ticket_id = self_evolving.request_apply(
        tenant_id=tenant_id,
        proposal_id=proposal.proposal_id,
        actor="sales_agent_1",
        control_repo=control,
    )
    control.grant_approval(tenant_id=tenant_id, ticket_id=ticket_id, actor="founder")
    self_evolving.approve_proposal(
        tenant_id=tenant_id,
        proposal_id=proposal.proposal_id,
        approved_by="founder",
    )
    applied = self_evolving.apply_proposal(tenant_id=tenant_id, proposal_id=proposal.proposal_id)
    assert applied.state == "applied"
