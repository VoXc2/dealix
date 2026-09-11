"""Best Offers Catalog — best in market, all sectors, all agents, best value."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.best_free_diagnostic import BEST_OFFERS, BestFreeDiagnosticOffer

class BestOfferCatalog:
    def list_best(self, sector: str | None = None) -> list[BestFreeDiagnosticOffer]:
        # Filter by sector if provided, else all
        if sector:
            # Simple: return all best offers for now, but could filter by sector fit
            return BEST_OFFERS
        return BEST_OFFERS

    def top_offer(self, sector: str, buyer: str, problem: str) -> BestFreeDiagnosticOffer:
        # Best thought: match problem to offer
        if "fatoora" in problem.lower() or "zatca" in problem.lower():
            for o in BEST_OFFERS:
                if "zatoora" in o.offer_id or "zatoora" in o.title_en.lower() or "zatca" in o.title_en.lower():
                    return o
        if "ai" in problem.lower():
            for o in BEST_OFFERS:
                if "ai_readiness" in o.offer_id:
                    return o
        # Default best
        return BEST_OFFERS[0]

    def to_dict(self, sector: str | None = None) -> dict[str, Any]:
        offers = self.list_best(sector)
        return {"offers": [o.model_dump() for o in offers], "total": len(offers), "best_in_market": True}

__all__ = ["BestOfferCatalog", "BEST_OFFERS"]
