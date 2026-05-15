"""Simulation schemas for org-level what-if analysis."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import uuid4


class SimulationScenario(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(default_factory=lambda: f"sim_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    assumptions: dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["SimulationScenario"]
