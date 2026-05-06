"""V12.5 RevOps — Gross margin snapshot.

Pure function:
    margin_sar = revenue_sar - delivery_cost_sar - support_cost_sar
    margin_pct = margin_sar / revenue_sar  (if revenue > 0 else None)

For the first paid pilots (≤ 3) margin is largely founder-time-cost,
which the founder may price at 0 (sweat equity) or at an explicit
hourly rate. This module records BOTH so future analysis is honest.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarginSnapshot:
    customer_handle: str
    revenue_sar: int
    delivery_cost_sar: int
    support_cost_sar: int
    other_cost_sar: int
    margin_sar: int
    margin_pct: float | None
    notes: str


def compute_margin(
    *,
    customer_handle: str,
    revenue_sar: int,
    delivery_cost_sar: int = 0,
    support_cost_sar: int = 0,
    other_cost_sar: int = 0,
    notes: str = "",
) -> MarginSnapshot:
    """Compute gross margin for one customer engagement.

    All cost inputs default to 0 (founder sweat equity). Real values
    are encouraged after the first paid pilot for honest per-customer
    economics.
    """
    if revenue_sar < 0:
        raise ValueError("revenue_sar must be ≥ 0")
    for name, val in (("delivery_cost_sar", delivery_cost_sar),
                      ("support_cost_sar", support_cost_sar),
                      ("other_cost_sar", other_cost_sar)):
        if val < 0:
            raise ValueError(f"{name} must be ≥ 0")

    margin_sar = revenue_sar - delivery_cost_sar - support_cost_sar - other_cost_sar
    margin_pct = (margin_sar / revenue_sar) if revenue_sar > 0 else None

    return MarginSnapshot(
        customer_handle=customer_handle,
        revenue_sar=revenue_sar,
        delivery_cost_sar=delivery_cost_sar,
        support_cost_sar=support_cost_sar,
        other_cost_sar=other_cost_sar,
        margin_sar=margin_sar,
        margin_pct=margin_pct,
        notes=notes,
    )
