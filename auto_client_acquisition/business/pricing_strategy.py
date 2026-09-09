"""Commercial strategy compatibility helpers under current quote-only authority.

Historical fixed monthly tiers and performance-fee ladders are retired as
commercial authority. This module remains import-compatible for analytics and
legacy callers, but it cannot publish a price, recommend a fixed plan, or
calculate a billable fee.
"""
from __future__ import annotations

from typing import Any

_CANONICAL_PATH = [
    "free_mini_diagnostic",
    "qualified_discovery",
    "customer_specific_quote",
    "revenue_command_pilot_30d",
]
_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"


def get_pricing_tiers() -> dict[str, Any]:
    """Return commercial authority metadata without a public pricing ladder."""
    return {
        "status": "quote_only",
        "currency": "SAR",
        "tiers": [],
        "commercial_path": list(_CANONICAL_PATH),
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
        "live_charge_allowed": False,
        "legacy_fixed_tiers_retired": True,
    }


def recommend_plan(
    *,
    company_size: str,
    monthly_budget_sar: float,
    goal: str,
) -> dict[str, Any]:
    """Route to discovery rather than infer a commercial package from inputs."""
    return {
        "recommended_plan": None,
        "recommended_next_step": "free_mini_diagnostic_then_qualified_discovery",
        "price_authority": _PRICE_AUTHORITY,
        "public_fixed_price": False,
        "automatic_plan_selection": False,
        "inputs": {
            "company_size": company_size,
            "monthly_budget_sar": monthly_budget_sar,
            "goal": goal,
        },
        "note": (
            "Company size, budget and goal may inform discovery but do not create "
            "pricing or package authority."
        ),
    }


def calculate_performance_fee(
    *,
    qualified_leads: int,
    booked_meetings: int,
    won_revenue_sar: float,
    lead_fee_sar: float = 0.0,
    meeting_fee_sar: float = 0.0,
    success_fee_pct: float = 0.0,
) -> dict[str, Any]:
    """Compatibility surface: never calculate an invoiceable performance fee."""
    del lead_fee_sar, meeting_fee_sar, success_fee_pct
    return {
        "status": "retired_commercial_authority",
        "qualified_leads": max(0, qualified_leads),
        "booked_meetings": max(0, booked_meetings),
        "won_revenue_sar": max(0.0, won_revenue_sar),
        "total_performance_fees_sar": None,
        "price_authority": _PRICE_AUTHORITY,
        "automatic_billing_allowed": False,
        "live_charge_allowed": False,
        "note": (
            "Performance economics may be analyzed internally, but any fee requires "
            "an explicit customer-specific commercial agreement and billing authority."
        ),
    }


def estimate_roi(
    *,
    plan_price_sar: float,
    expected_pipeline_sar: float,
    expected_revenue_sar: float,
) -> dict[str, Any]:
    """Internal scenario analysis using a caller-supplied quote amount.

    This does not generate a price, guarantee pipeline/revenue, or constitute a
    customer value claim.
    """
    if plan_price_sar <= 0:
        return {"error": "customer_specific_quote_amount_must_be_positive"}
    pipeline_multiple = round(expected_pipeline_sar / plan_price_sar, 2)
    revenue_multiple = round(expected_revenue_sar / plan_price_sar, 2)
    return {
        "status": "internal_estimate_only",
        "customer_value_claim": False,
        "guarantee": False,
        "quote_amount_source": "caller_supplied_customer_specific_quote",
        "plan_price_sar": plan_price_sar,
        "expected_pipeline_sar": expected_pipeline_sar,
        "expected_revenue_sar": expected_revenue_sar,
        "pipeline_to_subscription_multiple": pipeline_multiple,
        "revenue_to_subscription_multiple": revenue_multiple,
        "price_authority": _PRICE_AUTHORITY,
    }
