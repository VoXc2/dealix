"""Schemas for System 26 — the Organizational Control Plane."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.control_plane_os.ledger import ControlEvent


class RunState(StrEnum):
    """Lifecycle of a workflow run under control-plane supervision."""

    REGISTERED = "registered"
    RUNNING = "running"
    PAUSED = "paused"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    REROUTED = "rerouted"
    COMPLETED = "completed"
    FAILED = "failed"


def _run_id() -> str:
    return f"run_{uuid4().hex[:12]}"


class WorkflowRun(BaseModel):
    """A workflow run tracked by the control plane."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    run_id: str = Field(default_factory=_run_id)
    workflow_id: str
    customer_id: str
    state: RunState = RunState.REGISTERED
    correlation_id: str | None = None
    current_step: str | None = None
    parent_run_id: str | None = None
    attached_policy_ids: list[str] = Field(default_factory=list)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class RunStatus(BaseModel):
    """Live snapshot of a run — what `monitor` returns."""

    model_config = ConfigDict(extra="forbid")

    run: WorkflowRun
    task_summary: dict[str, int] = Field(default_factory=dict)
    events_count: int = 0
    awaiting_approval: list[str] = Field(default_factory=list)


class RunTrace(BaseModel):
    """Full event timeline for a run — what `trace` returns."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    events: list[ControlEvent] = Field(default_factory=list)
    timeline: list[dict[str, Any]] = Field(default_factory=list)


class PolicyEdit(BaseModel):
    """A request to live-edit a policy attached to a run.

    Never applied directly — always routed through the approval gate.
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str
    policy_id: str
    change: dict[str, Any]
    editor: str
