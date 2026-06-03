"""Typed records for the safety_v10 red-team eval pack."""
from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class EvalCategory(StrEnum):
    COLD_WHATSAPP_AR = "cold_whatsapp_ar"
    COLD_WHATSAPP_EN = "cold_whatsapp_en"
    LINKEDIN_AUTOMATION = "linkedin_automation"
    SCRAPING = "scraping"
    FAKE_PROOF = "fake_proof"
    FAKE_TESTIMONIAL = "fake_testimonial"
    GUARANTEED_REVENUE = "guaranteed_revenue"
    GUARANTEED_SEO_RANKING = "guaranteed_seo_ranking"
    LIVE_CHARGE = "live_charge"
    LIVE_SEND = "live_send"
    PROMPT_INJECTION = "prompt_injection"
    PII_LEAKAGE = "pii_leakage"
    SECRET_LEAKAGE = "secret_leakage"
    EXCESSIVE_AGENCY = "excessive_agency"
    UNSAFE_TOOL_USE = "unsafe_tool_use"


class EvalCase(BaseModel):
    """One red-team eval case."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str
    category: EvalCategory
    input_ar: str
    input_en: str
    expected_action: Literal["block", "require_approval", "allow"]
    why: str


class EvalResult(BaseModel):
    """Result of running one EvalCase through policy_engine_check."""

    model_config = ConfigDict(use_enum_values=True)

    case_id: str
    category: EvalCategory
    actual_action: Literal["block", "require_approval", "allow"]
    passed: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class EvalReport(BaseModel):
    """Aggregate of EvalResult across an entire run."""

    model_config = ConfigDict(use_enum_values=True)

    total: int
    passed: int
    failed: int
    by_category: dict[str, dict[str, int]] = Field(default_factory=dict)
    results: list[EvalResult] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
