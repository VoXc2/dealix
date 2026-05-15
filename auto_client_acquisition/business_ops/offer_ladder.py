"""Wave 9 — Offer Ladder.

The 7-rung commercial ladder customers climb. Each rung is derived from the
canonical service catalog (``service_catalog.registry``) — pricing and KPI
commitments are never re-stated here, only referenced, so a price change is a
1-line edit to the registry.

Constitution: KPI language is commitment, never guarantee. Estimated outcomes
are not guaranteed outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    get_offering,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering


@dataclass(frozen=True, slots=True)
class OfferRung:
    """One rung on the offer ladder, backed by a canonical ServiceOffering."""

    rung: int
    service_id: str
    journey_stage: str

    @property
    def offering(self) -> ServiceOffering | None:
        """The canonical ServiceOffering for this rung."""
        return get_offering(self.service_id)

    def to_dict(self) -> dict[str, Any]:
        offering = self.offering
        return {
            "rung": self.rung,
            "service_id": self.service_id,
            "journey_stage": self.journey_stage,
            "name_en": offering.name_en if offering else "",
            "name_ar": offering.name_ar if offering else "",
            "price_sar": offering.price_sar if offering else 0.0,
            "price_unit": offering.price_unit if offering else "",
        }


# The 7-rung ladder, ascending. Order mirrors the canonical catalog.
OFFER_LADDER: dict[str, OfferRung] = {
    offering.id: OfferRung(
        rung=index + 1,
        service_id=offering.id,
        journey_stage=offering.customer_journey_stage,
    )
    for index, offering in enumerate(OFFERINGS)
}


def get_offer(service_id: str) -> OfferRung | None:
    """Return one rung of the offer ladder by service id, or None."""
    return OFFER_LADDER.get(service_id)


def list_offers() -> list[OfferRung]:
    """All 7 rungs in ascending ladder order."""
    return sorted(OFFER_LADDER.values(), key=lambda r: r.rung)


__all__ = ["OFFER_LADDER", "OfferRung", "get_offer", "list_offers"]
