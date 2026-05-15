"""Schemas for enterprise control-plane runtime objects."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class ControlEvent:
    id: str
    tenant_id: str
    event_type: str
    source_module: str
    actor: str
    subject_type: str = ""
    subject_id: str = ""
    run_id: str = ""
    correlation_id: str = ""
    decision: str = ""
    occurred_at: str = field(default_factory=_now)
    payload: dict[str, Any] = field(default_factory=dict)
    redacted: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class WorkflowRun:
    run_id: str
    tenant_id: str
    workflow_id: str
    state: str
    actor: str
    customer_id: str = ""
    correlation_id: str = ""
    parent_run_id: str = ""
    current_step: str = ""
    attached_policy_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    registered_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ApprovalTicket:
    ticket_id: str
    tenant_id: str
    action_type: str
    description: str
    requested_by: str
    source_module: str
    state: str = "pending"
    subject_type: str = ""
    subject_id: str = ""
    run_id: str = ""
    granted_by: str = ""
    rejected_by: str = ""
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_now)
    resolved_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
