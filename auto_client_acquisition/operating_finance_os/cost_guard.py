"""Cost guard — block or warn when AI spend eats too much of offer price."""

from __future__ import annotations


def ai_spend_ratio(price: float, ai_cost: float) -> float:
    if price <= 0:
        return 1.0
    return ai_cost / price


def cost_guard_breached(
    *,
    price: float,
    ai_cost: float,
    max_ai_to_price_ratio: float = 0.12,
) -> bool:
    """True when AI cost exceeds configured share of price."""
    return ai_spend_ratio(price, ai_cost) > max_ai_to_price_ratio


__all__ = ["ai_spend_ratio", "cost_guard_breached"]
