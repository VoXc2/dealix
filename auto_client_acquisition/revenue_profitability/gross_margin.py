"""Gross margin estimator.

For one service session: revenue − total_cost = gross_margin.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_profitability.service_cost import (
    estimate_service_cost,
)


def compute_gross_margin(
    *,
    service_type: str,
    revenue_sar: float,
) -> dict[str, Any]:
    """Returns {revenue_sar, total_cost_sar, gross_margin_sar, gross_margin_pct, is_estimate}.

    Revenue is taken AS-GIVEN (caller is responsible for using only
    payment_confirmed amounts — see revenue_truth.is_revenue).
    """
    cost = estimate_service_cost(service_type=service_type)
    total_cost = cost["total_cost_sar"]
    margin = round(revenue_sar - total_cost, 2)
    margin_pct = round((margin / revenue_sar * 100), 1) if revenue_sar > 0 else 0.0

    return {
        "service_type": service_type,
        "revenue_sar": round(revenue_sar, 2),
        "total_cost_sar": total_cost,
        "gross_margin_sar": margin,
        "gross_margin_pct": margin_pct,
        "is_estimate": True,  # margin is estimate (cost side is estimate)
        "is_profitable": margin > 0,
        "cost_breakdown": cost,
        "source": "revenue_profitability.gross_margin",
    }
