"""Pydantic v2 schemas for service mapping v7."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Hard-rule forbidden actions — must be present on every recommendation.
FORBIDDEN_ACTIONS: tuple[str, ...] = (
    "cold_whatsapp",
    "linkedin_automation",
    "scrape_web",
    "live_charge",
    "send_email_live",
)


class MapRequest(BaseModel):
    """Inbound goal-to-service mapping request."""

    model_config = ConfigDict(extra="forbid")

    company_handle: str = Field(..., min_length=1)
    goal_ar: str = ""
    goal_en: str = ""
    pain_points: list[str] = Field(default_factory=list)
    available_budget_sar: float | None = None
    urgency: Literal["low", "medium", "high"] = "medium"


class ServiceRecommendation(BaseModel):
    """Deterministic recommendation — never auto-acted; founder approves."""

    model_config = ConfigDict(extra="forbid")

    company_handle: str
    recommended_service: str
    why_ar: str
    why_en: str
    expected_deliverables: list[str]
    excluded_actions: list[str]
    proof_metrics: list[str]
    price_band_sar: str
    risk_level: Literal["low", "medium", "high", "blocked"]
    approval_required: bool = True
    next_step: str
