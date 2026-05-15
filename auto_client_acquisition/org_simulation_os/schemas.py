"""Schemas for System 32 — the Organizational Simulation Engine."""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ScenarioKind(StrEnum):
    WORKFLOW = "workflow"
    FAILURE = "failure"
    APPROVAL = "approval"
    SCALE = "scale"
    INCIDENT = "incident"


class SimulationScenario(BaseModel):
    """A scenario to simulate before deployment."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    scenario_id: str = Field(default_factory=lambda: f"sim_{uuid4().hex[:12]}")
    kind: ScenarioKind
    parameters: dict[str, Any] = Field(default_factory=dict)


class SimulationResult(BaseModel):
    """The predicted outcome of a simulated scenario."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    scenario_id: str
    kind: ScenarioKind
    predicted_outcomes: list[dict[str, Any]] = Field(default_factory=list)
    bottlenecks: list[str] = Field(default_factory=list)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    recommendation: str = ""
