"""Pydantic schemas for Company Growth Beast (Arabic primary, English secondary)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CompanyGrowthProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    company_name_optional: str = ""
    sector: str = ""
    offer: str = ""
    ideal_customer: str = ""
    best_past_customers_summary: str = ""
    current_channels: str = ""
    current_sales_process: str = ""
    common_objections: str = ""
    support_questions: str = ""
    proof_assets: str = ""
    constraints: str = ""
    consent_for_diagnostic: bool = False
    language_preference: str = "ar"


class TargetSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_name_ar: str
    segment_name_en: str
    pain: str
    buying_trigger: str
    fit_score: int = Field(ge=0, le=100)
    urgency_score: int = Field(ge=0, le=100)
    proof_potential_score: int = Field(ge=0, le=100)
    access_score: int = Field(ge=0, le=100)
    risk_score: int = Field(ge=0, le=100)
    recommended_route: str
    reason: str
    action_mode: str = "draft_only"


class OfferRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_name_ar: str
    offer_name_en: str
    target_segment: str
    headline_ar: str
    headline_en: str
    promise: str
    non_promise: str
    seven_day_plan: list[str]
    proof_metric: str
    blocked_claims: list[str]
    approval_required: bool = True


class GrowthExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis: str
    target_segment: str
    offer: str
    channel: str
    safe_action: str
    success_metric: str
    expected_learning: str
    stop_condition: str
    action_mode: str = "draft_only"


class WeeklyGrowthReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    best_segment: str
    best_offer: str
    best_message_angle: str
    what_worked: list[str]
    what_failed: list[str]
    proof_events: list[str]
    support_insights: list[str]
    next_experiment: str
    top_3_decisions: list[str]
    blocked_actions: list[str]
