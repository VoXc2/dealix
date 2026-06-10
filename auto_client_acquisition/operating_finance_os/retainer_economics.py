"""Retainer economics — simple health signal from MRR vs monthly delivery load."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetainerEconomics:
    mrr: float
    monthly_delivery_hours: float
    monthly_ai_cost: float
    blended_hour_cost: float

    @property
    def implied_load_cost(self) -> float:
        return self.monthly_delivery_hours * self.blended_hour_cost + self.monthly_ai_cost

    @property
    def health_ratio(self) -> float:
        """>1 means MRR comfortably covers implied load + AI (rough)."""
        if self.implied_load_cost <= 0:
            return 999.0
        return self.mrr / self.implied_load_cost


__all__ = ["RetainerEconomics"]
