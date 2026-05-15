"""Tenant-aware operational schemas for Control Plane."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Literal
from uuid import uuid4


RunState = Literal["running", "paused", "awaiting_approval", "completed", "failed", "rolled_back"]


class WorkflowRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(default_factory=lambda: f"run_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    workflow_id: str = Field(..., min_length=1)
    customer_id: str = ""
    state: RunState = "running"
    current_step: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ControlEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:14]}")
    tenant_id: str = Field(..., min_length=1)
    event_type: str = Field(..., min_length=1)
    source_module: str = Field(..., min_length=1)
    actor: str = Field(..., min_length=1)
    run_id: str = ""
    subject_type: str = ""
    subject_id: str = ""
    decision: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RollbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    actor: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)


class PolicyEditRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    policy_id: str = Field(..., min_length=1)
    actor: str = Field(..., min_length=1)
    change: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "ControlEvent",
    "PolicyEditRequest",
    "RollbackRequest",
    "WorkflowRun",
]
