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

# How an offering's price is expressed. See docs/COMPANY_SERVICE_LADDER.md.
#   fixed             — a single confirmed price (used only after evidence).
#   range             — a real min-max band the founder quotes within.
#   recommended_draft — no fixed number yet; quoted per engagement until
#                       >= 3 paid pilots inform a real band.
PriceMode = Literal["fixed", "range", "recommended_draft"]

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
    # Pricing mode (governed-revenue catalog). `price_sar` stays present and
    # valid for every offering so existing consumers do not break: for a
    # `range` offering it is the min; for `recommended_draft` it is 0.0.
    price_mode: PriceMode = "fixed"
    price_sar_min: float | None = Field(default=None, ge=0)
    price_sar_max: float | None = Field(default=None, ge=0)
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

    @model_validator(mode="after")
    def _validate_price_mode(self) -> ServiceOffering:
        """Enforce price-mode invariants from docs/COMPANY_SERVICE_LADDER.md."""
        if self.price_mode == "range":
            if self.price_sar_min is None or self.price_sar_max is None:
                raise ValueError(
                    "price_mode='range' requires price_sar_min and price_sar_max"
                )
            if self.price_sar_min > self.price_sar_max:
                raise ValueError(
                    "price_sar_min must be <= price_sar_max for a range"
                )
        # `recommended_draft` carries no fixed price claim — min/max stay unset.
        return self
