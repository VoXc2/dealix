"""Durability, concurrency, and tenant-isolation tests for orchestrator state."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine, update

from auto_client_acquisition.orchestrator.policies import AutonomyMode, default_policy
from auto_client_acquisition.orchestrator.postgres_state import (
    ConcurrentWorkflowUpdate,
    OrchestratorTaskORM,
    PostgresTaskQueue,
    PostgresWorkflowRunStore,
    WorkflowRunORM,
)
from auto_client_acquisition.orchestrator.queue import TaskStatus
from auto_client_acquisition.orchestrator.runtime import (
    DAILY_GROWTH_RUN,
    Orchestrator,
    WorkflowDefinition,
    WorkflowRunState,
    WorkflowStep,
)
from auto_client_acquisition.orchestrator.tools import default_executors
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore


@pytest.fixture
def engine(tmp_path):
    db_path = tmp_path / "orchestrator.db"
    value = create_engine(f"sqlite:///{db_path}", future=True)
    WorkflowRunORM.metadata.create_all(value)
    return value


def _state(*, tenant_id: str, run_id: str = "run-1") -> WorkflowRunState:
    return WorkflowRunState(
        run_id=run_id,
        tenant_id=tenant_id,
        workflow_id="daily_growth_run",
        customer_id="customer-1",
        idempotency_key="daily-2026-08-15",
    )


def test_database_idempotency_survives_process_instances(engine) -> None:
    first = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    second = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")

    created_state, created = first.reserve(_state(tenant_id="tenant-a"))
    replay_state, replay_created = second.reserve(
        _state(tenant_id="tenant-a", run_id="another-generated-id")
    )

    assert created is True
    assert replay_created is False
    assert replay_state.run_id == created_state.run_id


def test_stale_workflow_snapshot_cannot_overwrite_newer_state(engine) -> None:
    store = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    store.reserve(_state(tenant_id="tenant-a"))
    first = store.get("run-1", tenant_id="tenant-a")
    stale = store.get("run-1", tenant_id="tenant-a")
    assert first is not None and stale is not None

    first.next_step_index = 1
    store.save(first)
    stale.next_step_index = 99

    with pytest.raises(ConcurrentWorkflowUpdate):
        store.save(stale)


def test_run_lease_is_atomic_and_expired_lease_is_recoverable(engine) -> None:
    first = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    second = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    first.reserve(_state(tenant_id="tenant-a"))

    assert first.claim("run-1", tenant_id="tenant-a", worker_id="worker-1") is not None
    assert second.claim("run-1", tenant_id="tenant-a", worker_id="worker-2") is None

    with engine.begin() as connection:
        connection.execute(
            update(WorkflowRunORM)
            .where(WorkflowRunORM.run_id == "run-1")
            .values(lease_expires_at=datetime.now(UTC) - timedelta(seconds=1))
        )

    assert second.claim("run-1", tenant_id="tenant-a", worker_id="worker-2") is not None


def test_task_enqueue_is_idempotent_per_tenant_run_and_step(engine) -> None:
    first = PostgresTaskQueue(engine, tenant_id="tenant-a")
    second = PostgresTaskQueue(engine, tenant_id="tenant-a")
    args = {
        "tenant_id": "tenant-a",
        "customer_id": "customer-1",
        "agent_id": "prospecting",
        "action_type": "discover_leads",
        "payload": {"step_id": "1_discover"},
        "correlation_id": "run-1",
    }

    original = first.enqueue(**args)
    replay = second.enqueue(**args)

    assert replay.task_id == original.task_id
    assert first.summary(tenant_id="tenant-a")[TaskStatus.PENDING] == 1


def test_task_claim_prevents_duplicate_execution_and_recovers_after_expiry(engine) -> None:
    first = PostgresTaskQueue(engine, tenant_id="tenant-a")
    second = PostgresTaskQueue(engine, tenant_id="tenant-a")
    task = first.enqueue(
        tenant_id="tenant-a",
        customer_id="customer-1",
        agent_id="prospecting",
        action_type="discover_leads",
        payload={"step_id": "1_discover"},
        correlation_id="run-1",
    )

    first.mark_executing(task.task_id, tenant_id="tenant-a", worker_id="worker-1")
    with pytest.raises(ValueError, match="cannot execute"):
        second.mark_executing(task.task_id, tenant_id="tenant-a", worker_id="worker-2")

    with engine.begin() as connection:
        connection.execute(
            update(OrchestratorTaskORM)
            .where(OrchestratorTaskORM.task_id == task.task_id)
            .values(claim_expires_at=datetime.now(UTC) - timedelta(seconds=1))
        )

    recovered = second.mark_executing(
        task.task_id,
        tenant_id="tenant-a",
        worker_id="worker-2",
    )
    assert recovered.status == TaskStatus.EXECUTING
    succeeded = second.succeed(
        task.task_id,
        result={"ok": True},
        tenant_id="tenant-a",
        worker_id="worker-2",
    )
    assert succeeded.status == TaskStatus.SUCCEEDED


def test_every_read_and_mutation_is_tenant_bound(engine) -> None:
    runs_a = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    runs_b = PostgresWorkflowRunStore(engine, tenant_id="tenant-b")
    tasks_a = PostgresTaskQueue(engine, tenant_id="tenant-a")
    tasks_b = PostgresTaskQueue(engine, tenant_id="tenant-b")
    runs_a.reserve(_state(tenant_id="tenant-a"))
    task = tasks_a.enqueue(
        tenant_id="tenant-a",
        customer_id="customer-1",
        agent_id="prospecting",
        action_type="discover_leads",
        payload={"step_id": "1_discover"},
        correlation_id="run-1",
    )

    assert runs_b.get("run-1", tenant_id="tenant-b") is None
    assert tasks_b.get(task.task_id, tenant_id="tenant-b") is None
    with pytest.raises(ValueError, match="cross-tenant"):
        runs_a.get("run-1", tenant_id="tenant-b")
    with pytest.raises(ValueError, match="cross-tenant"):
        tasks_a.get(task.task_id, tenant_id="tenant-b")


def test_workflow_restarts_on_new_instances_and_resumes_after_approval(engine) -> None:
    def resolver(customer_id):
        policy = default_policy(customer_id)
        policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        policy.require_human_for_first_send = False
        return policy

    executors = default_executors()
    executors["send_message"] = lambda task: {
        "provider_message_id": "provider-test-1",
        "source_ref": "provider:test-1",
        "execution_mode": "controlled_test",
    }
    queue_1 = PostgresTaskQueue(engine, tenant_id="tenant-a")
    runs_1 = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    first = Orchestrator(
        queue=queue_1,
        event_store=InMemoryEventStore(),
        policy_resolver=resolver,
        executor_registry=executors,
        tenant_id="tenant-a",
        run_store=runs_1,
    )
    initial = first.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="customer-1",
        idempotency_key="daily-2026-08-15",
    )
    assert initial["status"] == "awaiting_approval"
    assert initial["tasks_created"] == 6

    queue_2 = PostgresTaskQueue(engine, tenant_id="tenant-a")
    runs_2 = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    restarted = Orchestrator(
        queue=queue_2,
        event_store=InMemoryEventStore(),
        policy_resolver=resolver,
        executor_registry=executors,
        tenant_id="tenant-a",
        run_store=runs_2,
    )
    replay = restarted.run_workflow(
        workflow=DAILY_GROWTH_RUN,
        customer_id="customer-1",
        idempotency_key="daily-2026-08-15",
    )
    assert replay["replayed"] is True
    assert replay["tasks_created"] == 6
    assert queue_2.summary(tenant_id="tenant-a")[TaskStatus.AWAITING_APPROVAL] == 1

    approved = restarted.approve_and_execute(
        task_id=replay["awaiting_approval"][0],
        approved_by="owner@tenant-a.sa",
    )
    completed = restarted.get_workflow_run(replay["correlation_id"])

    assert approved.status == TaskStatus.SUCCEEDED
    assert completed["status"] == "completed"
    assert completed["tasks_created"] == 8
    assert len(completed["succeeded"]) == 8


def test_missing_executor_is_terminal_in_persisted_run(engine) -> None:
    queue = PostgresTaskQueue(engine, tenant_id="tenant-a")
    runs = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    workflow = WorkflowDefinition(
        workflow_id="missing-executor",
        name="Missing executor",
        description="terminal configuration failure",
        steps=(WorkflowStep("step-1", "agent-1", "discover_leads"),),
    )
    orchestrator = Orchestrator(
        queue=queue,
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry={},
        tenant_id="tenant-a",
        run_store=runs,
    )

    summary = orchestrator.run_workflow(
        workflow=workflow,
        customer_id="customer-1",
        idempotency_key="missing-executor-1",
    )

    assert summary["status"] == "failed"
    assert len(summary["failed"]) == 1
    assert summary["failure_reason"] == "no executor for discover_leads"


def test_committed_task_outcome_is_reused_after_run_snapshot_crash(engine) -> None:
    queue = PostgresTaskQueue(engine, tenant_id="tenant-a")
    runs = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    workflow = WorkflowDefinition(
        workflow_id="recover-committed-task",
        name="Recover committed task",
        description="reuse durable task result",
        steps=(WorkflowStep("step-1", "agent-1", "discover_leads"),),
    )
    run_state = WorkflowRunState(
        run_id="run-recover-1",
        tenant_id="tenant-a",
        workflow_id=workflow.workflow_id,
        customer_id="customer-1",
        idempotency_key="recover-1",
    )
    runs.reserve(run_state)
    task = queue.enqueue(
        tenant_id="tenant-a",
        customer_id="customer-1",
        agent_id="agent-1",
        action_type="discover_leads",
        payload={"step_id": "step-1", "inputs": {}},
        correlation_id=run_state.run_id,
        parent_workflow_id=workflow.workflow_id,
    )
    queue.mark_executing(task.task_id, tenant_id="tenant-a", worker_id="crashed-worker")
    queue.succeed(
        task.task_id,
        result={"source_ref": "durable:1"},
        tenant_id="tenant-a",
        worker_id="crashed-worker",
    )
    orchestrator = Orchestrator(
        queue=queue,
        event_store=InMemoryEventStore(),
        policy_resolver=default_policy,
        executor_registry={
            "discover_leads": lambda task: pytest.fail("provider must not run twice")
        },
        tenant_id="tenant-a",
        run_store=runs,
    )

    summary = orchestrator.run_workflow(
        workflow=workflow,
        customer_id="customer-1",
        idempotency_key="recover-1",
    )

    assert summary["status"] == "completed"
    assert summary["completed_steps"] == ["step-1"]
    assert summary["tasks_created"] == 1


def test_approved_external_outcome_resumes_without_second_provider_call(engine) -> None:
    def resolver(customer_id):
        policy = default_policy(customer_id)
        policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
        return policy

    queue = PostgresTaskQueue(engine, tenant_id="tenant-a")
    runs = PostgresWorkflowRunStore(engine, tenant_id="tenant-a")
    workflow = WorkflowDefinition(
        workflow_id="recover-approved-external",
        name="Recover approved external",
        description="approval result survives process crash",
        steps=(WorkflowStep("send-1", "outreach", "send_message"),),
    )
    first = Orchestrator(
        queue=queue,
        event_store=InMemoryEventStore(),
        policy_resolver=resolver,
        executor_registry={},
        tenant_id="tenant-a",
        run_store=runs,
    )
    waiting = first.run_workflow(
        workflow=workflow,
        customer_id="customer-1",
        idempotency_key="approved-crash-1",
    )
    task_id = waiting["awaiting_approval"][0]
    approver = "owner@tenant-a.sa"
    queue.approve(task_id, approved_by=approver, tenant_id="tenant-a")
    queue.mark_executing(task_id, tenant_id="tenant-a", worker_id="crashed-worker")
    queue.succeed(
        task_id,
        result={
            "provider_message_id": "provider-1",
            "source_ref": "provider:1",
        },
        tenant_id="tenant-a",
        worker_id="crashed-worker",
    )
    restarted = Orchestrator(
        queue=PostgresTaskQueue(engine, tenant_id="tenant-a"),
        event_store=InMemoryEventStore(),
        policy_resolver=resolver,
        executor_registry={
            "send_message": lambda task: pytest.fail("provider must not run twice")
        },
        tenant_id="tenant-a",
        run_store=PostgresWorkflowRunStore(engine, tenant_id="tenant-a"),
        workflow_registry={workflow.workflow_id: workflow},
    )

    task = restarted.approve_and_execute(task_id=task_id, approved_by=approver)
    summary = restarted.get_workflow_run(waiting["correlation_id"])

    assert task.status == TaskStatus.SUCCEEDED
    assert summary["status"] == "completed"
