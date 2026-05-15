"""Service catalog schemas — Pydantic v2 with extra='forbid' + slots."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CustomerJourneyStage = Literal[
    "discovery",   # Rung 1 — Free Diagnostic
    "first_paid",  # Rung 2 — Sprint
    "pilot",       # Rung 3 — Pilot
    "retainer",    # Rung 4 — Retainer / Managed Ops
    "enterprise",  # Rung 5 — Enterprise / Custom AI
    "channel",     # Agency Partner (distribution channel, not a rung)
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
    # Canonical anchor price. For banded rungs (Retainer, Enterprise) this is
    # the band minimum so legacy ascending-price logic and int() formatting
    # stay valid; the true band lives in price_sar_min / price_sar_max.
    price_sar: float = Field(..., ge=0)
    price_sar_min: float | None = Field(default=None, ge=0)
    price_sar_max: float | None = Field(default=None, ge=0)
    # Human-readable price strings — landing pages and the commercial map
    # render these verbatim so they never re-derive band formatting.
    price_display_ar: str = Field(..., min_length=1, max_length=80)
    price_display_en: str = Field(..., min_length=1, max_length=80)
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
    # True for the 5 customer-facing ladder rungs; False for the Agency
    # Partner distribution channel.
    is_rung: bool = True
    is_estimate: bool = True  # Article 8 — every numeric is an estimate

    @model_validator(mode="after")
    def _check_price_band(self) -> ServiceOffering:
        """A banded rung must carry a consistent min/max with price_sar==min."""
        if self.price_sar_max is not None or self.price_sar_min is not None:
            if self.price_sar_min is None or self.price_sar_max is None:
                raise ValueError(
                    f"{self.id}: price band needs both price_sar_min and price_sar_max"
                )
            if self.price_sar_min > self.price_sar_max:
                raise ValueError(
                    f"{self.id}: price_sar_min must be <= price_sar_max"
                )
            if self.price_sar != self.price_sar_min:
                raise ValueError(
                    f"{self.id}: price_sar must equal price_sar_min for a banded rung"
                )
        return self
