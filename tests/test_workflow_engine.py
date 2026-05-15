"""
Tests for the Enterprise Workflow Engine + Lead Qualification vertical slice.

Covers the nine capabilities the blueprint requires of the vertical slice:
governance, approvals, audit, observability (span no-op safe), rollback,
evals, ROI, operational memory, typed integrations.
"""

from __future__ import annotations

import pytest

from dealix.execution.engine import WorkflowEngine
from dealix.execution.evals import evaluate_run
from dealix.execution.lead_qualification import (
    build_registry,
    corrections_log,
    crm_record,
    lead_qualification_workflow,
    register_roi_baseline,
    reset_crm,
)
from dealix.execution.memory import OperationalMemory, PermissionError_
from dealix.execution.roi import ROIBaseline, ROILedger
from dealix.execution.tool_registry import RiskLevel
from dealix.execution.workflow import RunStatus, StepStatus
from dealix.trust.approval import ApprovalCenter
from dealix.trust.audit import InMemoryAuditSink

pytestmark = pytest.mark.asyncio


HOT_LEAD = {
    "company": "شركة العقار الذكي",
    "sector": "real_estate",
    "region": "Riyadh",
    "phone": "+966500000001",
    "budget_sar": 80_000,
    "message": "نحتاج عرض سعر demo بأسرع وقت",
}


@pytest.fixture
def engine() -> WorkflowEngine:
    reset_crm()
    roi = ROILedger()
    roi.register_baseline(ROIBaseline(workflow_name="lead_qualification", manual_minutes=22.0))
    return WorkflowEngine(
        build_registry(),
        approvals=ApprovalCenter(),
        audit=InMemoryAuditSink(),
        memory=OperationalMemory(),
        roi=roi,
    )


def _wf():
    return lead_qualification_workflow()


# ── Typed tool registry ─────────────────────────────────────────────


async def test_tool_registry_risk_classification():
    reg = build_registry()
    send = reg.get("whatsapp.send_message")
    assert send.requires_approval is True
    assert send.risk == RiskLevel.MEDIUM
    assert send.reversible is True
    assert reg.get("lead.evaluate").risk == RiskLevel.LOW
    assert reg.get("lead.evaluate").requires_approval is False
    # The registry refuses duplicate names.
    with pytest.raises(ValueError):
        reg.register(send)


# ── Governance + approvals: outbound always escalates ───────────────


async def test_run_pauses_for_human_approval_before_outbound(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_1",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    assert ctx.status == RunStatus.AWAITING_APPROVAL
    assert ctx.pending_approval_id is not None

    by_name = {r.name: r for r in ctx.step_records}
    for done in ("fetch_lead", "retrieve_history", "evaluate_lead",
                 "update_status", "generate_draft"):
        assert by_name[done].status == StepStatus.COMPLETED
        assert by_name[done].policy_decision == "allow"
    # The outbound step is parked, never executed without a human.
    assert by_name["send_message"].status == StepStatus.AWAITING_APPROVAL
    assert by_name["send_message"].policy_decision == "escalate"
    # Hot lead got written back to CRM as qualified.
    assert crm_record("t1", "lead_1")["status"] == "qualified"


async def test_approval_lets_the_run_complete(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_2",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    engine.approvals.grant(ctx.pending_approval_id, "founder")
    await engine.resume(_wf(), ctx)

    assert ctx.status == RunStatus.COMPLETED
    assert ctx.step_outputs["send_message"]["delivered"] is True
    send_rec = next(r for r in ctx.step_records if r.name == "send_message")
    assert send_rec.status == StepStatus.COMPLETED
    assert send_rec.approval_request_id is not None


# ── Rollback: rejection rolls the CRM write back ────────────────────


async def test_rejection_triggers_saga_rollback(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_3",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    assert crm_record("t1", "lead_3")["status"] == "qualified"

    engine.approvals.reject(ctx.pending_approval_id, "founder", "hold for Q3")
    await engine.resume(_wf(), ctx)

    assert ctx.status == RunStatus.COMPENSATED
    update_rec = next(r for r in ctx.step_records if r.name == "update_status")
    assert update_rec.compensated is True
    # CRM status restored to its pre-run value.
    assert crm_record("t1", "lead_3")["status"] == "new"


async def test_tool_failure_triggers_rollback(engine: WorkflowEngine):
    payload = {**HOT_LEAD, "simulate_send_failure": True}
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_4",
        trigger_payload=payload, actor_id="ops",
    )
    engine.approvals.grant(ctx.pending_approval_id, "founder")
    await engine.resume(_wf(), ctx)

    assert ctx.status == RunStatus.COMPENSATED
    send_rec = next(r for r in ctx.step_records if r.name == "send_message")
    assert send_rec.status == StepStatus.FAILED
    assert send_rec.attempts == 3  # retried before giving up
    # The reversible CRM write was rolled back.
    assert crm_record("t1", "lead_4")["status"] == "new"


# ── Audit ───────────────────────────────────────────────────────────


async def test_audit_trail_covers_the_run(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_5",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    actions = [e.action.value for e in engine.audit.recent(limit=200)
               if e.workflow_id == ctx.run_id]
    assert "workflow.started" in actions
    assert "policy.evaluated" in actions
    assert "approval.requested" in actions
    assert "tool.invoked" in actions


# ── Evals ───────────────────────────────────────────────────────────


async def test_evals_pass_for_a_clean_run(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_6",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    engine.approvals.grant(ctx.pending_approval_id, "founder")
    await engine.resume(_wf(), ctx)

    result = evaluate_run(ctx.to_dict())
    assert result.passed is True
    assert result.score == pytest.approx(1.0)
    assert result.checks["no_policy_bypass"] is True
    assert result.checks["approvals_honoured"] is True
    assert result.metrics["escalations"] == 1


async def test_evals_pass_for_a_clean_rollback(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_7",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    engine.approvals.reject(ctx.pending_approval_id, "founder", "no")
    await engine.resume(_wf(), ctx)

    result = evaluate_run(ctx.to_dict())
    # A failed run that rolls back cleanly still passes governance evals.
    assert result.checks["clean_rollback_on_failure"] is True
    assert result.checks["no_policy_bypass"] is True


# ── ROI ─────────────────────────────────────────────────────────────


async def test_roi_is_booked_on_completion(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_8",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    engine.approvals.grant(ctx.pending_approval_id, "founder")
    await engine.resume(_wf(), ctx)

    summary = engine.roi.summary(tenant_id="t1")
    assert summary["runs_booked"] == 1
    assert summary["total_minutes_saved"] > 0
    assert summary["total_cost_saved_sar"] > 0


async def test_roi_not_booked_for_rolled_back_run(engine: WorkflowEngine):
    ctx = await engine.start(
        _wf(), tenant_id="t1", entity_id="lead_9",
        trigger_payload=HOT_LEAD, actor_id="ops",
    )
    engine.approvals.reject(ctx.pending_approval_id, "founder", "no")
    await engine.resume(_wf(), ctx)
    assert engine.roi.summary()["runs_booked"] == 0


# ── Operational memory + tenant isolation ───────────────────────────


async def test_memory_records_history_per_entity(engine: WorkflowEngine):
    await engine.start(_wf(), tenant_id="t1", entity_id="lead_10",
                       trigger_payload=HOT_LEAD, actor_id="ops")
    history = engine.memory.history_for_entity("lead_10", tenant_id="t1")
    assert len(history) == 1
    assert history[0]["entity_id"] == "lead_10"


async def test_memory_blocks_cross_tenant_reads(engine: WorkflowEngine):
    ctx = await engine.start(_wf(), tenant_id="t1", entity_id="lead_11",
                             trigger_payload=HOT_LEAD, actor_id="ops")
    assert engine.memory.get_run(ctx.run_id, tenant_id="t1") is not None
    with pytest.raises(PermissionError_):
        engine.memory.get_run(ctx.run_id, tenant_id="attacker_tenant")


# ── API surface ─────────────────────────────────────────────────────


async def test_api_status_endpoint(async_client):
    res = await async_client.get("/api/v1/workflow/status")
    assert res.status_code == 200
    body = res.json()
    assert body["service"] == "workflow_engine"
    assert body["hard_gates"]["outbound_requires_approval"] is True


async def test_api_run_then_approve(async_client):
    res = await async_client.post(
        "/api/v1/workflow/lead-qualification/run",
        json={
            "tenant_id": "api_t", "lead_id": "api_lead_1",
            "company": "Logistics SA", "sector": "logistics",
            "phone": "+966500000099", "budget_sar": 120000,
            "message": "need a demo and pricing",
        },
    )
    assert res.status_code == 200
    run = res.json()["run"]
    assert run["status"] == "awaiting_approval"
    run_id = run["run_id"]

    res2 = await async_client.post(
        f"/api/v1/workflow/runs/{run_id}/approve",
        json={"approver_id": "founder"},
    )
    assert res2.status_code == 200
    payload = res2.json()
    assert payload["run"]["status"] == "completed"
    assert payload["evals"]["passed"] is True


async def test_api_run_then_reject_rolls_back(async_client):
    res = await async_client.post(
        "/api/v1/workflow/lead-qualification/run",
        json={
            "tenant_id": "api_t", "lead_id": "api_lead_2",
            "company": "Acme", "sector": "fintech",
            "phone": "+966500000088", "budget_sar": 60000,
            "message": "pricing please",
        },
    )
    run_id = res.json()["run"]["run_id"]
    res2 = await async_client.post(
        f"/api/v1/workflow/runs/{run_id}/reject",
        json={"approver_id": "founder", "reason": "later"},
    )
    assert res2.json()["run"]["status"] == "compensated"
