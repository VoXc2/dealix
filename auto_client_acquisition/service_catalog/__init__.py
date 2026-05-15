"""Dealix Service Catalog (Wave 13 Phase 2 + Enterprise tier).

Single source of truth for the 12 priced offerings (7 ladder + 5 enterprise).
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work for free until KPI met"),
no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.registry import (
    ENTERPRISE_SERVICE_IDS,
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
    list_enterprise_offerings,
    list_offerings,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering

__all__ = [
    "ENTERPRISE_SERVICE_IDS",
    "OFFERINGS",
    "SERVICE_IDS",
    "ServiceOffering",
    "get_offering",
    "list_enterprise_offerings",
    "list_offerings",
]
