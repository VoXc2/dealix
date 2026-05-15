"""End-to-end governed workflow proof (tenant-scoped, approval-first)."""

from __future__ import annotations

from auto_client_acquisition.agent_os import (
    AgentCard,
    clear_agent_registry_for_tests,
    get_agent,
    register_agent,
)
from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest, ApprovalStatus
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)
from auto_client_acquisition.auditability_os.audit_event import (
    clear_for_test as clear_audit_for_test,
)
from auto_client_acquisition.auditability_os.audit_event import (
    list_events as list_audit_events,
)
from auto_client_acquisition.auditability_os.evidence_chain import build_chain
from auto_client_acquisition.governance_os.runtime_decision import decide
from auto_client_acquisition.value_os.value_ledger import (
    add_event as add_value_event,
)
from auto_client_acquisition.value_os.value_ledger import (
    clear_for_test as clear_value_for_test,
)
from auto_client_acquisition.value_os.value_ledger import (
    list_events as list_value_events,
)


def test_revenue_os_governed_workflow_end_to_end(tmp_path, monkeypatch) -> None:
    tenant_id = "tenant_acme"
    customer_id = "acme"
    run_id = "run_demo_001"

    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    clear_audit_for_test()
    clear_value_for_test()
    clear_agent_registry_for_tests()
    approvals = get_default_approval_store()
    approvals.clear()

    # 1) register tenant-scoped sales agent
    card = AgentCard(
        agent_id="sales_agent_1",
        name="Sales Agent",
        owner="founder",
        purpose="draft and qualify opportunities",
        autonomy_level=2,
        status="active",
        tenant_id=tenant_id,
    )
    register_agent(card)
    assert get_agent("sales_agent_1") is not None

    # 2) evaluate high-risk external action via runtime governance contract
    decision = decide(
        action_type="whatsapp.send_message",
        actor="sales_agent_1",
        risk_score=0.95,
        context={"risk_score": 0.95, "is_cold": False},
    )
    assert decision.decision.value.lower() in {"escalate", "require_approval"}
    assert decision.approval_required is True

    # 3) human-ai oversight queue receives approval ticket
    req = ApprovalRequest(
        object_type="workflow_run",
        object_id=run_id,
        action_type="whatsapp.send_message",
        action_mode="approval_required",
        summary_en="Send external WhatsApp message",
        risk_level="high",
        customer_id=customer_id,
        tenant_id=tenant_id,
    )
    approvals.create(req)
    pending = approvals.list_pending()
    assert any(r.approval_id == req.approval_id for r in pending)

    # 4) approval granted by human
    approved = approvals.approve(req.approval_id, who="founder")
    assert approved.status == ApprovalStatus.APPROVED

    # 5) value metric recorded with strict evidence
    metric = add_value_event(
        tenant_id=tenant_id,
        customer_id=customer_id,
        kind="pipeline_value",
        amount=1200.0,
        tier="verified",
        source_ref="invoice#1",
    )
    assert metric.tenant_id == tenant_id
    assert len(list_value_events(customer_id=customer_id)) >= 1

    # 6) run trace contains control events
    record_event(
        customer_id=customer_id,
        engagement_id=run_id,
        kind=AuditEventKind.SOURCE_PASSPORT_VALIDATED,
        actor="data_os",
        source_refs=["SRC-1"],
        tenant_id=tenant_id,
        summary="source passport validated",
    )
    record_event(
        customer_id=customer_id,
        engagement_id=run_id,
        kind=AuditEventKind.AI_RUN,
        actor="sales_agent_1",
        source_refs=["SRC-1"],
        output_refs=["OUT-1"],
        tenant_id=tenant_id,
        summary="drafted outreach plan",
    )
    record_event(
        customer_id=customer_id,
        engagement_id=run_id,
        kind=AuditEventKind.GOVERNANCE_DECISION,
        actor="founder",
        decision="approved",
        tenant_id=tenant_id,
        summary="approval granted for controlled external action",
    )
    assert len(list_audit_events(customer_id=customer_id)) >= 3

    chain = build_chain(customer_id=customer_id, engagement_id=run_id)
    node_types = {n.node_type for n in chain.nodes}
    assert {"source", "ai_run", "decision"} <= node_types

    # 7) self-evolving proposal cannot apply without approval
    self_evolving = decide(
        action_type="self_evolving.apply_patch",
        actor="self_evolving_os",
        risk_score=0.91,
    )
    assert self_evolving.approval_required is True
    assert self_evolving.safe_alternative == "draft_only"
