"""Finance Radar — top-3 at-risk + top-3 unprofitable services.

Wraps revenue_truth + gross_margin into a single founder-facing
summary suitable for Executive Command Center.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def finance_radar_summary() -> dict[str, Any]:
    """Returns top-3 at-risk + top-3 unprofitable + summary stats."""
    return safe_call(
        name="finance_radar_summary",
        fn=_compute,
        fallback={
            "at_risk_top_3": [],
            "unprofitable_top_3": [],
            "confirmed_revenue_sar": 0.0,
            "is_estimate": True,
            "source": "insufficient_data",
        },
    )


def _compute() -> dict[str, Any]:
    from auto_client_acquisition.revenue_profitability.gross_margin import (
        compute_gross_margin,
    )
    from auto_client_acquisition.revenue_profitability.revenue_truth import (
        revenue_summary,
    )
    from auto_client_acquisition.service_sessions import list_sessions

    sessions = list_sessions(limit=200)

    # At-risk = sessions stuck in waiting_for_approval or blocked
    at_risk = [
        {
            "session_id": s.session_id,
            "customer_handle": s.customer_handle,
            "service_type": s.service_type,
            "status": s.status,
        }
        for s in sessions
        if s.status in ("waiting_for_approval", "blocked")
    ][:3]

    # Unprofitable: estimate per service_type's package price minus cost.
    # Without confirmed revenue per session, we use *typical pricing* as
    # an indicator (NOT actual revenue — that requires payment_confirmed).
    package_prices: dict[str, float] = {
        "diagnostic": 0.0,
        "leadops_sprint": 499.0,
        "growth_proof_sprint": 1500.0,
        "support_ops_setup": 1500.0,
        "customer_portal_setup": 0.0,
        "executive_pack": 7500.0,
        "proof_pack": 0.0,
        "agency_partner_pack": 0.0,  # custom
        "lead_intelligence_sprint": 12000.0,
        "support_desk_sprint": 15000.0,
        "quick_win_ops": 10000.0,
    }
    unprofitable: list[dict[str, Any]] = []
    for service_type, indicative_price in package_prices.items():
        if indicative_price <= 0:
            continue
        margin = compute_gross_margin(
            service_type=service_type,
            revenue_sar=indicative_price,
        )
        if not margin["is_profitable"]:
            unprofitable.append({
                "service_type": service_type,
                "indicative_price_sar": indicative_price,
                "estimated_cost_sar": margin["total_cost_sar"],
                "estimated_margin_sar": margin["gross_margin_sar"],
                "is_estimate": True,
            })
    unprofitable.sort(key=lambda x: x["estimated_margin_sar"])
    unprofitable_top_3 = unprofitable[:3]

    revenue = revenue_summary()

    return {
        "at_risk_top_3": at_risk,
        "unprofitable_top_3": unprofitable_top_3,
        "confirmed_revenue_sar": revenue.get("confirmed_revenue_sar", 0.0),
        "net_revenue_sar": revenue.get("net_revenue_sar", 0.0),
        "is_estimate": True,
        "source": "revenue_profitability.finance_radar",
    }
