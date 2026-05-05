"""Pydantic v2 schemas for ai_workforce_v10."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


ReviewerVerdict = Literal["approved", "needs_revision", "blocked"]


class WorkforceMemoryEntry(BaseModel):
    """A single short-term memory entry for one customer.

    Memory NEVER crosses customer boundaries. ``value_redacted`` is
    expected to already be redacted before record_memory is called.
    """

    model_config = ConfigDict(extra="forbid")

    customer_handle: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    value_redacted: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    ttl_hours: int = Field(default=24, ge=0, le=168)


class ReviewerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: ReviewerVerdict = "approved"
    reasons_ar: list[str] = Field(default_factory=list)
    reasons_en: list[str] = Field(default_factory=list)
    blocked_tokens: list[str] = Field(default_factory=list)


class PlannerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assigned_agents: list[str] = Field(default_factory=list)
    task_plan: list[dict[str, Any]] = Field(default_factory=list)
    rationale_ar: str = ""
    rationale_en: str = ""
