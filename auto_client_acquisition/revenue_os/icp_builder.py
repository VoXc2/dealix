"""ICP Builder — derive a Saudi ICP from customer answers or first-party data.

بناء شخصية العميل المثالية (ICP) السعودي.

If the customer has no documented ICP, this module produces a defensible
default from a few questions; if they have CRM data, it derives an ICP
from observed won-deal characteristics.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field


class CustomerTier(StrEnum):
    SME = "sme"
    MID_MARKET = "mid_market"
    ENTERPRISE = "enterprise"


class ICPProfile(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    name_ar: str
    name_en: str
    tier: CustomerTier
    verticals: list[str] = Field(default_factory=list)
    regions: list[str] = Field(default_factory=list)
    headcount_min: int | None = None
    headcount_max: int | None = None
    revenue_min_sar: float | None = None
    revenue_max_sar: float | None = None
    triggers: list[str] = Field(default_factory=list)
    deal_breakers: list[str] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def from_answers(
    *,
    sector: str,
    region: str,
    target_size: str = "mid_market",
    desired_triggers: list[str] | None = None,
) -> ICPProfile:
    """Build a defensible default ICP from minimal answers (3 questions)."""
    tier = CustomerTier(target_size)
    bands = {
        CustomerTier.SME: (10, 50, 5_000_000, 30_000_000),
        CustomerTier.MID_MARKET: (50, 200, 30_000_000, 200_000_000),
        CustomerTier.ENTERPRISE: (200, 5000, 200_000_000, 50_000_000_000),
    }[tier]
    return ICPProfile(
        name_ar=f"{sector} — {region} — {target_size}",
        name_en=f"{sector} — {region} — {target_size}",
        tier=tier,
        verticals=[sector],
        regions=[region],
        headcount_min=bands[0],
        headcount_max=bands[1],
        revenue_min_sar=bands[2],
        revenue_max_sar=bands[3],
        triggers=list(desired_triggers or []),
        deal_breakers=[
            "no_commercial_registration",
            "active_regulatory_action",
            "data_residency_outside_ksa_required",
        ],
    )


def from_won_deals(records: Iterable[dict[str, Any]]) -> ICPProfile:
    """Derive an ICP from observed won-deal characteristics (median-shaped)."""
    records = list(records)
    if not records:
        return from_answers(sector="other", region="riyadh", target_size="mid_market")
    verticals = sorted({str(r.get("vertical") or "other") for r in records})
    regions = sorted({str(r.get("region") or "riyadh") for r in records})
    heads = sorted([int(r.get("headcount") or 0) for r in records if r.get("headcount")])
    revs = sorted([float(r.get("annual_revenue_sar") or 0) for r in records if r.get("annual_revenue_sar")])
    head_min = heads[0] if heads else None
    head_max = heads[-1] if heads else None
    rev_min = revs[0] if revs else None
    rev_max = revs[-1] if revs else None
    tier = CustomerTier.MID_MARKET
    if head_max and head_max >= 200:
        tier = CustomerTier.ENTERPRISE
    elif head_max and head_max < 50:
        tier = CustomerTier.SME

    return ICPProfile(
        name_ar="ICP مستنبط من الصفقات الفائزة",
        name_en="ICP derived from won deals",
        tier=tier,
        verticals=verticals[:5],
        regions=regions[:5],
        headcount_min=head_min,
        headcount_max=head_max,
        revenue_min_sar=rev_min,
        revenue_max_sar=rev_max,
        triggers=[],
        deal_breakers=[
            "no_commercial_registration",
            "active_regulatory_action",
        ],
    )
