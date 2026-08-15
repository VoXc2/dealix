"""
Task Queue — agent tasks lifecycle: requested → approved → executed → done/failed.

Each task is auditable + replayable + revocable (if not yet executed).
The queue is in-memory; production uses a SQL-backed adapter with the
same Protocol.
"""

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


class TaskStatus:
    PENDING = "pending"           # waiting in queue
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALL_STATUSES: tuple[str, ...] = (
    TaskStatus.PENDING,
    TaskStatus.AWAITING_APPROVAL,
    TaskStatus.APPROVED,
    TaskStatus.REJECTED,
    TaskStatus.EXECUTING,
    TaskStatus.SUCCEEDED,
    TaskStatus.FAILED,
    TaskStatus.CANCELLED,
)


def task_id_for(
    *,
    tenant_id: str,
    correlation_id: str | None,
    step_id: str | None,
) -> str:
    """Return a stable task id for a workflow step, or a random id ad hoc work."""
    if correlation_id and step_id:
        digest = sha256(f"{tenant_id}:{correlation_id}:{step_id}".encode()).hexdigest()[:24]
        return f"tsk_{digest}"
    return f"tsk_{uuid.uuid4().hex[:24]}"


@dataclass
class AgentTask:
    """Single agent task — full lifecycle tracked."""

    task_id: str
    customer_id: str
    agent_id: str            # which of the 11 agents
    action_type: str         # one of orchestrator.policies.ACTION_TYPES
    payload: dict[str, Any]
    tenant_id: str = "default"
    status: str = TaskStatus.PENDING
    requires_approval: bool = False
    approval_reason: str | None = None
    correlation_id: str | None = None
    causation_task_id: str | None = None
    parent_workflow_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))
    approved_at: datetime | None = None
    approved_by: str | None = None
    executed_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    result: dict[str, Any] | None = None
    retries: int = 0
    max_retries: int = 2

    @property
    def execution_idempotency_key(self) -> str:
        """Stable key external providers must receive to suppress duplicate effects."""
        return f"dealix:{self.tenant_id}:{self.task_id}"


@dataclass
class TaskQueue:
    """Lightweight in-memory task queue."""

    tasks: dict[str, AgentTask] = field(default_factory=dict)

    def enqueue(
        self,
        *,
        tenant_id: str = "default",
        customer_id: str,
        agent_id: str,
        action_type: str,
        payload: dict[str, Any] | None = None,
        requires_approval: bool = False,
        approval_reason: str | None = None,
        correlation_id: str | None = None,
        causation_task_id: str | None = None,
        parent_workflow_id: str | None = None,
    ) -> AgentTask:
        task_id = task_id_for(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            step_id=str((payload or {}).get("step_id") or "") or None,
        )
        existing = self.tasks.get(task_id)
        if existing is not None:
            if existing.tenant_id != tenant_id:
                raise ValueError("cross-tenant task id collision")
            return existing
        task = AgentTask(
            task_id=task_id,
            tenant_id=tenant_id,
            customer_id=customer_id,
            agent_id=agent_id,
            action_type=action_type,
            payload=payload or {},
            requires_approval=requires_approval,
            approval_reason=approval_reason,
            correlation_id=correlation_id,
            causation_task_id=causation_task_id,
            parent_workflow_id=parent_workflow_id,
            status=TaskStatus.AWAITING_APPROVAL if requires_approval else TaskStatus.PENDING,
        )
        self.tasks[task.task_id] = task
        self._persist()
        return task

    def approve(
        self,
        task_id: str,
        *,
        approved_by: str,
        tenant_id: str | None = None,
    ) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        if task.status != TaskStatus.AWAITING_APPROVAL:
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        task.status = TaskStatus.APPROVED
        task.approved_at = datetime.now(UTC).replace(tzinfo=None)
        task.approved_by = approved_by
        self._persist()
        return task

    def reject(
        self,
        task_id: str,
        *,
        rejected_by: str,
        reason: str = "",
        tenant_id: str | None = None,
    ) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        if task.status != TaskStatus.AWAITING_APPROVAL:
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        task.status = TaskStatus.REJECTED
        task.completed_at = datetime.now(UTC).replace(tzinfo=None)
        task.approved_by = rejected_by
        task.error = f"rejected: {reason}" if reason else "rejected"
        self._persist()
        return task

    def cancel(self, task_id: str, *, tenant_id: str | None = None) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        if task.status in (TaskStatus.SUCCEEDED, TaskStatus.FAILED, TaskStatus.CANCELLED):
            raise ValueError(f"task {task_id} is already terminal (status={task.status})")
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now(UTC).replace(tzinfo=None)
        self._persist()
        return task

    def mark_executing(
        self,
        task_id: str,
        *,
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        if task.status not in (TaskStatus.PENDING, TaskStatus.APPROVED):
            raise ValueError(f"cannot execute task in status={task.status}")
        task.status = TaskStatus.EXECUTING
        task.executed_at = datetime.now(UTC).replace(tzinfo=None)
        self._persist()
        return task

    def succeed(
        self,
        task_id: str,
        *,
        result: dict[str, Any],
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        task.status = TaskStatus.SUCCEEDED
        task.result = result
        task.completed_at = datetime.now(UTC).replace(tzinfo=None)
        self._persist()
        return task

    def fail(
        self,
        task_id: str,
        *,
        error: str,
        retryable: bool = True,
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        task = self._get(task_id, tenant_id=tenant_id)
        task.error = error
        if retryable and task.retries < task.max_retries:
            task.retries += 1
            task.status = TaskStatus.PENDING
        else:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now(UTC).replace(tzinfo=None)
        self._persist()
        return task

    # ── Query API ─────────────────────────────────────────────
    def by_status(self, status: str, *, tenant_id: str | None = None) -> list[AgentTask]:
        return [
            t for t in self.tasks.values()
            if t.status == status and (tenant_id is None or t.tenant_id == tenant_id)
        ]

    def for_customer(
        self,
        customer_id: str,
        *,
        tenant_id: str | None = None,
    ) -> list[AgentTask]:
        return [
            t for t in self.tasks.values()
            if t.customer_id == customer_id and (tenant_id is None or t.tenant_id == tenant_id)
        ]

    def for_workflow(
        self,
        workflow_id: str,
        *,
        tenant_id: str | None = None,
    ) -> list[AgentTask]:
        return [
            t for t in self.tasks.values()
            if t.parent_workflow_id == workflow_id
            and (tenant_id is None or t.tenant_id == tenant_id)
        ]

    def get(self, task_id: str, *, tenant_id: str | None = None) -> AgentTask | None:
        task = self.tasks.get(task_id)
        if task is not None and tenant_id is not None and task.tenant_id != tenant_id:
            return None
        return task

    def summary(
        self,
        customer_id: str | None = None,
        *,
        tenant_id: str | None = None,
    ) -> dict[str, int]:
        out: dict[str, int] = dict.fromkeys(ALL_STATUSES, 0)
        for t in self.tasks.values():
            if customer_id and t.customer_id != customer_id:
                continue
            if tenant_id is not None and t.tenant_id != tenant_id:
                continue
            out[t.status] = out.get(t.status, 0) + 1
        return out

    def _get(self, task_id: str, *, tenant_id: str | None = None) -> AgentTask:
        task = self.get(task_id, tenant_id=tenant_id)
        if task is None:
            raise KeyError(f"unknown task: {task_id}")
        return task

    def _persist(self) -> None:
        """Persistence hook used by durable queue adapters."""


class JsonTaskQueue(TaskQueue):
    """Atomic JSON-backed queue for restart-safe single-node deployments."""

    backend_name = "json"

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        super().__init__(tasks=self._load())

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        return datetime.fromisoformat(value) if value else None

    def _load(self) -> dict[str, AgentTask]:
        if not self._path.is_file():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        tasks: dict[str, AgentTask] = {}
        for task_id, payload in (raw.get("tasks") or {}).items():
            if not isinstance(payload, dict):
                continue
            row = dict(payload)
            row.setdefault("tenant_id", "default")
            for key in (
                "created_at",
                "approved_at",
                "executed_at",
                "completed_at",
            ):
                row[key] = self._parse_datetime(row.get(key))
            tasks[task_id] = AgentTask(**row)
        return tasks

    def _persist(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {"tasks": {}}
        for task_id, task in self.tasks.items():
            row = asdict(task)
            for key in (
                "created_at",
                "approved_at",
                "executed_at",
                "completed_at",
            ):
                value = row.get(key)
                row[key] = value.isoformat() if value else None
            payload["tasks"][task_id] = row
        temp_path = self._path.with_suffix(self._path.suffix + ".tmp")
        temp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temp_path, self._path)
