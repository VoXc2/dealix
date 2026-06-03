"""Per-service cost estimator.

Cost components:
- ai_cost_sar: estimated AI/LLM costs
- founder_time_minutes: founder hours
- support_time_minutes: CSM/support hours
- delivery_time_minutes: hands-on delivery hours

All fields marked is_estimate=True. Founder calibrates over time.
"""
from __future__ import annotations

from typing import Any, Literal

ServiceType = Literal[
    "diagnostic", "leadops_sprint", "growth_proof_sprint",
    "support_ops_setup", "customer_portal_setup", "executive_pack",
    "proof_pack", "agency_partner_pack",
    "lead_intelligence_sprint", "support_desk_sprint", "quick_win_ops",
]

# Default cost estimates per service (in SAR equivalents).
# Founder time @ ~200 SAR/hr = ~3.33 SAR/min as baseline.
_FOUNDER_RATE_SAR_PER_MIN = 3.33
_AI_AVG_COST_SAR = 0.10  # rough avg per LLM call

_SERVICE_DEFAULTS: dict[ServiceType, dict[str, int | float]] = {
    "diagnostic": {
        "ai_calls_estimate": 3,
        "founder_time_minutes": 30,  # 30-min call + report writing
        "support_time_minutes": 0,
        "delivery_time_minutes": 60,
    },
    "leadops_sprint": {
        "ai_calls_estimate": 40,
        "founder_time_minutes": 240,  # 4 hours over 7 days
        "support_time_minutes": 60,
        "delivery_time_minutes": 360,
    },
    "growth_proof_sprint": {
        "ai_calls_estimate": 30,
        "founder_time_minutes": 180,
        "support_time_minutes": 60,
        "delivery_time_minutes": 240,
    },
    "support_ops_setup": {
        "ai_calls_estimate": 20,
        "founder_time_minutes": 120,
        "support_time_minutes": 60,
        "delivery_time_minutes": 180,
    },
    "customer_portal_setup": {
        "ai_calls_estimate": 5,
        "founder_time_minutes": 30,
        "support_time_minutes": 30,
        "delivery_time_minutes": 60,
    },
    "executive_pack": {
        "ai_calls_estimate": 5,
        "founder_time_minutes": 60,
        "support_time_minutes": 0,
        "delivery_time_minutes": 30,
    },
    "proof_pack": {
        "ai_calls_estimate": 10,
        "founder_time_minutes": 90,
        "support_time_minutes": 0,
        "delivery_time_minutes": 60,
    },
    "agency_partner_pack": {
        "ai_calls_estimate": 50,
        "founder_time_minutes": 480,  # 8 hours
        "support_time_minutes": 120,
        "delivery_time_minutes": 480,
    },
    "lead_intelligence_sprint": {
        "ai_calls_estimate": 15,
        "founder_time_minutes": 180,
        "support_time_minutes": 60,
        "delivery_time_minutes": 240,
    },
    "support_desk_sprint": {
        "ai_calls_estimate": 12,
        "founder_time_minutes": 120,
        "support_time_minutes": 90,
        "delivery_time_minutes": 180,
    },
    "quick_win_ops": {
        "ai_calls_estimate": 8,
        "founder_time_minutes": 90,
        "support_time_minutes": 30,
        "delivery_time_minutes": 120,
    },
}


def estimate_service_cost(*, service_type: str) -> dict[str, Any]:
    """Returns cost breakdown + total. All fields are estimates."""
    defaults = _SERVICE_DEFAULTS.get(
        service_type,  # type: ignore[arg-type]
        {
            "ai_calls_estimate": 5,
            "founder_time_minutes": 60,
            "support_time_minutes": 30,
            "delivery_time_minutes": 60,
        },
    )

    ai_cost_sar = round(defaults["ai_calls_estimate"] * _AI_AVG_COST_SAR, 2)
    founder_cost_sar = round(
        defaults["founder_time_minutes"] * _FOUNDER_RATE_SAR_PER_MIN, 2,
    )
    support_cost_sar = round(
        defaults["support_time_minutes"] * 1.5, 2,  # CSM ~1.5 SAR/min
    )
    delivery_cost_sar = round(
        defaults["delivery_time_minutes"] * 1.0, 2,  # delivery ~1 SAR/min
    )

    total = ai_cost_sar + founder_cost_sar + support_cost_sar + delivery_cost_sar

    return {
        "service_type": service_type,
        "ai_cost_sar": ai_cost_sar,
        "founder_cost_sar": founder_cost_sar,
        "support_cost_sar": support_cost_sar,
        "delivery_cost_sar": delivery_cost_sar,
        "total_cost_sar": round(total, 2),
        "founder_time_minutes": defaults["founder_time_minutes"],
        "support_time_minutes": defaults["support_time_minutes"],
        "delivery_time_minutes": defaults["delivery_time_minutes"],
        "is_estimate": True,
        "source": "revenue_profitability.service_cost (defaults)",
    }
