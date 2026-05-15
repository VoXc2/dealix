"""Enterprise Control Plane — end-to-end proof.

Check #10 of the verify contract. One test wires the real modules into
the full Revenue-OS control flow and proves the layers work together:

  inbound lead → tenant resolved → tenant-scoped agent registered →
  workflow run registered → agent action evaluated → high-risk action
  escalates → approval ticket appears in the tenant queue → human
  grants approval → value metric recorded with source_ref → run trace
  contains the control events → rollback request needs approval →
  self-evolving proposal cannot apply without approval.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_governance.policy import evaluate_action
from auto_client_acquisition.agent_governance.schemas import (
    AutonomyLevel,
    ToolCategory,
    ToolPermission,
)
from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    get_agent,
    register_agent,
)
from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_store import (
    clear_evidence_store_for_tests,
    record,
    run_trace,
)
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.institutional_control_os.run_registry import (
    RUN_ROLLED_BACK,
    RunRegistryError,
    clear_run_registry_for_tests,
    finalize_rollback,
    register_run,
    request_rollback,
)
from auto_client_acquisition.value_os.value_ledger import (
    add_event,
    clear_value_ledger_for_tests,
)

TENANT = "acme_co"


@pytest.fixture(autouse=True)
def _isolated():
    clear_agent_registry_for_tests()
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_value_ledger_for_tests()
    yield
    clear_agent_registry_for_tests()
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_value_ledger_for_tests()


def test_enterprise_control_plane_e2e():
    store = ApprovalStore()

    # 1. Tenant resolved + tenant-scoped sales agent registered.
    register_agent(
        AgentCard(
            agent_id="sales_agent",
            name="Sales Agent",
            owner="founder",
            purpose="route inbound Saudi B2B leads",
            autonomy_level=2,
            status="active",
            tenant_id=TENANT,
        ),
    )
    assert get_agent("sales_agent", tenant_id=TENANT) is not None
    # Tenant isolation holds.
    assert get_agent("sales_agent", tenant_id="other") is None

    # 2. Workflow run registered in the Control Plane.
    run = register_run(
        tenant_id=TENANT, workflow_id="inbound_lead", customer_id="lead_5521",
    )
    record(
        tenant_id=TENANT, evidence_type="ai_run", client_id=TENANT,
        summary="inbound lead run registered", run_id=run.run_id,
    )

    # 3. Agent action evaluated by the governance contract — an
    #    external-visible draft requires approval, never auto-executes.
    verdict = evaluate_action(
        agent_id="sales_agent",
        tool=ToolCategory.DRAFT_WHATSAPP_REPLY,
        autonomy_level=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.DRAFT_WHATSAPP_REPLY],
    )
    assert verdict.permission == ToolPermission.REQUIRES_APPROVAL

    # 4. The runtime decision escalates the high-risk external action.
    decision = decide(action="whatsapp.send_message", actor="sales_agent")
    assert decision.is_escalation
    assert decision.approval_required is True
    record(
        tenant_id=TENANT, evidence_type="governance_decision", client_id=TENANT,
        summary=f"escalate: {decision.reasons[0]}", run_id=run.run_id,
    )

    # 5. Approval ticket filed — appears in the tenant's oversight queue.
    ticket = store.create(
        ApprovalRequest(
            tenant_id=TENANT,
            object_type="outbound_message",
            object_id="msg_1",
            action_type="draft_whatsapp_manual",
            action_mode="approval_required",
            risk_level="high",
            run_id=run.run_id,
            summary_en="Outbound WhatsApp reply to inbound lead",
        ),
    )
    pending = store.list_pending(tenant_id=TENANT)
    assert any(t.approval_id == ticket.approval_id for t in pending)
    # No cross-tenant leakage.
    assert store.list_pending(tenant_id="other") == []

    # 6. Human grants the approval — the action becomes executable.
    granted = store.approve(ticket.approval_id, who="founder")
    assert ApprovalStatus(granted.status) == ApprovalStatus.APPROVED
    record(
        tenant_id=TENANT, evidence_type="approval", client_id=TENANT,
        summary="approval granted by founder", run_id=run.run_id,
    )

    # 7. Value metric recorded — measured value carries a source_ref.
    value = add_event(
        customer_id="lead_5521",
        kind="meeting_booked",
        tier="verified",
        amount=1.0,
        source_ref="crm:meeting/8842",
        tenant_id=TENANT,
    )
    assert value.is_measured is True
    record(
        tenant_id=TENANT, evidence_type="value", client_id=TENANT,
        summary="meeting booked (verified)", run_id=run.run_id,
    )

    # 8. The run trace contains every control event, tenant-scoped.
    trace = run_trace(tenant_id=TENANT, run_id=run.run_id)
    trace_types = {e.evidence_type for e in trace}
    assert {"ai_run", "governance_decision", "approval", "value"} <= trace_types

    # 9. A rollback request files an approval ticket and cannot finalize
    #    until that ticket is granted.
    rollback_ticket = request_rollback(
        run.run_id, requested_by="founder", reason="lead mis-routed",
        approval_store=store,
    )
    assert rollback_ticket.tenant_id == TENANT
    with pytest.raises(RunRegistryError, match="rollback_not_approved"):
        finalize_rollback(run.run_id, approval_store=store)
    store.approve(rollback_ticket.approval_id, who="founder")
    rolled = finalize_rollback(run.run_id, approval_store=store)
    assert rolled.state == RUN_ROLLED_BACK

    # 10. A self-evolving proposal cannot apply without approval.
    proposal = store.create(
        ApprovalRequest(
            tenant_id=TENANT,
            object_type="improvement_proposal",
            object_id="prop_e2e",
            action_type="self_improvement_apply",
            action_mode="approval_required",
            risk_level="high",
            summary_en="Apply routing-prompt improvement",
        ),
    )
    assert ApprovalStatus(proposal.status) == ApprovalStatus.PENDING
