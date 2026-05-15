"""Typed contracts for the enterprise workflow foundation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

RiskLevel = Literal["low", "medium", "high"]
GovernanceDecision = Literal["allow", "require_approval", "block"]
RunStatus = Literal["completed", "failed", "paused_for_approval", "rolled_back"]


@dataclass(frozen=True, slots=True)
class AgentSpec:
    """Minimal runtime contract for an operational agent."""

    name: str
    version: str
    risk_level: RiskLevel
    allowed_tools: tuple[str, ...]
    requires_approval_for: tuple[str, ...]
    memory_scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """One executable step in a workflow definition."""

    step_id: str
    name: str
    action: str
    risk_level: RiskLevel
    max_retries: int = 1
    requires_approval: bool = False
    estimated_value_sar: int = 0
    rollback_on_failure: bool = True


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """Workflow definition loaded from YAML."""

    workflow_id: str
    name: str
    trigger: str
    steps: tuple[WorkflowStep, ...]


@dataclass(frozen=True, slots=True)
class GovernanceOutcome:
    """Decision returned by governance evaluation per action."""

    decision: GovernanceDecision
    risk_score: int
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class StepTrace:
    """Per-step execution trace for observability and audit."""

    step_id: str
    action: str
    decision: GovernanceDecision
    status: str
    attempt: int
    risk_score: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass(frozen=True, slots=True)
class WorkflowRunMetrics:
    """Execution metrics suitable for observability and executive reporting."""

    total_steps: int
    completed_steps: int
    retries_total: int
    approvals_requested: int
    approvals_granted: int
    value_generated_sar: int
    rollback_events: int
    duration_ms: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class WorkflowRunResult:
    """Final workflow run output."""

    run_id: str
    workflow_id: str
    status: RunStatus
    tenant_id: str
    actor_role: str
    blocked_step_id: str | None
    traces: tuple[StepTrace, ...]
    audit_log: tuple[dict[str, Any], ...]
    metrics: WorkflowRunMetrics

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "status": self.status,
            "tenant_id": self.tenant_id,
            "actor_role": self.actor_role,
            "blocked_step_id": self.blocked_step_id,
            "traces": [trace.to_dict() for trace in self.traces],
            "audit_log": [dict(item) for item in self.audit_log],
            "metrics": self.metrics.to_dict(),
        }


def new_run_id() -> str:
    return f"ent_run_{uuid4().hex[:12]}"
