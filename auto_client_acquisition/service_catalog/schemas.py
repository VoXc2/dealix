"""Service catalog schemas — Pydantic v2 with extra='forbid' + slots."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CustomerJourneyStage = Literal[
    "discovery",      # Free Mini Diagnostic
    "first_paid",     # 499 Sprint
    "expansion",      # Data-to-Revenue Pack
    "monthly",        # Growth Ops Monthly
    "executive",      # Executive Command Center
    "support_addon",  # Support OS Add-on
    "channel",        # Agency Partner OS
]

ActionMode = Literal[
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
]


class ServiceOffering(BaseModel):
    """One priced offering in Dealix's catalog.

    Read-only data class. Article 8 forbids "guaranteed"/"نضمن".
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., min_length=1, max_length=64)
    name_ar: str = Field(..., min_length=1, max_length=120)
    name_en: str = Field(..., min_length=1, max_length=120)
    price_sar: float = Field(..., ge=0)
    price_min_sar: float | None = Field(default=None, ge=0)
    price_max_sar: float | None = Field(default=None, ge=0)
    price_unit: Literal["one_time", "per_month", "custom"] = "one_time"
    duration_days: int = Field(..., ge=0, le=365)
    deliverables: tuple[str, ...] = Field(..., min_length=1)
    target_segments: tuple[str, ...] = Field(default_factory=tuple)
    trigger_signals: tuple[str, ...] = Field(default_factory=tuple)
    kpi_commitment_ar: str
    kpi_commitment_en: str
    refund_policy_ar: str
    refund_policy_en: str
    action_modes_used: tuple[ActionMode, ...] = Field(..., min_length=1)
    hard_gates: tuple[str, ...] = Field(..., min_length=1)
    customer_journey_stage: CustomerJourneyStage
    is_estimate: bool = True  # Article 8 — every numeric is an estimate

    @model_validator(mode="after")
    def _validate_price_range(self) -> "ServiceOffering":
        has_min = self.price_min_sar is not None
        has_max = self.price_max_sar is not None
        if has_min != has_max:
            raise ValueError("price_min_sar and price_max_sar must be set together")
        if has_min and has_max:
            if self.price_min_sar > self.price_max_sar:
                raise ValueError("price_min_sar must be <= price_max_sar")
            if not (self.price_min_sar <= self.price_sar <= self.price_max_sar):
                raise ValueError("price_sar must fall within [price_min_sar, price_max_sar]")
        return self
