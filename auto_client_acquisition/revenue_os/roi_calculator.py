"""ROI Calculator — Saudi B2B ROI model for Dealix Revenue Intelligence Sprint.

حاسبة العائد على الاستثمار للسوق السعودي.

Conservative / mid / optimistic scenarios. Matches docs/sales/roi_model_saudi.md.
Pure function; safe for sales-side use and for embedding in proposals.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ROIInputs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bdr_count: int = Field(ge=0, default=2)
    bdr_loaded_cost_sar_month: float = Field(ge=0, default=18_000)
    current_cac_sar: float = Field(ge=0, default=8_000)
    average_deal_size_sar: float = Field(ge=0, default=120_000)
    monthly_qualified_leads_now: int = Field(ge=0, default=12)
    win_rate_now: float = Field(ge=0.0, le=1.0, default=0.18)
    sales_cycle_days_now: int = Field(ge=1, default=90)
    dealix_annual_fee_sar: float = Field(ge=0, default=96_000)  # Growth tier
    dealix_onboarding_sar: float = Field(ge=0, default=15_000)


class ROIScenario(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    cac_reduction_pct: float
    win_rate_uplift_pct: float
    cycle_compression_pct: float
    lead_volume_multiplier: float


class ROIResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario: str
    annual_new_qualified_leads: int
    annual_new_wins: int
    annual_revenue_uplift_sar: float
    annual_cac_savings_sar: float
    annual_bdr_productivity_savings_sar: float
    total_annual_value_sar: float
    annual_dealix_cost_sar: float
    net_roi_sar: float
    roi_multiple: float
    payback_months: float

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


CONSERVATIVE = ROIScenario(
    name="conservative",
    cac_reduction_pct=0.15,
    win_rate_uplift_pct=0.10,
    cycle_compression_pct=0.10,
    lead_volume_multiplier=1.5,
)
MID = ROIScenario(
    name="mid",
    cac_reduction_pct=0.25,
    win_rate_uplift_pct=0.20,
    cycle_compression_pct=0.20,
    lead_volume_multiplier=2.0,
)
OPTIMISTIC = ROIScenario(
    name="optimistic",
    cac_reduction_pct=0.40,
    win_rate_uplift_pct=0.40,
    cycle_compression_pct=0.30,
    lead_volume_multiplier=3.0,
)


def compute(inputs: ROIInputs, scenario: ROIScenario) -> ROIResult:
    monthly_leads_after = inputs.monthly_qualified_leads_now * scenario.lead_volume_multiplier
    annual_leads_after = monthly_leads_after * 12
    annual_leads_now = inputs.monthly_qualified_leads_now * 12
    new_leads = annual_leads_after - annual_leads_now

    win_rate_after = min(1.0, inputs.win_rate_now * (1 + scenario.win_rate_uplift_pct))
    annual_wins_after = annual_leads_after * win_rate_after
    annual_wins_now = annual_leads_now * inputs.win_rate_now
    new_wins = max(0.0, annual_wins_after - annual_wins_now)

    revenue_uplift = new_wins * inputs.average_deal_size_sar
    cac_savings = (
        annual_leads_after * inputs.current_cac_sar * scenario.cac_reduction_pct
    )
    bdr_productivity_savings = (
        inputs.bdr_count * inputs.bdr_loaded_cost_sar_month * 12 * scenario.cycle_compression_pct
    )

    total_value = revenue_uplift + cac_savings + bdr_productivity_savings
    annual_dealix_cost = inputs.dealix_annual_fee_sar + inputs.dealix_onboarding_sar
    net_roi = total_value - annual_dealix_cost
    roi_multiple = (total_value / annual_dealix_cost) if annual_dealix_cost else 0.0
    payback_months = (
        (annual_dealix_cost / (total_value / 12)) if total_value > 0 else float("inf")
    )

    return ROIResult(
        scenario=scenario.name,
        annual_new_qualified_leads=int(new_leads),
        annual_new_wins=int(new_wins),
        annual_revenue_uplift_sar=round(revenue_uplift, 0),
        annual_cac_savings_sar=round(cac_savings, 0),
        annual_bdr_productivity_savings_sar=round(bdr_productivity_savings, 0),
        total_annual_value_sar=round(total_value, 0),
        annual_dealix_cost_sar=round(annual_dealix_cost, 0),
        net_roi_sar=round(net_roi, 0),
        roi_multiple=round(roi_multiple, 2),
        payback_months=round(payback_months, 1),
    )


def compute_all(inputs: ROIInputs) -> dict[str, ROIResult]:
    """Returns conservative / mid / optimistic side-by-side."""
    return {
        "conservative": compute(inputs, CONSERVATIVE),
        "mid": compute(inputs, MID),
        "optimistic": compute(inputs, OPTIMISTIC),
    }
