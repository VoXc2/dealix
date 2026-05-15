"""Typed records for the workflow_os_v10 state machine.

Temporal-style: states + steps + retry policy + idempotency keys +
checkpoint. Pure native Python — no Temporal SDK dependency.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

WorkflowState = Literal[
    "pending",
    "running",
    "paused_for_approval",
    "completed",
    "blocked",
    "failed",
    "retrying",
]


# Allowed state transitions for any individual workflow step.
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"running", "blocked"},
    "running": {
        "completed",
        "failed",
        "paused_for_approval",
        "retrying",
        "blocked",
    },
    "retrying": {"running", "failed", "blocked"},
    "paused_for_approval": {"running", "blocked"},
    "completed": set(),
    "failed": {"retrying"},  # only via the retry mechanism
    "blocked": set(),
}


class RetryPolicy(BaseModel):
    """Exponential-backoff retry policy."""

    model_config = ConfigDict(extra="forbid")

    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_delay_seconds: int = 60


class IdempotencyKey(BaseModel):
    """Wrapper for an idempotency key — strict equality."""

    model_config = ConfigDict(extra="forbid")

    key: str
    namespace: str = "default"

    def composite(self) -> str:
        return f"{self.namespace}::{self.key}"


class WorkflowStep(BaseModel):
    """One step in a workflow run."""

    model_config = ConfigDict(extra="forbid")

    name: str
    idempotency_key: str
    state: WorkflowState
    attempt: int = 0
    max_retries: int = 3
    retry_after_seconds: int = 60
    result: dict[str, Any] = Field(default_factory=dict)
    error: str = ""
    started_at: datetime | None = None
    completed_at: datetime | None = None


class WorkflowDefinition(BaseModel):
    """Static definition of a workflow — name + ordered step names."""

    model_config = ConfigDict(extra="forbid")

    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid4().hex[:12]}")
    name: str
    description_ar: str = ""
    description_en: str = ""
    steps: list[str] = Field(default_factory=list)
    allowed_transitions: dict[str, list[str]] = Field(
        default_factory=lambda: {k: sorted(v) for k, v in ALLOWED_TRANSITIONS.items()}
    )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class WorkflowRun(BaseModel):
    """Live instance of a workflow."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(default_factory=lambda: f"run_{uuid4().hex[:12]}")
    workflow_id: str
    customer_handle: str = "Saudi B2B customer"
    state: WorkflowState = "pending"
    current_step: str = ""
    step_history: list[WorkflowStep] = Field(default_factory=list)
    idempotency_keys_seen: set[str] = Field(default_factory=set)
    checkpoint: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        # Sets aren't JSON-serializable; convert via mode="json".
        data = self.model_dump(mode="json")
        # pydantic v2 serializes set as list, but we want a stable order.
        if isinstance(data.get("idempotency_keys_seen"), list):
            data["idempotency_keys_seen"] = sorted(data["idempotency_keys_seen"])
        return data
