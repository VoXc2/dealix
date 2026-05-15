"""Schemas for System 31 — the Enterprise Safety Engine."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker(BaseModel):
    """Per-target failure breaker — opens after `threshold` failures."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    breaker_id: str = Field(default_factory=lambda: f"brk_{uuid4().hex[:12]}")
    target: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    threshold: int = 3
    opened_at: datetime | None = None


class KillSwitch(BaseModel):
    """An emergency stop for an agent or workflow target."""

    model_config = ConfigDict(extra="forbid")

    switch_id: str = Field(default_factory=lambda: f"kil_{uuid4().hex[:12]}")
    target: str
    engaged: bool = True
    engaged_by: str = "system"
    reason: str = ""
    engaged_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    released_at: datetime | None = None


class ExecutionLimit(BaseModel):
    """Rate / concurrency ceilings for a target."""

    model_config = ConfigDict(extra="forbid")

    target: str
    max_actions_per_hour: int = Field(default=1000, ge=0)
    max_concurrency: int = Field(default=10, ge=0)


class SafetyVerdict(BaseModel):
    """Result of a runtime safety check."""

    model_config = ConfigDict(extra="forbid")

    target: str
    allowed: bool
    barriers_hit: list[str] = Field(default_factory=list)
    reason: str = ""
