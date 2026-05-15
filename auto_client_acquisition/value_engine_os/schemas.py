"""Schemas for System 34 — the Business Value Engine."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ValueTier(StrEnum):
    """Discipline tier — `measured` requires a verifiable source reference."""

    MEASURED = "measured"
    ESTIMATED = "estimated"


class WorkflowValueMetric(BaseModel):
    """One recorded value measurement for a workflow run."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    metric_id: str = Field(default_factory=lambda: f"val_{uuid4().hex[:12]}")
    run_id: str
    workflow_id: str
    revenue_impact_sar: float = 0.0
    time_saved_minutes: float = 0.0
    execution_speed_ms: float = 0.0
    efficiency_gain_pct: float = 0.0
    tier: ValueTier = ValueTier.ESTIMATED
    source_ref: str = ""
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ROIReport(BaseModel):
    """Aggregated ROI for one workflow over a period."""

    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    period: str
    metric_count: int
    total_value_sar: float
    total_time_saved_minutes: float
    avg_efficiency_gain_pct: float
    cost_sar: float
    roi_ratio: float
    optimization_suggestions: list[str] = Field(default_factory=list)
