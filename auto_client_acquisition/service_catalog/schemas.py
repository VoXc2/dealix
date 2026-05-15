"""Service catalog schemas — Pydantic v2 with extra='forbid' + slots."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CustomerJourneyStage = Literal[
    "discovery",      # Free Mini Diagnostic
    "first_paid",     # 499 Sprint
    "expansion",      # Data-to-Revenue Pack
    "monthly",        # Growth Ops Monthly
    "executive",      # Executive Command Center
    "support_addon",  # Support OS Add-on
    "channel",        # Agency Partner OS
    "enterprise",     # Enterprise AI Transformation programs
]

EnterpriseCategory = Literal[
    "operating_system",      # AI Operating System for Business
    "revenue",               # AI Revenue Transformation
    "knowledge",             # AI Knowledge & Decision Platform
    "operations",            # AI Operations Automation
    "governance",            # AI Governance & Readiness Program
    "transformation_sprint", # Flagship 45-day Enterprise Transformation Sprint
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
    price_unit: Literal["one_time", "per_month", "custom"] = "one_time"
    duration_days: int = Field(..., ge=0, le=365)
    deliverables: tuple[str, ...] = Field(..., min_length=1)
    kpi_commitment_ar: str
    kpi_commitment_en: str
    refund_policy_ar: str
    refund_policy_en: str
    action_modes_used: tuple[ActionMode, ...] = Field(..., min_length=1)
    hard_gates: tuple[str, ...] = Field(..., min_length=1)
    customer_journey_stage: CustomerJourneyStage
    is_estimate: bool = True  # Article 8 — every numeric is an estimate


class PricingTier(BaseModel):
    """One tier of an enterprise offering (e.g. Basic / Growth / Enterprise).

    Enterprise deals carry a one-time ``setup_sar`` plus a recurring
    ``monthly_sar`` retainer — the single-price ``ServiceOffering`` model
    cannot express this, so enterprise programs use this richer shape.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., min_length=1, max_length=64)
    name_ar: str = Field(..., min_length=1, max_length=120)
    name_en: str = Field(..., min_length=1, max_length=120)
    setup_sar: float = Field(..., ge=0)
    monthly_sar: float = Field(..., ge=0)
    min_duration_days: int = Field(..., ge=0, le=730)
    deliverables: tuple[str, ...] = Field(..., min_length=1)
    kpi_commitment_ar: str = Field(..., min_length=1)
    kpi_commitment_en: str = Field(..., min_length=1)
    exclusions: tuple[str, ...] = ()
    is_estimate: bool = True


class EnterpriseOffering(BaseModel):
    """An enterprise AI transformation program — sold as a tiered contract.

    Distinct from ``ServiceOffering`` (single price): an enterprise program
    bundles a multi-workstream scope and is quoted per ``PricingTier``.
    Article 8 still holds — commitment language only, never "guaranteed".
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., min_length=1, max_length=64)
    name_ar: str = Field(..., min_length=1, max_length=160)
    name_en: str = Field(..., min_length=1, max_length=160)
    category: EnterpriseCategory
    summary_ar: str = Field(..., min_length=1)
    summary_en: str = Field(..., min_length=1)
    workstreams: tuple[str, ...] = Field(..., min_length=1)
    tiers: tuple[PricingTier, ...] = Field(..., min_length=1)
    action_modes_used: tuple[ActionMode, ...] = Field(..., min_length=1)
    hard_gates: tuple[str, ...] = Field(..., min_length=1)
    customer_journey_stage: CustomerJourneyStage = "enterprise"
    is_estimate: bool = True  # Article 8 — every numeric is an estimate
