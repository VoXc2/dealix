"""
Workflow definition + run state.

A workflow is a *deterministic* ordered list of steps. Each step binds a
typed tool to an input-mapping function that projects the run context onto
the tool's input. There is no autonomous branching at this layer — agents
run *inside* steps, they do not replace the workflow.

This is intentionally the simplest thing that works (no Temporal clone):
a list of steps + a context object + an engine that walks them.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

# An input mapper projects the run context onto a tool's input dict.
InputMapper = Callable[["WorkflowContext"], dict[str, Any]]


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"  # failed + rolled back


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    DENIED = "denied"  # blocked by policy
    SKIPPED = "skipped"
    COMPENSATED = "compensated"


def _utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class WorkflowStep:
    """One deterministic step: a tool + how to feed it."""

    name: str
    tool_name: str
    inputs: InputMapper
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "tool": self.tool_name, "description": self.description}


@dataclass(slots=True)
class WorkflowDefinition:
    """A named, versioned, deterministic workflow."""

    name: str
    version: str
    description: str
    trigger: str  # e.g. "webhook", "manual", "schedule"
    steps: list[WorkflowStep]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "trigger": self.trigger,
            "steps": [s.to_dict() for s in self.steps],
        }


@dataclass(slots=True)
class StepRecord:
    """Audit-grade record of a single step execution."""

    name: str
    tool_name: str
    status: StepStatus = StepStatus.PENDING
    policy_decision: str | None = None
    policy_rule: str | None = None
    approval_request_id: str | None = None
    attempts: int = 0
    duration_ms: float = 0.0
    output: dict[str, Any] = field(default_factory=dict)
    # Resolved tool input — kept for compensation; never serialised (may hold PII).
    resolved_input: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    compensated: bool = False
    started_at: datetime | None = None
    finished_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "tool": self.tool_name,
            "status": self.status.value,
            "policy_decision": self.policy_decision,
            "policy_rule": self.policy_rule,
            "approval_request_id": self.approval_request_id,
            "attempts": self.attempts,
            "duration_ms": round(self.duration_ms, 2),
            "error": self.error,
            "compensated": self.compensated,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }


@dataclass(slots=True)
class WorkflowContext:
    """Mutable run state threaded through every step.

    `step_outputs` accumulates each step's result so later steps' input
    mappers (and the policy evidence builder) can read upstream data.
    """

    run_id: str
    workflow_name: str
    workflow_version: str
    tenant_id: str
    entity_id: str
    trigger_payload: dict[str, Any]
    actor_id: str
    trace_id: str
    correlation_id: str

    status: RunStatus = RunStatus.PENDING
    current_step_index: int = 0
    step_outputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    step_records: list[StepRecord] = field(default_factory=list)
    pending_approval_id: str | None = None
    error: str | None = None
    started_at: datetime = field(default_factory=_utcnow)
    finished_at: datetime | None = None

    @staticmethod
    def new(
        workflow: WorkflowDefinition,
        *,
        tenant_id: str,
        entity_id: str,
        trigger_payload: dict[str, Any],
        actor_id: str,
        correlation_id: str | None = None,
    ) -> WorkflowContext:
        run_id = f"wfr_{uuid.uuid4().hex[:16]}"
        return WorkflowContext(
            run_id=run_id,
            workflow_name=workflow.name,
            workflow_version=workflow.version,
            tenant_id=tenant_id,
            entity_id=entity_id,
            trigger_payload=dict(trigger_payload),
            actor_id=actor_id,
            trace_id=f"trace_{uuid.uuid4().hex}",
            correlation_id=correlation_id or run_id,
        )

    @property
    def duration_ms(self) -> float:
        end = self.finished_at or _utcnow()
        return (end - self.started_at).total_seconds() * 1000.0

    @property
    def is_terminal(self) -> bool:
        return self.status in (
            RunStatus.COMPLETED,
            RunStatus.FAILED,
            RunStatus.COMPENSATED,
        )

    def output(self, step_name: str) -> dict[str, Any]:
        """Read an upstream step's output (empty dict if not yet run)."""
        return self.step_outputs.get(step_name, {})

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow": self.workflow_name,
            "workflow_version": self.workflow_version,
            "tenant_id": self.tenant_id,
            "entity_id": self.entity_id,
            "actor_id": self.actor_id,
            "status": self.status.value,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "current_step_index": self.current_step_index,
            "pending_approval_id": self.pending_approval_id,
            "error": self.error,
            "duration_ms": round(self.duration_ms, 2),
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "steps": [r.to_dict() for r in self.step_records],
            "step_outputs": self.step_outputs,
        }


__all__ = [
    "InputMapper",
    "RunStatus",
    "StepRecord",
    "StepStatus",
    "WorkflowContext",
    "WorkflowDefinition",
    "WorkflowStep",
]
