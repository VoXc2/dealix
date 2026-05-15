"""Schemas for internal workflow ROI/value engine."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class WorkflowValueMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric_id: str = Field(default_factory=lambda: f"met_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    metric_name: str = Field(..., min_length=1)
    tier: str = Field(default="estimated", min_length=1)
    amount: float = 0.0
    source_ref: str = ""
    confirmation_ref: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["WorkflowValueMetric"]
