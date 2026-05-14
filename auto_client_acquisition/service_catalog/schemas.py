"""Service catalog schemas — Pydantic v2 with extra='forbid' + slots."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CustomerJourneyStage = Literal[
    # 2026-Q2 active ladder
    "discovery",       # Strategic Diagnostic (free)
    "monthly",         # Governed Ops Retainer (4,999/mo)
    "flagship",        # Revenue Intelligence Sprint (25,000)
    # Legacy values — preserved so historical records load. NOT used
    # by any 2026-Q2 active offering.
    "first_paid",      # legacy: 499 Sprint
    "expansion",       # legacy: Data-to-Revenue Pack
    "executive",       # legacy: Executive Command Center
    "support_addon",   # legacy: Support OS Add-on
    "channel",         # legacy: Agency Partner OS
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
