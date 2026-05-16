"""Dealix Service Catalog (Wave 13 Phase 2).

Single source of truth for the 7 priced offerings.
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work for free until KPI met"),
no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.governed_catalog import (
    GOVERNED_SERVICE_IDS,
    GOVERNED_SERVICES,
    GovernedService,
    get_governed_service,
    list_governed_services,
    list_headline_services,
)
from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
    list_offerings,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering

__all__ = [
    "GOVERNED_SERVICES",
    "GOVERNED_SERVICE_IDS",
    "GovernedService",
    "OFFERINGS",
    "SERVICE_IDS",
    "ServiceOffering",
    "get_governed_service",
    "get_offering",
    "list_governed_services",
    "list_headline_services",
    "list_offerings",
]
