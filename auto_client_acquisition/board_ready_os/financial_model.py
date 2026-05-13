"""Financial Model — per-offer unit economics with minimum-margin targets."""

from __future__ import annotations

from dataclasses import dataclass


# Doctrine minimum gross margin targets per offer category.
_MIN_MARGIN: dict[str, float] = {
    "diagnostic": 0.75,
    "sprint": 0.65,
    "pilot": 0.55,
    "retainer": 0.65,
    "enterprise": 0.50,
    "academy": 0.80,
    "platform": 0.80,
}


@dataclass(frozen=True)
class OfferUnitEconomics:
    offer_id: str
    offer_category: str  # one of the keys in _MIN_MARGIN
    price: float
    delivery_hours: float
    ai_cost: float
    review_hours: float
    qa_hours: float
    governance_overhead: float
    revision_risk: float
    communication_cost: float

    def total_cost(self) -> float:
        return (
            self.ai_cost
            + self.governance_overhead
            + self.revision_risk
            + self.communication_cost
            + (self.delivery_hours + self.review_hours + self.qa_hours)
        )

    def gross_margin(self) -> float:
        if self.price <= 0:
            return 0.0
        return max(0.0, (self.price - self.total_cost()) / self.price)


def is_offer_healthy(offer: OfferUnitEconomics) -> tuple[bool, str | None]:
    target = _MIN_MARGIN.get(offer.offer_category)
    if target is None:
        return (False, f"unknown_category:{offer.offer_category}")
    margin = offer.gross_margin()
    if margin < target:
        return (False, f"margin_below_target:{margin:.2f}<{target:.2f}")
    return (True, None)
