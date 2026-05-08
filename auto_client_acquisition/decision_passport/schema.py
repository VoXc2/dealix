"""Pydantic schema for Decision Passport API responses."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

PriorityBucket = Literal["P0_NOW", "P1_THIS_WEEK", "P2_NURTURE", "P3_LOW_PRIORITY", "BLOCKED"]


class ScoreBoard(BaseModel):
    """Multi-dimensional scores (0–1 scale where applicable)."""

    fit_score: float = Field(ge=0.0, le=1.0)
    intent_score: float = Field(ge=0.0, le=1.0, description="Derived from pain + message strength")
    urgency_score: float = Field(ge=0.0, le=1.0)
    revenue_potential_score: float = Field(ge=0.0, le=1.0)
    engagement_score: float = Field(ge=0.0, le=1.0, description="Proxy: BANT progress + data depth")
    data_quality_score: float = Field(ge=0.0, le=1.0)
    warm_route_score: float = Field(ge=0.0, le=1.0, description="Higher = safer channels available")
    compliance_risk_score: float = Field(ge=0.0, le=1.0, description="Higher = more policy attention")
    deliverability_risk_score: float = Field(ge=0.0, le=1.0, description="Email/channel readiness risk")


class DecisionPassport(BaseModel):
    """جواز القرار — قرار تجاري واحد لكل lead."""

    schema_version: str = "1.0"
    lead_id: str
    company: str
    contact_name: str | None = None
    source: str
    locale: str = "ar"
    why_now_ar: str
    why_now_en: str
    icp_tier: str
    priority_bucket: PriorityBucket
    scores: ScoreBoard
    best_channel: str
    recommended_action: str
    recommended_action_ar: str
    blocked_actions: list[str] = Field(default_factory=list)
    proof_target: str
    proof_target_ar: str
    next_step_ar: str
    next_step_en: str
    bant_open_count: int = 0
    qualification_status: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
