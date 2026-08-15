"""
Orchestrator Runtime — runs agent workflows.

A WorkflowDefinition is a graph of WorkflowSteps. Each step:
  - chooses the agent that runs it
  - declares its action_type
  - takes inputs (often outputs from prior steps)
  - emits AgentTask + RevenueEvent

The Orchestrator handles policy checks, approval gates, retries, and
event emission. It is deterministic given the same inputs + policy.

Key design: agents themselves are pluggable via a `tool_registry` callable.
This means the runtime is testable without spinning up real LLMs / providers.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any

from auto_client_acquisition.orchestrator.policies import (
    EXTERNAL_ACTION_TYPES,
    BudgetUsage,
    Policy,
    requires_approval,
    within_budget,
)
from auto_client_acquisition.orchestrator.queue import AgentTask, TaskQueue, TaskStatus
from auto_client_acquisition.revenue_memory.event_store import EventStore
from auto_client_acquisition.revenue_memory.events import RevenueEvent, make_event

log = logging.getLogger(__name__)


# ── Workflow definition ───────────────────────────────────────────
@dataclass
class WorkflowStep:
    step_id: str                 # unique within workflow
    agent_id: str                # which of the 11 agents
    action_type: str             # one of policies.ACTION_TYPES
    inputs_from: tuple[str, ...] = ()  # step_ids whose outputs feed this step
    description: str = ""


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    description: str
    steps: tuple[WorkflowStep, ...]


# ── The flagship workflow: Daily Growth Run ──────────────────────
DAILY_GROWTH_RUN = WorkflowDefinition(
    workflow_id="daily_growth_run",
    name="Daily Growth Run — اكتشاف + تأهيل + إرسال",
    description=(
        "كل صباح: اكتشاف 200 شركة → اختيار 40 بإشارات → enrichment → "
        "compliance check → personalization → human approval → send → "
        "classify replies → تقرير نهاية اليوم."
    ),
    steps=(
        WorkflowStep("1_discover", "prospecting", "discover_leads",
                     description="200 شركة جديدة من Saudi Maps + LinkedIn"),
        WorkflowStep("2_signals", "signal", "discover_leads",
                     ("1_discover",), "اختيار أعلى 40 بإشارات شراء"),
        WorkflowStep("3_enrich", "enrichment", "enrich_lead",
                     ("2_signals",), "تكميل بيانات DM + size + tech"),
        WorkflowStep("4_compliance", "compliance", "draft_message",
                     ("3_enrich",), "فحص PDPL + opt-out قبل أي صياغة"),
        WorkflowStep("5_personalize", "personalization", "draft_message",
                     ("4_compliance",), "صياغة رسالة عربية مخصصة لكل شركة"),
        WorkflowStep("6_send", "outreach", "send_message",
                     ("5_personalize",), "إرسال عبر القناة الأنسب"),
        WorkflowStep("7_classify", "reply", "classify_reply",
                     ("6_send",), "تصنيف كل رد + اقتراح next action"),
        WorkflowStep("8_brief", "executive_analyst", "generate_qbr",
                     ("7_classify",), "تقرير نهاية اليوم"),
    ),
)


# ── Executor signature ────────────────────────────────────────────
ExecutorFunc = Callable[[AgentTask], dict[str, Any]]
"""Run one task and return evidence-bearing output (or raise).

External connectors must pass ``task.execution_idempotency_key`` to the
provider when that provider supports idempotency. Dealix never registers an
external connector by default, so no side effect occurs without explicit
configuration and a human approval.
"""


class WorkflowRunStatus:
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    RETRY_PENDING = "retry_pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


@dataclass
class WorkflowRunState:
    """Serializable state needed to resume one governed workflow run."""

    run_id: str
    tenant_id: str
    workflow_id: str
    customer_id: str
    idempotency_key: str
    initial_inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    task_ids: list[str] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    next_step_index: int = 0
    status: str = WorkflowRunStatus.RUNNING
    awaiting_task_id: str | None = None
    failure_reason: str | None = None
    finalized: bool = False
    version: int = 0


class InMemoryWorkflowRunStore:
    """Thread-safe run store; production adapters can implement the same API."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._runs: dict[str, WorkflowRunState] = {}
        self._idempotency_index: dict[tuple[str, str, str, str], str] = {}
        self._leases: dict[str, tuple[str, datetime]] = {}

    backend_name = "memory"

    def save(self, state: WorkflowRunState) -> WorkflowRunState:
        with self._lock:
            self._runs[state.run_id] = state
            self._idempotency_index[
                (state.tenant_id, state.customer_id, state.workflow_id, state.idempotency_key)
            ] = state.run_id
        return state

    def reserve(self, state: WorkflowRunState) -> tuple[WorkflowRunState, bool]:
        """Atomically reserve an idempotency key for one workflow run."""
        key = (state.tenant_id, state.customer_id, state.workflow_id, state.idempotency_key)
        with self._lock:
            existing_id = self._idempotency_index.get(key)
            if existing_id:
                return self._runs[existing_id], False
            self._runs[state.run_id] = state
            self._idempotency_index[key] = state.run_id
            return state, True

    def get(
        self,
        run_id: str,
        *,
        tenant_id: str | None = None,
    ) -> WorkflowRunState | None:
        with self._lock:
            state = self._runs.get(run_id)
            if state is not None and tenant_id is not None and state.tenant_id != tenant_id:
                return None
            return state

    def find_idempotent(
        self,
        *,
        tenant_id: str = "default",
        customer_id: str,
        workflow_id: str,
        idempotency_key: str,
    ) -> WorkflowRunState | None:
        with self._lock:
            run_id = self._idempotency_index.get(
                (tenant_id, customer_id, workflow_id, idempotency_key)
            )
            return self._runs.get(run_id) if run_id else None

    def claim(
        self,
        run_id: str,
        *,
        tenant_id: str,
        worker_id: str,
        lease_seconds: int = 60,
    ) -> WorkflowRunState | None:
        """Acquire a short workflow lease; expired leases are recoverable."""
        now = datetime.now(UTC)
        with self._lock:
            state = self._runs.get(run_id)
            if state is None or state.tenant_id != tenant_id:
                return None
            current = self._leases.get(run_id)
            if current and current[0] != worker_id and current[1] > now:
                return None
            self._leases[run_id] = (worker_id, now + timedelta(seconds=lease_seconds))
            return state

    def release(self, run_id: str, *, tenant_id: str, worker_id: str) -> None:
        with self._lock:
            state = self._runs.get(run_id)
            current = self._leases.get(run_id)
            if state is not None and state.tenant_id == tenant_id and current:
                if current[0] == worker_id:
                    self._leases.pop(run_id, None)


class JsonWorkflowRunStore(InMemoryWorkflowRunStore):
    """Atomic JSON-backed run store for restart-safe single-node operation."""

    backend_name = "json"

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        super().__init__()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if not self._path.is_file():
            return
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for run_id, payload in (raw.get("runs") or {}).items():
            if not isinstance(payload, dict):
                continue
            payload.setdefault("tenant_id", "default")
            payload.setdefault("version", 0)
            state = WorkflowRunState(**payload)
            self._runs[run_id] = state
            self._idempotency_index[
                (state.tenant_id, state.customer_id, state.workflow_id, state.idempotency_key)
            ] = run_id

    def save(self, state: WorkflowRunState) -> WorkflowRunState:
        with self._lock:
            self._runs[state.run_id] = state
            self._idempotency_index[
                (state.tenant_id, state.customer_id, state.workflow_id, state.idempotency_key)
            ] = state.run_id
            self._flush_locked()
        return state

    def reserve(self, state: WorkflowRunState) -> tuple[WorkflowRunState, bool]:
        key = (state.tenant_id, state.customer_id, state.workflow_id, state.idempotency_key)
        with self._lock:
            existing_id = self._idempotency_index.get(key)
            if existing_id:
                return self._runs[existing_id], False
            self._runs[state.run_id] = state
            self._idempotency_index[key] = state.run_id
            self._flush_locked()
            return state, True

    def _flush_locked(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self._path.with_suffix(self._path.suffix + ".tmp")
        temp_path.write_text(
            json.dumps(
                {"runs": {key: asdict(value) for key, value in self._runs.items()}},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        os.replace(temp_path, self._path)


# ── The Orchestrator ──────────────────────────────────────────────
@dataclass
class Orchestrator:
    """Runs workflows + enforces policy + emits events."""

    queue: TaskQueue
    event_store: EventStore
    policy_resolver: Callable[[str], Policy]    # customer_id → Policy
    executor_registry: dict[str, ExecutorFunc]  # action_type → executor
    tenant_id: str = "default"
    worker_id: str = field(default_factory=lambda: f"worker_{uuid.uuid4().hex[:16]}")
    budget_usage: dict[str, BudgetUsage] = field(default_factory=dict)
    run_store: InMemoryWorkflowRunStore = field(default_factory=InMemoryWorkflowRunStore)
    workflow_registry: dict[str, WorkflowDefinition] = field(
        default_factory=lambda: {DAILY_GROWTH_RUN.workflow_id: DAILY_GROWTH_RUN}
    )

    # ── Public API ───────────────────────────────────────────
    def run_workflow(
        self,
        *,
        workflow: WorkflowDefinition,
        customer_id: str,
        initial_inputs: dict[str, Any] | None = None,
        actor: str = "system",
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """
        Plan + dispatch one full workflow run.

        Returns the final summary: tasks created, executed, awaiting_approval, failed.
        """
        idem = (idempotency_key or uuid.uuid4().hex).strip()
        if not idem:
            raise ValueError("idempotency_key cannot be empty")
        digest = sha256(
            f"{self.tenant_id}:{customer_id}:{workflow.workflow_id}:{idem}".encode()
        ).hexdigest()[:16]
        state = WorkflowRunState(
            run_id=f"wf_{digest}",
            tenant_id=self.tenant_id,
            workflow_id=workflow.workflow_id,
            customer_id=customer_id,
            idempotency_key=idem,
            initial_inputs=dict(initial_inputs or {}),
        )
        self.workflow_registry[workflow.workflow_id] = workflow
        state, created = self.run_store.reserve(state)
        if state.status != WorkflowRunStatus.RUNNING:
            return self._run_summary(state, workflow, replayed=True)
        claimed = self.run_store.claim(
            state.run_id,
            tenant_id=self.tenant_id,
            worker_id=self.worker_id,
        )
        if claimed is None:
            return self._run_summary(state, workflow, replayed=not created)
        try:
            self._advance_workflow(claimed, workflow, actor=actor)
            return self._run_summary(claimed, workflow, replayed=not created)
        finally:
            self.run_store.release(
                state.run_id,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )

    def approve_and_execute(self, *, task_id: str, approved_by: str) -> AgentTask:
        """Human approves a pending task — orchestrator runs it."""
        existing = self.queue.get(task_id, tenant_id=self.tenant_id)
        if existing is None:
            raise KeyError(f"unknown task: {task_id}")
        run_id = existing.correlation_id or ""
        claimed = None
        if run_id:
            claimed = self.run_store.claim(
                run_id,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )
            if claimed is None:
                raise ValueError(f"workflow run is already claimed: {run_id}")
        try:
            was_awaiting = existing.status == TaskStatus.AWAITING_APPROVAL
            already_approved = (
                existing.status
                in {TaskStatus.APPROVED, TaskStatus.EXECUTING, TaskStatus.SUCCEEDED}
                and existing.approved_by == approved_by
            )
            task = (
                existing
                if already_approved
                else self.queue.approve(
                    task_id,
                    approved_by=approved_by,
                    tenant_id=self.tenant_id,
                )
            )
            if was_awaiting:
                self._emit_event(
                    customer_id=task.customer_id,
                    event_type="agent.action_approved",
                    actor=approved_by,
                    correlation_id=task.correlation_id,
                    payload={"agent_id": task.agent_id, "task_id": task_id},
                )
            if task.status != TaskStatus.SUCCEEDED:
                self._execute_task(
                    task,
                    actor=approved_by,
                    correlation_id=task.correlation_id,
                )
            task = self.queue.get(task_id, tenant_id=self.tenant_id) or task
            self._resume_after_task(task, actor=approved_by)
            return task
        finally:
            if claimed is not None:
                self.run_store.release(
                    run_id,
                    tenant_id=self.tenant_id,
                    worker_id=self.worker_id,
                )

    def reject_task(self, *, task_id: str, rejected_by: str, reason: str = "") -> AgentTask:
        existing = self.queue.get(task_id, tenant_id=self.tenant_id)
        if existing is None:
            raise KeyError(f"unknown task: {task_id}")
        run_id = existing.correlation_id or ""
        claimed = None
        if run_id:
            claimed = self.run_store.claim(
                run_id,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )
            if claimed is None:
                raise ValueError(f"workflow run is already claimed: {run_id}")
        try:
            task = self.queue.reject(
                task_id,
                rejected_by=rejected_by,
                reason=reason,
                tenant_id=self.tenant_id,
            )
            self._emit_event(
                customer_id=task.customer_id,
                event_type="agent.action_rejected",
                actor=rejected_by,
                correlation_id=task.correlation_id,
                payload={"agent_id": task.agent_id, "task_id": task_id, "reason": reason},
            )
            state = claimed or self.run_store.get(run_id, tenant_id=self.tenant_id)
            if state is not None and state.awaiting_task_id == task.task_id:
                state.status = WorkflowRunStatus.REJECTED
                state.failure_reason = reason or "approval_rejected"
                state.awaiting_task_id = None
                self.run_store.save(state)
            return task
        finally:
            if claimed is not None:
                self.run_store.release(
                    run_id,
                    tenant_id=self.tenant_id,
                    worker_id=self.worker_id,
                )

    def get_workflow_run(self, run_id: str) -> dict[str, Any]:
        state = self.run_store.get(run_id, tenant_id=self.tenant_id)
        if state is None:
            raise KeyError(f"workflow run not found: {run_id}")
        workflow = self.workflow_registry.get(state.workflow_id)
        if workflow is None:
            raise KeyError(f"workflow definition not found: {state.workflow_id}")
        return self._run_summary(state, workflow, replayed=False)

    def retry_workflow(self, *, run_id: str, actor: str = "system") -> dict[str, Any]:
        state = self.run_store.claim(
            run_id,
            tenant_id=self.tenant_id,
            worker_id=self.worker_id,
        )
        if state is None:
            existing = self.run_store.get(run_id, tenant_id=self.tenant_id)
            if existing is None:
                raise KeyError(f"workflow run not found: {run_id}")
            raise ValueError(f"workflow run is already claimed: {run_id}")
        try:
            if state.status != WorkflowRunStatus.RETRY_PENDING or not state.awaiting_task_id:
                raise ValueError(f"run {run_id} is not retryable (status={state.status})")
            task = self.queue.get(state.awaiting_task_id, tenant_id=self.tenant_id)
            if task is None:
                raise KeyError(f"workflow task not found: {state.awaiting_task_id}")
            result = self._execute_task(task, actor=actor, correlation_id=run_id)
            task = self.queue.get(task.task_id, tenant_id=self.tenant_id) or task
            if result is not None:
                self._record_step_success(state, task, result)
                workflow = self.workflow_registry[state.workflow_id]
                self._advance_workflow(state, workflow, actor=actor)
            elif task.status == TaskStatus.FAILED:
                state.status = WorkflowRunStatus.FAILED
                state.failure_reason = task.error or "task_failed"
                self.run_store.save(state)
            workflow = self.workflow_registry[state.workflow_id]
            return self._run_summary(state, workflow, replayed=False)
        finally:
            self.run_store.release(
                run_id,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )

    # ── Internal ─────────────────────────────────────────────
    def _advance_workflow(
        self,
        state: WorkflowRunState,
        workflow: WorkflowDefinition,
        *,
        actor: str,
    ) -> None:
        policy = self.policy_resolver(state.customer_id)
        usage = self.budget_usage.setdefault(state.customer_id, BudgetUsage())
        state.status = WorkflowRunStatus.RUNNING

        while state.next_step_index < len(workflow.steps):
            step = workflow.steps[state.next_step_index]
            missing_dependencies = [
                dependency
                for dependency in step.inputs_from
                if dependency not in state.outputs
            ]
            if missing_dependencies:
                state.status = WorkflowRunStatus.FAILED
                state.failure_reason = (
                    "upstream_not_completed:" + ",".join(missing_dependencies)
                )
                self.run_store.save(state)
                return

            step_inputs = {
                dependency: state.outputs[dependency]
                for dependency in step.inputs_from
            }
            if not step.inputs_from and state.initial_inputs:
                step_inputs["initial"] = state.initial_inputs

            risk_context: dict[str, Any] = dict(state.initial_inputs)
            for upstream_output in step_inputs.values():
                if isinstance(upstream_output, dict):
                    risk_context.update(upstream_output)
            risks = {
                "is_first_send_to_account": risk_context.get(
                    "is_first_send_to_account", False
                ),
                "deal_value_sar": risk_context.get("deal_value_sar", 0),
                "contains_legal_topic": risk_context.get(
                    "contains_legal_topic", False
                ),
                "sector": risk_context.get("sector"),
                "draft_text": risk_context.get("draft_text", ""),
                "consecutive_followup_index": risk_context.get(
                    "consecutive_followup_index", 0
                ),
            }
            needs_approval, reason = requires_approval(
                action_type=step.action_type,
                policy=policy,
                risk_factors=risks,
            )

            ok, budget_reason = within_budget(usage=usage, budget=policy.budget)
            if not ok:
                state.status = WorkflowRunStatus.FAILED
                state.failure_reason = f"budget:{budget_reason}"
                log.warning("budget_exhausted: %s", budget_reason)
                self._emit_event(
                    customer_id=state.customer_id,
                    event_type="agent.action_rejected",
                    actor=actor,
                    correlation_id=state.run_id,
                    payload={
                        "agent_id": step.agent_id,
                        "step_id": step.step_id,
                        "reason": state.failure_reason,
                    },
                )
                self.run_store.save(state)
                return

            task = self.queue.enqueue(
                tenant_id=state.tenant_id,
                customer_id=state.customer_id,
                agent_id=step.agent_id,
                action_type=step.action_type,
                payload={"step_id": step.step_id, "inputs": step_inputs},
                requires_approval=needs_approval,
                approval_reason=reason,
                correlation_id=state.run_id,
                parent_workflow_id=workflow.workflow_id,
            )
            if task.task_id not in state.task_ids:
                state.task_ids.append(task.task_id)
            self._emit_event(
                customer_id=state.customer_id,
                event_type="agent.action_requested",
                actor=actor,
                correlation_id=state.run_id,
                payload={
                    "agent_id": step.agent_id,
                    "task_id": task.task_id,
                    "step_id": step.step_id,
                    "requires_approval": needs_approval,
                    "approval_reason": reason,
                },
            )

            # Crash recovery: the task outcome can commit before the workflow
            # snapshot. Reuse that durable result instead of calling a provider
            # a second time.
            if task.status == TaskStatus.SUCCEEDED and task.result is not None:
                self._record_step_success(state, task, task.result)
                continue
            if task.status in {
                TaskStatus.FAILED,
                TaskStatus.REJECTED,
                TaskStatus.CANCELLED,
            }:
                state.status = WorkflowRunStatus.FAILED
                state.awaiting_task_id = task.task_id
                state.failure_reason = task.error or f"task_{task.status}"
                self.run_store.save(state)
                return
            if task.status == TaskStatus.EXECUTING:
                state.status = WorkflowRunStatus.RETRY_PENDING
                state.awaiting_task_id = task.task_id
                self.run_store.save(state)
                return

            if needs_approval and task.status == TaskStatus.AWAITING_APPROVAL:
                state.status = WorkflowRunStatus.AWAITING_APPROVAL
                state.awaiting_task_id = task.task_id
                self.run_store.save(state)
                return

            result = self._execute_task(
                task,
                actor=actor,
                correlation_id=state.run_id,
            )
            task = self.queue.get(task.task_id, tenant_id=self.tenant_id) or task
            if result is not None:
                self._record_step_success(state, task, result)
                continue
            state.awaiting_task_id = task.task_id
            if task.status == TaskStatus.PENDING:
                state.status = WorkflowRunStatus.RETRY_PENDING
            else:
                state.status = WorkflowRunStatus.FAILED
                state.failure_reason = task.error or "task_failed"
            self.run_store.save(state)
            return

        state.status = WorkflowRunStatus.COMPLETED
        state.awaiting_task_id = None
        self._finalize_run(state)
        self.run_store.save(state)

    def _record_step_success(
        self,
        state: WorkflowRunState,
        task: AgentTask,
        result: dict[str, Any],
    ) -> None:
        step_id = str(task.payload.get("step_id") or "")
        if not step_id:
            raise ValueError("workflow task is missing step_id")
        if step_id not in state.completed_steps:
            state.completed_steps.append(step_id)
        state.outputs[step_id] = result
        state.next_step_index += 1
        state.awaiting_task_id = None
        state.failure_reason = None
        self.run_store.save(state)

    def _resume_after_task(self, task: AgentTask, *, actor: str) -> None:
        state = self.run_store.claim(
            task.correlation_id or "",
            tenant_id=self.tenant_id,
            worker_id=self.worker_id,
        )
        if state is None or state.awaiting_task_id != task.task_id:
            return
        try:
            if task.status == TaskStatus.SUCCEEDED and task.result is not None:
                self._record_step_success(state, task, task.result)
                workflow = self.workflow_registry.get(state.workflow_id)
                if workflow is None:
                    state.status = WorkflowRunStatus.FAILED
                    state.failure_reason = "workflow_definition_not_registered"
                    self.run_store.save(state)
                    return
                self._advance_workflow(state, workflow, actor=actor)
                return
            if task.status == TaskStatus.PENDING:
                state.status = WorkflowRunStatus.RETRY_PENDING
            else:
                state.status = WorkflowRunStatus.FAILED
                state.failure_reason = task.error or "task_failed"
            self.run_store.save(state)
        finally:
            self.run_store.release(
                state.run_id,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )

    def _run_summary(
        self,
        state: WorkflowRunState,
        workflow: WorkflowDefinition,
        *,
        replayed: bool,
    ) -> dict[str, Any]:
        tasks = [
            task
            for task_id in state.task_ids
            if (task := self.queue.get(task_id, tenant_id=self.tenant_id)) is not None
        ]
        deferred_steps = [
            step.step_id
            for step in workflow.steps[state.next_step_index + 1 :]
        ] if state.status in {
            WorkflowRunStatus.AWAITING_APPROVAL,
            WorkflowRunStatus.RETRY_PENDING,
        } else []
        blocked_steps = []
        if state.status in {WorkflowRunStatus.FAILED, WorkflowRunStatus.REJECTED}:
            blocked_steps = [
                {
                    "step_id": step.step_id,
                    "reason": state.failure_reason or state.status,
                }
                for step in workflow.steps[state.next_step_index + 1 :]
            ]
        return {
            "workflow_id": state.workflow_id,
            "correlation_id": state.run_id,
            "customer_id": state.customer_id,
            "tenant_id": state.tenant_id,
            "idempotency_key": state.idempotency_key,
            "status": state.status,
            "replayed": replayed,
            "tasks_created": len(state.task_ids),
            "awaiting_approval": [
                task.task_id
                for task in tasks
                if task.status == TaskStatus.AWAITING_APPROVAL
            ],
            "succeeded": [
                task.task_id for task in tasks if task.status == TaskStatus.SUCCEEDED
            ],
            "failed": [
                task.task_id for task in tasks if task.status == TaskStatus.FAILED
            ],
            "completed_steps": list(state.completed_steps),
            "deferred_steps": deferred_steps,
            "blocked_steps": blocked_steps,
            "failure_reason": state.failure_reason,
            "finalized": state.finalized,
        }

    def _finalize_run(self, state: WorkflowRunState) -> None:
        """Record outcome, proof posture, and a non-self-applying learning signal."""
        if state.finalized:
            return
        tasks = [
            task
            for task_id in state.task_ids
            if (task := self.queue.get(task_id, tenant_id=self.tenant_id)) is not None
        ]
        outputs = list(state.outputs.values())
        synthetic_outputs = sum(
            1 for output in outputs
            if output.get("execution_mode") == "synthetic_demo"
        )
        source_refs = sorted(
            {
                str(output["source_ref"])
                for output in outputs
                if output.get("source_ref")
            }
        )
        external_tasks = [
            task.task_id
            for task in tasks
            if task.action_type in EXTERNAL_ACTION_TYPES
            and task.status == TaskStatus.SUCCEEDED
        ]
        retries = sum(task.retries for task in tasks)

        for event_type, payload in (
            (
                "workflow.outcome_recorded",
                {
                    "workflow_id": state.workflow_id,
                    "status": state.status,
                    "completed_steps": len(state.completed_steps),
                    "external_tasks_executed": external_tasks,
                },
            ),
            (
                "workflow.proof_recorded",
                {
                    "synthetic_outputs": synthetic_outputs,
                    "source_refs": source_refs,
                    "claimable_external": bool(source_refs) and synthetic_outputs == 0,
                    "evidence_level": "L0" if synthetic_outputs else "unverified",
                },
            ),
            (
                "workflow.learning_proposed",
                {
                    "retry_count": retries,
                    "proposal": (
                        "review_retried_steps"
                        if retries
                        else "maintain_governed_execution_path"
                    ),
                    "auto_applied": False,
                },
            ),
        ):
            self._emit_event(
                customer_id=state.customer_id,
                event_type=event_type,
                actor="system",
                correlation_id=state.run_id,
                payload={"run_id": state.run_id, **payload},
            )
        state.finalized = True

    def _execute_task(
        self,
        task: AgentTask,
        *,
        actor: str,
        correlation_id: str | None,
    ) -> dict[str, Any] | None:
        executor = self.executor_registry.get(task.action_type)
        if executor is None:
            self.queue.fail(
                task.task_id,
                error=f"no executor for {task.action_type}",
                retryable=False,
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )
            self._emit_event(
                customer_id=task.customer_id,
                event_type="agent.action_failed",
                actor=actor,
                correlation_id=correlation_id,
                payload={"task_id": task.task_id, "error": "no_executor"},
            )
            return None

        task = self.queue.mark_executing(
            task.task_id,
            tenant_id=self.tenant_id,
            worker_id=self.worker_id,
        )
        try:
            result = executor(task)
        except Exception as exc:
            task = self.queue.fail(
                task.task_id,
                error=str(exc)[:500],
                tenant_id=self.tenant_id,
                worker_id=self.worker_id,
            )
            self._emit_event(
                customer_id=task.customer_id,
                event_type="agent.action_failed",
                actor=actor,
                correlation_id=correlation_id,
                payload={
                    "task_id": task.task_id,
                    "error": str(exc)[:500],
                    "retries": task.retries,
                },
            )
            return None

        # Persist the provider outcome before secondary telemetry. A failed
        # outcome write is not misclassified as an executor failure; replay
        # uses the stable provider idempotency key on the task.
        task = self.queue.succeed(
            task.task_id,
            result=result,
            tenant_id=self.tenant_id,
            worker_id=self.worker_id,
        )
        try:
            self._emit_event(
                customer_id=task.customer_id,
                event_type="agent.action_executed",
                actor=actor,
                correlation_id=correlation_id,
                payload={
                    "agent_id": task.agent_id,
                    "task_id": task.task_id,
                    "action_type": task.action_type,
                },
            )
        except Exception:
            log.exception("task outcome persisted but execution event emission failed")
        usage = self.budget_usage.setdefault(task.customer_id, BudgetUsage())
        if task.action_type == "send_message":
            usage.messages_today += 1
        usage.api_calls_today += 1
        return result

    def _emit_event(
        self,
        *,
        customer_id: str,
        event_type: str,
        actor: str,
        correlation_id: str | None,
        payload: dict[str, Any],
    ) -> None:
        e = make_event(
            event_type=event_type,
            customer_id=customer_id,
            subject_type="agent_task",
            subject_id=payload.get("task_id", payload.get("step_id", "unknown")),
            payload=payload,
            actor=actor,
            correlation_id=correlation_id,
        )
        self.event_store.append(e)
