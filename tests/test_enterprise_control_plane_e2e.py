"""End-to-end enterprise control plane workflow test."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_mesh_os.repositories import (
    AgentDescriptor,
    InMemoryAgentMeshRepository,
    TrustBoundary,
)
from auto_client_acquisition.assurance_contract_os.repositories import (
    AssuranceContract,
    InMemoryAssuranceContractRepository,
)
from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.runtime_safety_os.repositories import InMemoryRuntimeSafetyRepository
from auto_client_acquisition.self_evolving_os.repositories import (
    ImprovementProposal,
    InMemorySelfEvolvingRepository,
    ProposalApprovalRequiredError,
)
from auto_client_acquisition.value_engine_os.repositories import (
    InMemoryValueEngineRepository,
    WorkflowValueMetric,
)


def test_enterprise_control_plane_e2e() -> None:
    tenant_id = "tenant-enterprise"
    control_plane = InMemoryControlPlaneRepository()
    agent_mesh = InMemoryAgentMeshRepository()
    contracts = InMemoryAssuranceContractRepository()
    runtime_safety = InMemoryRuntimeSafetyRepository()
    value_engine = InMemoryValueEngineRepository()
    self_evolving = InMemorySelfEvolvingRepository()

    # 1) register tenant-scoped sales agent
    agent_mesh.set_trust_boundary(
        TrustBoundary(
            boundary_id="trust-1",
            tenant_id=tenant_id,
            scope="sales",
            max_autonomy_level=2,
        )
    )
    agent_mesh.register_agent(
        AgentDescriptor(
            agent_id="sales_agent",
            tenant_id=tenant_id,
            name="Sales Agent",
            owner="revops",
            capabilities=("outbound_sales",),
            trust_tier="high",
            status="active",
            autonomy_level=2,
            composite_score=0.97,
        )
    )

    # 2) register assurance contract
    contracts.register_contract(
        AssuranceContract(
            contract_id="ctr-whatsapp",
            tenant_id=tenant_id,
            action_type="whatsapp.send_message",
            external_action=True,
            irreversible_action=True,
            rollback_plan_required=True,
        )
    )

    # 3) register workflow run
    run = control_plane.register_workflow_run(
        tenant_id=tenant_id,
        workflow_id="revenue_os_control_plane_e2e",
        customer_id="cust-123",
    )

    # 4) route agent
    routed = agent_mesh.route_agent(tenant_id=tenant_id, capability="outbound_sales")
    assert routed is not None and routed.agent_id == "sales_agent"

    # 5) evaluate contract → external action escalates
    contract_decision = contracts.evaluate_action(
        tenant_id=tenant_id,
        action_type="whatsapp.send_message",
        external_action=True,
        irreversible_action=True,
        rollback_plan="fallback_to_draft_only",
    )
    assert contract_decision.decision == "escalate"

    # 6) approval appears in oversight queue
    approval = control_plane.request_approval(
        tenant_id=tenant_id,
        action_type="whatsapp.send_message",
        description="External WhatsApp send for inbound lead follow-up.",
        requested_by="sales_agent",
        source_module="agent_mesh",
        run_id=run.run_id,
        subject_type="agent_action",
        subject_id="whatsapp.send_message",
    )
    queue = control_plane.list_oversight_queue(tenant_id=tenant_id)
    assert len(queue) == 1 and queue[0].ticket_id == approval.ticket_id

    # 7) approval can be granted
    control_plane.grant_approval(
        tenant_id=tenant_id,
        ticket_id=approval.ticket_id,
        granted_by="sami",
        reason="warm inbound context validated",
    )
    assert control_plane.get_ticket(tenant_id=tenant_id, ticket_id=approval.ticket_id).state == "granted"

    # 8) runtime safety check
    runtime_safety.activate_kill_switch(
        tenant_id=tenant_id,
        agent_id="sales_agent_shadow",
        reason="sandbox validation",
        triggered_by="safety-bot",
    )
    assert runtime_safety.is_agent_isolated(tenant_id=tenant_id, agent_id="sales_agent_shadow")

    # 9) value metric measured with source_ref
    value_engine.record_metric(
        WorkflowValueMetric(
            metric_id="val-1",
            tenant_id=tenant_id,
            run_id=run.run_id,
            metric_name="pipeline_revenue_realized",
            metric_kind="measured",
            value=4500.0,
            source_ref="invoice:INV-4500",
        )
    )
    summary = value_engine.roi_summary(tenant_id=tenant_id)
    assert summary["measured_total"] == 4500.0

    # 10) trace contains control events
    control_plane.append_event(
        tenant_id=tenant_id,
        event_type="workflow.action.executed",
        source_module="agent_mesh",
        actor="sales_agent",
        run_id=run.run_id,
        decision="executed",
        payload={"action_type": "whatsapp.send_message"},
    )
    trace_types = {event.event_type for event in control_plane.trace(tenant_id=tenant_id, run_id=run.run_id)}
    assert {"approval.submitted", "approval.granted", "workflow.action.executed"} <= trace_types

    # 11) rollback request requires approval
    rollback_ticket = control_plane.request_rollback(
        tenant_id=tenant_id,
        run_id=run.run_id,
        requested_by="ops",
        reason="operator rollback request",
    )
    assert rollback_ticket.state == "pending"

    # 12) self-evolving proposal cannot apply without approval
    self_evolving.submit_proposal(
        ImprovementProposal(
            proposal_id="proposal-1",
            tenant_id=tenant_id,
            title="Adjust routing score weights",
            change_summary="Increase trust_tier weight.",
            proposed_by="system",
        )
    )
    with pytest.raises(ProposalApprovalRequiredError):
        self_evolving.apply_proposal(
            tenant_id=tenant_id,
            proposal_id="proposal-1",
            applied_by="system",
        )
