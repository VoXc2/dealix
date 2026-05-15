"""Offer-level unit economics (deterministic; currency-agnostic numbers)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OfferUnitEconomics:
    offer_id: str
    price: float
    delivery_hours: float
    qa_hours: float
    governance_overhead_hours: float
    ai_cost: float
    blended_hour_cost: float

    @property
    def delivery_cost(self) -> float:
        hours = self.delivery_hours + self.qa_hours + self.governance_overhead_hours
        return hours * self.blended_hour_cost

    @property
    def gross_margin(self) -> float:
        if self.price <= 0:
            return 0.0
        return max(0.0, (self.price - self.delivery_cost - self.ai_cost) / self.price)


__all__ = ["OfferUnitEconomics"]
