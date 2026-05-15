"""Schemas for the integration_upgrade adapter shim."""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

DegradeSeverity = Literal["info", "low", "medium", "high", "critical"]


class DegradedSection(BaseModel):
    """Returned in place of a section that failed to compose."""

    model_config = ConfigDict(extra="forbid")

    section: str
    degraded: bool = True
    severity: DegradeSeverity = "medium"
    reason_ar: str
    reason_en: str
    next_fix_ar: str = ""
    next_fix_en: str = ""
    safety_summary: str = "no_500_no_internal_leak"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ContractStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    available: bool
    degraded: bool = False
    blockers: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SafeLabel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label_ar: str
    label_en: str
    source_internal: str
