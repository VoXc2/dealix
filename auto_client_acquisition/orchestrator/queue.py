"""
Task Queue — agent task lifecycle: requested → approved → executed → done/failed.

Each task is auditable, replayable, and revocable (if not yet executed).
The queue is in-memory by default; pass a ``path`` (or use
``load_task_queue``) to snapshot it to disk so an interrupted run can be
**resumed** after a restart. ``enqueue`` accepts an ``idempotency_key`` so a
retried request never creates a duplicate task.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
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

_TERMINAL: frozenset[str] = frozenset(
    {TaskStatus.SUCCEEDED, TaskStatus.FAILED, TaskStatus.CANCELLED, TaskStatus.REJECTED}
)

_DEFAULT_PATH = "var/task-queue.json"
_lock = threading.Lock()


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


@dataclass
class AgentTask:
    """Single agent task — full lifecycle tracked."""

    task_id: str
    customer_id: str
    agent_id: str            # which of the 11 agents
    action_type: str         # one of orchestrator.policies.ACTION_TYPES
    payload: dict[str, Any]
    status: str = TaskStatus.PENDING
    requires_approval: bool = False
    approval_reason: str | None = None
    correlation_id: str | None = None
    causation_task_id: str | None = None
    parent_workflow_id: str | None = None
    idempotency_key: str | None = None
    created_at: datetime = field(default_factory=_now)
    approved_at: datetime | None = None
    approved_by: str | None = None
    executed_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    result: dict[str, Any] | None = None
    retries: int = 0
    max_retries: int = 2


_DT_FIELDS = ("created_at", "approved_at", "executed_at", "completed_at")


def _task_to_dict(task: AgentTask) -> dict[str, Any]:
    out = dict(task.__dict__)
    for f in _DT_FIELDS:
        val = out.get(f)
        out[f] = val.isoformat() if isinstance(val, datetime) else None
    return out


def _task_from_dict(data: dict[str, Any]) -> AgentTask:
    data = dict(data)
    for f in _DT_FIELDS:
        raw = data.get(f)
        data[f] = datetime.fromisoformat(raw) if raw else None
    if data.get("created_at") is None:
        data["created_at"] = _now()
    return AgentTask(**data)


@dataclass
class TaskQueue:
    """Task queue. Pass ``path`` to snapshot to disk for crash-resumability."""

    tasks: dict[str, AgentTask] = field(default_factory=dict)
    path: Path | None = None
    idempotency_index: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.path is not None and not self.tasks:
            self._load()

    def enqueue(
        self,
        *,
        customer_id: str,
        agent_id: str,
        action_type: str,
        payload: dict[str, Any] | None = None,
        requires_approval: bool = False,
        approval_reason: str | None = None,
        correlation_id: str | None = None,
        causation_task_id: str | None = None,
        parent_workflow_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> AgentTask:
        # Idempotency — a retried request returns the existing task.
        if idempotency_key and idempotency_key in self.idempotency_index:
            existing = self.tasks.get(self.idempotency_index[idempotency_key])
            if existing is not None:
                return existing
        task = AgentTask(
            task_id=f"tsk_{uuid.uuid4().hex[:24]}",
            customer_id=customer_id,
            agent_id=agent_id,
            action_type=action_type,
            payload=payload or {},
            requires_approval=requires_approval,
            approval_reason=approval_reason,
            correlation_id=correlation_id,
            causation_task_id=causation_task_id,
            parent_workflow_id=parent_workflow_id,
            idempotency_key=idempotency_key,
            status=TaskStatus.AWAITING_APPROVAL if requires_approval else TaskStatus.PENDING,
        )
        self.tasks[task.task_id] = task
        if idempotency_key:
            self.idempotency_index[idempotency_key] = task.task_id
        self._persist()
        return task

    def approve(self, task_id: str, *, approved_by: str) -> AgentTask:
        task = self._get(task_id)
        if task.status != TaskStatus.AWAITING_APPROVAL:
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        task.status = TaskStatus.APPROVED
        task.approved_at = _now()
        task.approved_by = approved_by
        self._persist()
        return task

    def reject(self, task_id: str, *, rejected_by: str, reason: str = "") -> AgentTask:
        task = self._get(task_id)
        if task.status != TaskStatus.AWAITING_APPROVAL:
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        task.status = TaskStatus.REJECTED
        task.completed_at = _now()
        task.approved_by = rejected_by
        task.error = f"rejected: {reason}" if reason else "rejected"
        self._persist()
        return task

    def cancel(self, task_id: str) -> AgentTask:
        task = self._get(task_id)
        if task.status in _TERMINAL:
            raise ValueError(f"task {task_id} is already terminal (status={task.status})")
        task.status = TaskStatus.CANCELLED
        task.completed_at = _now()
        self._persist()
        return task

    def mark_executing(self, task_id: str) -> AgentTask:
        task = self._get(task_id)
        if task.status not in (TaskStatus.PENDING, TaskStatus.APPROVED):
            raise ValueError(f"cannot execute task in status={task.status}")
        task.status = TaskStatus.EXECUTING
        task.executed_at = _now()
        self._persist()
        return task

    def succeed(self, task_id: str, *, result: dict[str, Any]) -> AgentTask:
        task = self._get(task_id)
        task.status = TaskStatus.SUCCEEDED
        task.result = result
        task.completed_at = _now()
        self._persist()
        return task

    def fail(self, task_id: str, *, error: str) -> AgentTask:
        task = self._get(task_id)
        task.error = error
        if task.retries < task.max_retries:
            task.retries += 1
            task.status = TaskStatus.PENDING
        else:
            task.status = TaskStatus.FAILED
            task.completed_at = _now()
        self._persist()
        return task

    # ── Resumability ──────────────────────────────────────────
    def resumable(self) -> list[AgentTask]:
        """Non-terminal tasks — what a worker picks up after a restart."""
        return [t for t in self.tasks.values() if t.status not in _TERMINAL]

    # ── Query API ─────────────────────────────────────────────
    def by_status(self, status: str) -> list[AgentTask]:
        return [t for t in self.tasks.values() if t.status == status]

    def for_customer(self, customer_id: str) -> list[AgentTask]:
        return [t for t in self.tasks.values() if t.customer_id == customer_id]

    def for_workflow(self, workflow_id: str) -> list[AgentTask]:
        return [t for t in self.tasks.values() if t.parent_workflow_id == workflow_id]

    def summary(self, customer_id: str | None = None) -> dict[str, int]:
        out: dict[str, int] = dict.fromkeys(ALL_STATUSES, 0)
        for t in self.tasks.values():
            if customer_id and t.customer_id != customer_id:
                continue
            out[t.status] = out.get(t.status, 0) + 1
        return out

    # ── Persistence ───────────────────────────────────────────
    def _persist(self) -> None:
        if self.path is None:
            return
        snapshot = {
            "tasks": {tid: _task_to_dict(t) for tid, t in self.tasks.items()},
            "idempotency_index": self.idempotency_index,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with _lock, self.path.open("w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False)

    def _load(self) -> None:
        if self.path is None or not self.path.exists():
            return
        with _lock, self.path.open("r", encoding="utf-8") as f:
            try:
                snapshot = json.load(f)
            except Exception:
                return
        self.tasks = {
            tid: _task_from_dict(d) for tid, d in snapshot.get("tasks", {}).items()
        }
        self.idempotency_index = dict(snapshot.get("idempotency_index", {}))

    def _get(self, task_id: str) -> AgentTask:
        if task_id not in self.tasks:
            raise KeyError(f"unknown task: {task_id}")
        return self.tasks[task_id]


def _resolve_path(path: Path | str | None) -> Path:
    p = Path(path or os.environ.get("DEALIX_TASK_QUEUE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # queue.py → orchestrator → auto_client_acquisition → repo root
        p = Path(__file__).resolve().parents[2] / p
    return p


def load_task_queue(path: Path | str | None = None) -> TaskQueue:
    """Load a disk-snapshotted task queue (resumes any non-terminal tasks)."""
    return TaskQueue(path=_resolve_path(path))


def clear_for_test(path: Path | str | None = None) -> None:
    """Test-only: delete the queue snapshot."""
    p = _resolve_path(path)
    if p.exists():
        with _lock:
            p.unlink()


__all__ = [
    "ALL_STATUSES",
    "AgentTask",
    "TaskQueue",
    "TaskStatus",
    "clear_for_test",
    "load_task_queue",
]
