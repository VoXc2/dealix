"""Runtime safety schemas."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class KillSwitchState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    target_id: str = Field(..., min_length=1)
    is_active: bool = False
    reason: str = ""
    activated_at: datetime | None = None


class CircuitBreakerState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    failures: int = 0
    threshold: int = Field(default=3, ge=1)
    is_open: bool = False
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CanaryRollout(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    rollout_id: str = Field(..., min_length=1)
    target_module: str = Field(..., min_length=1)
    canary_percent: int = Field(default=0, ge=0, le=100)
    status: str = "pending"


__all__ = ["CanaryRollout", "CircuitBreakerState", "KillSwitchState"]
