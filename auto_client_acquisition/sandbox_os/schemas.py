"""Schemas for System 29 — the Enterprise Sandbox Engine."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class SandboxIsolation(StrEnum):
    FULL = "full"
    CANARY = "canary"
    STAGED = "staged"


class SandboxEnv(BaseModel):
    """An isolated environment for safe experimentation."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    sandbox_id: str = Field(default_factory=lambda: f"sbx_{uuid4().hex[:12]}")
    name: str
    isolation: SandboxIsolation = SandboxIsolation.FULL
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SandboxStep(BaseModel):
    """One step of a workflow to be simulated."""

    model_config = ConfigDict(extra="forbid")

    step_id: str
    action_type: str
    inputs: dict[str, Any] = Field(default_factory=dict)


class SandboxRun(BaseModel):
    """A simulated workflow run — never touches production."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(default_factory=lambda: f"sbr_{uuid4().hex[:12]}")
    sandbox_id: str
    workflow_id: str
    status: str = "completed"
    is_production: bool = False
    step_results: list[dict[str, Any]] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None


class CanaryRollout(BaseModel):
    """A staged canary rollout of a workflow."""

    model_config = ConfigDict(extra="forbid")

    rollout_id: str = Field(default_factory=lambda: f"can_{uuid4().hex[:12]}")
    workflow_id: str
    traffic_pct: float = Field(ge=0.0, le=100.0)
    status: str = "observing"
    health: dict[str, Any] = Field(default_factory=dict)


class ReplayResult(BaseModel):
    """The diff between a source sandbox run and its replay."""

    model_config = ConfigDict(extra="forbid")

    source_run_id: str
    replay_run_id: str
    divergences: list[dict[str, Any]] = Field(default_factory=list)
