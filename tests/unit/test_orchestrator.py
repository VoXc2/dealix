"""Smoke tests for the Agent Orchestrator runtime."""

from __future__ import annotations

import pytest

from auto_client_acquisition.orchestrator.policies import (
    ALL_MODES,
    AutonomyMode,
    BudgetLimit,
    BudgetUsage,
    Policy,
    default_policy,
    is_in_quiet_hours,
    requires_approval,
    within_budget,
)
from auto_client_acquisition.orchestrator.queue import (
    JsonTaskQueue,
    TaskQueue,
    TaskStatus,
)
from auto_client_acquisition.orchestrator.runtime import (
    DAILY_GROWTH_RUN,
    JsonWorkflowRunStore,
    Orchestrator,
    WorkflowDefinition,
    WorkflowStep,
)
from auto_client_acquisition.orchestrator.tools import default_executors
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore


# ── Policies ─────────────────────────────────────────────────────
def test_all_modes_known():
    assert AutonomyMode.MANUAL in ALL_MODES
    assert AutonomyMode.FULL_AUTOPILOT in ALL_MODES


def test_manual_mode_always_requires_approval():
    p = default_policy("c1")
    p.autonomy_mode = AutonomyMode.MANUAL
    needs, _ = requires_approval(action_type="send_message", policy=p)
    assert needs is True


def test_safe_autopilot_still_requires_human_for_routine_send():
    p = default_policy("c1")
    p.autonomy_mode = AutonomyMode.SAFE_AUTOPILOT
    p.require_human_for_first_send = False
    needs, _ = requires_approval(
        action_type="send_message",
        policy=p,
        risk_factors={"is_first_send_to_account": False, "deal_value_sar": 5000},
    )
    assert needs is True


def test_high_value_deal_escalates_even_in_autopilot():
    p = default_policy("c1")
    p.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
    p.require_human_for_first_send = False
    needs, reason = requires_approval(
        action_type="send_message",
        policy=p,
        risk_factors={"deal_value_sar": 200_000},
    )
    assert needs is True
    assert "high_value_deal" in (reason or "")


def test_blocked_keyword_escalates():
    p = default_policy("c1")
    p.autonomy_mode = AutonomyMode.SAFE_AUTOPILOT
    p.blocked_keywords = ("ضمان",)
    p.require_human_for_first_send = False
    needs, reason = requires_approval(
        action_type="send_message",
        policy=p,
        risk_factors={"draft_text": "نقدم ضمان كامل"},
    )
    assert needs is True
    assert "blocked_keyword" in (reason or "")


def test_quiet_hours_overnight():
    p = default_policy("c1")
    p.quiet_hours_riyadh = (21, 8)
    assert is_in_quiet_hours(hour_riyadh=22, policy=p) is True
    assert is_in_quiet_hours(hour_riyadh=3, policy=p) is True
    assert is_in_quiet_hours(hour_riyadh=10, policy=p) is False


def test_within_budget_blocks_when_exceeded():
    budget = BudgetLimit(max_messages_per_day=10)
    usage = BudgetUsage(messages_today=10)
    ok, reason = within_budget(usage=usage, budget=budget)
    assert ok is False
    assert "messages" in (reason or "")


def test_within_budget_allows_below_caps():
    ok, _ = within_budget(usage=BudgetUsage(messages_today=5), budget=BudgetLimit())
    assert ok is True


# ── Queue ────────────────────────────────────────────────────────
def test_enqueue_pending_no_approval():
    q = TaskQueue()
    t = q.enqueue(customer_id="c1", agent_id="prospecting", action_type="discover_leads")
    assert t.status == TaskStatus.PENDING


def test_enqueue_awaiting_approval():
    q = TaskQueue()
    t = q.enqueue(
        customer_id="c1", agent_id="outreach", action_type="send_message",
        requires_approval=True, approval_reason="first_send",
    )
    assert t.status == TaskStatus.AWAITING_APPROVAL


def test_approve_then_succeed():
    q = TaskQueue()
    t = q.enqueue(customer_id="c1", agent_id="outreach", action_type="send_message",
                  requires_approval=True)
    q.approve(t.task_id, approved_by="user@x.sa")
    assert t.status == TaskStatus.APPROVED
    q.mark_executing(t.task_id)
    q.succeed(t.task_id, result={"sent": 1})
    assert t.status == TaskStatus.SUCCEEDED


def test_reject_terminates():
    q = TaskQueue()
    t = q.enqueue(customer_id="c1", agent_id="outreach", action_type="send_message",
                  requires_approval=True)
    q.reject(t.task_id, rejected_by="user@x.sa", reason="not now")
    assert t.status == TaskStatus.REJECTED


def test_fail_with_retries_returns_to_pending():
    q = TaskQueue()
    t = q.enqueue(customer_id="c1", agent_id="outreach", action_type="send_message")
    q.mark_executing(t.task_id)
    q.fail(t.task_id, error="provider_timeout")
    assert t.status == TaskStatus.PENDING
    assert t.retries == 1


def test_fail_after_max_retries_terminates():
    q = TaskQueue()
    t = q.enqueue(customer_id="c1", agent_id="outreach", action_type="send_message")
    t.max_retries = 1
    q.mark_executing(t.task_id)
    q.fail(t.task_id, error="error1")  # retry 1
    q.mark_executing(t.task_id)
    q.fail(t.task_id, error="error2")  # exhausts retries
    assert t.status == TaskStatus.FAILED


def test_summary_counts():
    q = TaskQueue()
    q.enqueue(customer_id="c1", agent_id="x", action_type="discover_leads")
    q.enqueue(customer_id="c1", agent_id="x", action_type="discover_leads",
              requires_approval=True)
    s = q.summary()
    assert s[TaskStatus.PENDING] == 1
    assert s[TaskStatus.AWAITING_APPROVAL] == 1


def test_workflow_step_enqueue_is_idempotent():
    q = TaskQueue()
    kwargs = {
        "tenant_id": "tenant-a",
        "customer_id": "c1",
        "agent_id": "prospecting",
        "action_type": "discover_leads",
        "payload": {"step_id": "1_discover"},
        "correlation_id": "run-1",
    }
    first = q.enqueue(**kwargs)
    replay = q.enqueue(**kwargs)
    assert replay.task_id == first.task_id
    assert replay.execution_idempotency_key == f"dealix:tenant-a:{first.task_id}"
    assert len(q.tasks) == 1


# ── Runtime ──────────────────────────────────────────────────────
def test_run_workflow_executes_internal_steps_and_holds_external():
    """Full autopilot executes internal work but never bypasses external approval."""
    queue = TaskQueue()
    store = InMemoryEventStore()

    def policy_resolver(customer_id):
        p = default_policy(customer_id)
        p.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        p.require_human_for_first_send = False
        return p

    orch = Orchestrator(
        queue=queue,
        event_store=store,
        policy_resolver=policy_resolver,
        executor_registry=default_executors(),
    )
    summary = orch.run_workflow(workflow=DAILY_GROWTH_RUN, customer_id="c1")
    assert summary["tasks_created"] == 6
    assert len(summary["awaiting_approval"]) == 1
    assert len(summary["succeeded"]) == 5
    assert summary["status"] == "awaiting_approval"
    assert summary["blocked_steps"] == []
    assert summary["deferred_steps"] == [
        "7_classify",
        "8_brief",
    ]


def test_run_workflow_draft_approve_holds_send():
    """In draft_and_approve, send_message tasks await approval."""
    queue = TaskQueue()
    store = InMemoryEventStore()

    def policy_resolver(customer_id):
        p = default_policy(customer_id)
        p.autonomy_mode = AutonomyMode.DRAFT_APPROVE
        return p

    orch = Orchestrator(
        queue=queue,
        event_store=store,
        policy_resolver=policy_resolver,
        executor_registry=default_executors(),
    )
    summary = orch.run_workflow(workflow=DAILY_GROWTH_RUN, customer_id="c1")
    # send_message step should be awaiting_approval, not succeeded
    awaiting_tasks = [queue.tasks[tid] for tid in summary["awaiting_approval"]]
    awaiting_actions = {t.action_type for t in awaiting_tasks}
    assert "send_message" in awaiting_actions


def test_risk_context_reaches_external_approval_reason():
    queue = TaskQueue()
    store = InMemoryEventStore()

    def resolver(customer_id):
        policy = default_policy(customer_id)
        policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        policy.require_human_for_first_send = False
        return policy

    orch = Orchestrator(
        queue=queue,
        event_store=store,
        policy_resolver=resolver,
        executor_registry=default_executors(),
    )
    summary = orch.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="c1",
        initial_inputs={"deal_value_sar": 250_000},
    )

    task = queue.tasks[summary["awaiting_approval"][0]]
    assert task.approval_reason == "high_value_deal_sar=250000"


def test_run_workflow_emits_events():
    queue = TaskQueue()
    store = InMemoryEventStore()

    def resolver(c):
        p = default_policy(c)
        p.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        p.require_human_for_first_send = False
        return p

    orch = Orchestrator(queue=queue, event_store=store, policy_resolver=resolver,
                       executor_registry=default_executors())
    orch.run_workflow(workflow=DAILY_GROWTH_RUN, customer_id="c1")

    requested = [e for e in store._sorted_events() if e.event_type == "agent.action_requested"]
    executed = [e for e in store._sorted_events() if e.event_type == "agent.action_executed"]
    assert len(requested) == 6
    assert len(executed) == 5


def test_telemetry_failure_does_not_revert_committed_task_outcome():
    class FailingExecutionEventStore(InMemoryEventStore):
        def append(self, event):
            if event.event_type == "agent.action_executed":
                raise RuntimeError("telemetry unavailable")
            return super().append(event)

    workflow = WorkflowDefinition(
        workflow_id="telemetry-resilience",
        name="Telemetry resilience",
        description="task outcome remains authoritative",
        steps=(WorkflowStep("step-1", "prospecting", "discover_leads"),),
    )
    queue = TaskQueue()
    orchestrator = Orchestrator(
        queue=queue,
        event_store=FailingExecutionEventStore(),
        policy_resolver=default_policy,
        executor_registry=default_executors(),
    )

    summary = orchestrator.run_workflow(workflow=workflow, customer_id="c1")

    assert summary["status"] == "completed"
    assert queue.get(summary["succeeded"][0]).status == TaskStatus.SUCCEEDED


def test_approve_and_execute_flow():
    queue = TaskQueue()
    store = InMemoryEventStore()

    def resolver(c):
        p = default_policy(c)
        p.autonomy_mode = AutonomyMode.DRAFT_APPROVE
        return p

    orch = Orchestrator(queue=queue, event_store=store, policy_resolver=resolver,
                       executor_registry=default_executors())
    summary = orch.run_workflow(workflow=DAILY_GROWTH_RUN, customer_id="c1")
    assert len(summary["awaiting_approval"]) > 0
    pending_id = summary["awaiting_approval"][0]
    orch.executor_registry["send_message"] = lambda _task: {"sent": 1}
    task = orch.approve_and_execute(task_id=pending_id, approved_by="user@x.sa")
    assert task.status == TaskStatus.SUCCEEDED
    resumed = orch.get_workflow_run(summary["correlation_id"])
    assert resumed["status"] == "completed"
    assert resumed["finalized"] is True
    assert len(resumed["succeeded"]) == len(DAILY_GROWTH_RUN.steps)
    assert resumed["completed_steps"] == [step.step_id for step in DAILY_GROWTH_RUN.steps]
    closure_events = [
        event
        for event in store._sorted_events()
        if event.event_type.startswith("workflow.")
    ]
    assert [event.event_type for event in closure_events] == [
        "workflow.outcome_recorded",
        "workflow.proof_recorded",
        "workflow.learning_proposed",
    ]
    proof = closure_events[1]
    assert proof.payload["claimable_external"] is False
    assert proof.payload["evidence_level"] == "L0"


def test_idempotency_replays_existing_run_without_duplicate_tasks():
    queue = TaskQueue()
    orch = Orchestrator(
        queue=queue,
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry=default_executors(),
    )

    first = orch.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="c1",
        idempotency_key="riyadh-2026-08-15",
    )
    replay = orch.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="c1",
        idempotency_key="riyadh-2026-08-15",
    )

    assert replay["correlation_id"] == first["correlation_id"]
    assert replay["replayed"] is True
    assert replay["tasks_created"] == first["tasks_created"]
    assert len(queue.tasks) == first["tasks_created"]


def test_retry_resumes_transient_failure_and_completes():
    attempts = {"count": 0}

    def flaky(_task):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("temporary")
        return {"ok": True}

    workflow = WorkflowDefinition(
        workflow_id="retryable",
        name="Retryable",
        description="",
        steps=(WorkflowStep("one", "ops", "discover_leads"),),
    )
    orch = Orchestrator(
        queue=TaskQueue(),
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry={"discover_leads": flaky},
    )

    first = orch.run_workflow(workflow=workflow, customer_id="c1")
    assert first["status"] == "retry_pending"
    done = orch.retry_workflow(run_id=first["correlation_id"])
    assert done["status"] == "completed"
    assert attempts["count"] == 2


def test_json_state_survives_restart_and_resumes_after_approval(tmp_path):
    queue_path = tmp_path / "tasks.json"
    runs_path = tmp_path / "runs.json"

    first = Orchestrator(
        queue=JsonTaskQueue(queue_path),
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry=default_executors(),
        run_store=JsonWorkflowRunStore(runs_path),
    )
    started = first.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="c1",
        idempotency_key="restart-proof",
    )
    pending_id = started["awaiting_approval"][0]

    executors = default_executors()
    executors["send_message"] = lambda _task: {
        "sent": 1,
        "source_ref": "provider-receipt-1",
    }
    restarted = Orchestrator(
        queue=JsonTaskQueue(queue_path),
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry=executors,
        run_store=JsonWorkflowRunStore(runs_path),
    )

    task = restarted.approve_and_execute(
        task_id=pending_id,
        approved_by="founder@dealix.sa",
    )
    completed = restarted.get_workflow_run(started["correlation_id"])

    assert task.status == TaskStatus.SUCCEEDED
    assert completed["status"] == "completed"
    assert completed["finalized"] is True
    replay = restarted.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="c1",
        idempotency_key="restart-proof",
    )
    assert replay["replayed"] is True
    assert replay["correlation_id"] == started["correlation_id"]


def test_approved_external_task_without_connector_fails_closed():
    queue = TaskQueue()
    store = InMemoryEventStore()

    orch = Orchestrator(
        queue=queue,
        event_store=store,
        policy_resolver=default_policy,
        executor_registry=default_executors(),
    )
    task = queue.enqueue(
        customer_id="c1",
        agent_id="outreach",
        action_type="send_message",
        requires_approval=True,
    )

    result = orch.approve_and_execute(
        task_id=task.task_id,
        approved_by="user@x.sa",
    )

    assert result.status == TaskStatus.FAILED
    assert result.retries == 0
    assert result.error == "no executor for send_message"


def test_budget_exhaustion_stops_workflow():
    queue = TaskQueue()
    store = InMemoryEventStore()

    def resolver(c):
        p = default_policy(c)
        p.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        p.require_human_for_first_send = False
        p.budget = BudgetLimit(max_messages_per_day=1, max_external_api_calls_per_day=2)
        return p

    orch = Orchestrator(queue=queue, event_store=store, policy_resolver=resolver,
                       executor_registry=default_executors())
    orch.run_workflow(workflow=DAILY_GROWTH_RUN, customer_id="c1")
    rejected_events = [e for e in store._sorted_events() if e.event_type == "agent.action_rejected"]
    # At least one budget rejection should be emitted
    assert any("budget" in e.payload.get("reason", "") for e in rejected_events)


def test_executor_failure_marks_task_failed_after_retries():
    queue = TaskQueue()
    store = InMemoryEventStore()

    def resolver(c):
        p = default_policy(c)
        p.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        p.require_human_for_first_send = False
        return p

    def bad_executor(task):
        raise RuntimeError("simulated provider failure")

    orch = Orchestrator(
        queue=queue, event_store=store, policy_resolver=resolver,
        executor_registry={"discover_leads": bad_executor},
    )
    short_wf = WorkflowDefinition(
        workflow_id="short", name="Short", description="",
        steps=(WorkflowStep("1", "prospecting", "discover_leads"),),
    )
    summary = orch.run_workflow(workflow=short_wf, customer_id="c1")
    failed_events = [e for e in store._sorted_events() if e.event_type == "agent.action_failed"]
    assert len(failed_events) >= 1
