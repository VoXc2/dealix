"""Pydantic v2 schemas for founder_v10."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SeverityLevel = Literal["low", "medium", "high", "blocked"]


class Blocker(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    title_ar: str = ""
    title_en: str = ""
    severity: SeverityLevel = "low"
    blocking_layer: str = ""


class RiskEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    risk_type: str = ""
    level: SeverityLevel = "low"
    detected_in: str = ""
    action: str = ""


class DailyBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    summary_ar: str = ""
    summary_en: str = ""
    top_3_decisions: list[dict[str, Any]] = Field(default_factory=list)
    cost_summary_usd: float = 0.0
    risk_register: list[dict[str, Any]] = Field(default_factory=list)
    evidence_summary: dict[str, Any] = Field(default_factory=dict)
    blockers: list[str] = Field(default_factory=list)
    next_action_ar: str = ""
    next_action_en: str = ""
