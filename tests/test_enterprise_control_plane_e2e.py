"""Enterprise Control Plane E2E governance proof."""

from __future__ import annotations

from auto_client_acquisition.agent_mesh_os import AgentDescriptor, AgentMeshRepository
from auto_client_acquisition.assurance_contract_os import (
    AssuranceContract,
    AssuranceContractRepository,
)
from auto_client_acquisition.control_plane_os import (
    ControlPlaneRepository,
    RollbackRequest,
)
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.self_evolving_os import (
    ImprovementProposal,
    SelfEvolvingRepository,
)
from auto_client_acquisition.value_engine_os import (
    ValueEngineRepository,
    WorkflowValueMetric,
)


def test_revenue_os_control_plane_e2e() -> None:
    tenant_id = "tenant-acme"

    # 1) register tenant-scoped sales agent
    mesh = AgentMeshRepository()
    mesh.register(
        AgentDescriptor(
            agent_id="sales_agent",
            tenant_id=tenant_id,
            name="Sales Agent",
            owner="founder",
            capabilities=["outreach"],
            tool_permissions=["draft", "queue_for_approval"],
            composite_score=0.92,
        ),
    )
    routed = mesh.route(tenant_id=tenant_id, capability="outreach")
    assert routed.agent_id == "sales_agent"

    # 2) register assurance contract for whatsapp.send_message
    contracts = AssuranceContractRepository()
    contracts.register(
        AssuranceContract(
            tenant_id=tenant_id,
            agent_id="sales_agent",
            action_type="whatsapp.send_message",
            precondition_checks=["has_decision_passport"],
            is_external=True,
        ),
    )

    # 3) register workflow run
    control = ControlPlaneRepository()
    run = control.register_run(
        tenant_id=tenant_id,
        workflow_id="lead_to_offer",
        customer_id="customer-1",
        actor="sales_agent",
    )

    # 4) evaluate contract
    contract_result = contracts.evaluate(
        tenant_id=tenant_id,
        agent_id="sales_agent",
        action_type="whatsapp.send_message",
        context={"has_decision_passport": True},
    )
    assert contract_result.decision == "escalate"

    # 5) external action escalates (runtime policy + contract)
    runtime = decide(action_type="whatsapp.send_message", risk_score=0.9, actor="sales_agent")
    assert runtime.approval_required is True

    # 6) approval ticket appears in oversight queue
    ticket = control.request_rollback(
        RollbackRequest(
            tenant_id=tenant_id,
            run_id=run.run_id,
            actor="sales_agent",
            reason="external_action_gate",
        ),
    )
    pending = control.pending_approvals(tenant_id=tenant_id)
    assert any(row.ticket_id == ticket.ticket_id for row in pending)

    # 7) approval can be granted
    control.grant_approval(tenant_id=tenant_id, ticket_id=ticket.ticket_id, actor="founder")

    # 8) value metric can be recorded with source_ref
    values = ValueEngineRepository()
    values.record(
        WorkflowValueMetric(
            tenant_id=tenant_id,
            run_id=run.run_id,
            metric_name="pipeline_value",
            tier="measured",
            amount=1200.0,
            source_ref="invoice#42",
        ),
    )
    report = values.roi_report(tenant_id=tenant_id, run_id=run.run_id)
    assert report["total_measured_value"] == 1200.0

    # 9) run trace contains control events
    finalized = control.finalize_rollback(
        tenant_id=tenant_id,
        run_id=run.run_id,
        ticket_id=ticket.ticket_id,
        actor="founder",
    )
    assert finalized.state == "rolled_back"
    trace = control.trace_run(tenant_id=tenant_id, run_id=run.run_id)
    event_types = {event.event_type for event in trace}
    assert {"run_registered", "rollback_requested", "approval_granted", "rollback_finalized"} <= event_types

    # 10) self-evolving proposal cannot apply without approval
    evolving = SelfEvolvingRepository()
    proposal = evolving.propose(
        ImprovementProposal(
            tenant_id=tenant_id,
            run_id=run.run_id,
            title="Adjust routing policy weights",
        ),
    )
    try:
        evolving.apply(proposal_id=proposal.proposal_id)
        raise AssertionError("proposal should require approval before apply")
    except ValueError as exc:
        assert "approval_required" in str(exc)
