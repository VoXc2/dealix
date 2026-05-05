"""Typed schemas for the weekly executive report."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WeeklyReport(BaseModel):
    """Founder-facing weekly executive report.

    Composed from existing layers (no LLM). Bilingual output with
    Arabic primary. The markdown_ar / markdown_en strings are ready
    for copy-paste into LinkedIn / Notion / email.
    """

    model_config = ConfigDict(extra="forbid")

    week_label: str = ""
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    executive_summary_ar: str = ""
    executive_summary_en: str = ""
    revenue_movement: dict[str, Any] = Field(default_factory=dict)
    pipeline: dict[str, Any] = Field(default_factory=dict)
    delivery: dict[str, Any] = Field(default_factory=dict)
    proof: dict[str, Any] = Field(default_factory=dict)
    risks: list[str] = Field(default_factory=list)
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    next_week_plan: list[str] = Field(default_factory=list)
    markdown_ar: str = ""
    markdown_en: str = ""
    guardrails: dict[str, Any] = Field(default_factory=dict)
