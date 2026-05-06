"""Rough gross-margin estimate from delivery/support hour assumptions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MarginInputs:
    revenue_sar: int
    delivery_hours: float
    support_hours: float
    delivery_hour_cost_sar: float = 120.0
    support_hour_cost_sar: float = 90.0
    refund_risk_factor: float = 0.0  # 0..1 reduces confidence, not SAR directly


def estimate_margin(inp: MarginInputs) -> dict[str, Any]:
    """Deterministic margin sketch — not accounting-grade."""
    if inp.revenue_sar <= 0:
        return {
            "schema_version": 1,
            "revenue_sar": 0,
            "variable_cost_sar": 0.0,
            "gross_margin_sar": 0.0,
            "gross_margin_pct": None,
            "confidence": "none",
            "refund_risk_factor": inp.refund_risk_factor,
        }

    delivery_cost = inp.delivery_hours * inp.delivery_hour_cost_sar
    support_cost = inp.support_hours * inp.support_hour_cost_sar
    variable = delivery_cost + support_cost
    gm = float(inp.revenue_sar) - variable
    pct = (gm / float(inp.revenue_sar)) * 100.0 if inp.revenue_sar else None
    confidence = "high" if inp.refund_risk_factor <= 0.1 else "medium"

    return {
        "schema_version": 1,
        "revenue_sar": inp.revenue_sar,
        "delivery_cost_sar": round(delivery_cost, 2),
        "support_cost_sar": round(support_cost, 2),
        "variable_cost_sar": round(variable, 2),
        "gross_margin_sar": round(gm, 2),
        "gross_margin_pct": round(pct, 2) if pct is not None else None,
        "confidence": confidence,
        "refund_risk_factor": inp.refund_risk_factor,
    }
