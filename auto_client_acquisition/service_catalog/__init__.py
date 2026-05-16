"""Dealix Service Catalog (Wave 13 Phase 2).

Single source of truth for the priced offerings:
- `OFFERINGS` — the canonical 7-offering core ladder.
- `GOVERNED_TIER_OFFERINGS` — 3 higher-tier Governed Revenue & AI Operations
  offers that sit above the core ladder.
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work for free until KPI met"),
no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.registry import (
    ALL_OFFERINGS,
    GOVERNED_TIER_OFFERINGS,
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
    list_governed_tier,
    list_offerings,
)
from auto_client_acquisition.service_catalog.schemas import (
    ServiceOffering,
    ServiceTier,
)

__all__ = [
    "ALL_OFFERINGS",
    "GOVERNED_TIER_OFFERINGS",
    "OFFERINGS",
    "SERVICE_IDS",
    "ServiceOffering",
    "ServiceTier",
    "get_offering",
    "list_governed_tier",
    "list_offerings",
]
