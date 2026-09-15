"""Service catalog schemas — Pydantic v2 with extra='forbid' + slots."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CustomerJourneyStage = Literal[
    "discovery",       # Free Mini Diagnostic
    "first_paid",      # 499 Sprint
    "expansion",       # Data-to-Revenue Pack
    "monthly",         # Growth Ops Monthly
    "executive",       # Executive Command Center
    "support_addon",   # Support OS Add-on
    "channel",         # Agency Partner OS
    "transformation",  # Enterprise Transformation OS systems (setup + monthly ranges)
]

ActionMode = Literal[
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
]

CommercialStatus = Literal[
    "free_entry",
    "quote_only",
    "internal_experiment",
    "future",
    "public_approved",
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
    price_unit: Literal["one_time", "per_month", "custom"] = "one_time"
    duration_days: int | None = Field(..., ge=0, le=365)
    duration_policy: Literal["fixed_internal_estimate", "customer_specific_after_qualified_discovery", "ongoing_or_scoped"] = "fixed_internal_estimate"
    deliverables: tuple[str, ...] = Field(..., min_length=1)
    kpi_commitment_ar: str
    kpi_commitment_en: str
    refund_policy_ar: str
    refund_policy_en: str
    action_modes_used: tuple[ActionMode, ...] = Field(..., min_length=1)
    hard_gates: tuple[str, ...] = Field(..., min_length=1)
    customer_journey_stage: CustomerJourneyStage
    is_estimate: bool = True  # Article 8 — every numeric is an estimate
    commercial_status: CommercialStatus = "internal_experiment"

    # Optional enterprise-transformation range fields. Default None so the
    # core 7 offerings stay valid. For "transformation"-stage systems the
    # setup fee is a *range* (price_sar = low end / billable floor; price_sar_max
    # = high end) and there is also a recurring monthly range. All estimates.
    price_sar_max: float | None = Field(default=None, ge=0)
    price_monthly_sar_min: float | None = Field(default=None, ge=0)
    price_monthly_sar_max: float | None = Field(default=None, ge=0)
    setup_is_range: bool = False
