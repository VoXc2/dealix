"""Dealix Service Catalog (Wave 13 Phase 2).

Single source of truth for the 7 priced offerings.
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work for free until KPI met"),
no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.enterprise_registry import (
    ENTERPRISE_OFFERING_IDS,
    ENTERPRISE_OFFERINGS,
    get_enterprise_offering,
    get_enterprise_tier,
    list_enterprise_offerings,
)
from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
    list_offerings,
)
from auto_client_acquisition.service_catalog.schemas import (
    EnterpriseOffering,
    PricingTier,
    ServiceOffering,
)

__all__ = [
    "ENTERPRISE_OFFERINGS",
    "ENTERPRISE_OFFERING_IDS",
    "EnterpriseOffering",
    "OFFERINGS",
    "PricingTier",
    "SERVICE_IDS",
    "ServiceOffering",
    "get_enterprise_offering",
    "get_enterprise_tier",
    "get_offering",
    "list_enterprise_offerings",
    "list_offerings",
]
