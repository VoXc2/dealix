"""Dealix Service Catalog (Wave 13 Phase 2).

Single source of truth for the 7 priced offerings.
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work for free until KPI met"),
no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
    list_offerings,
)
from auto_client_acquisition.service_catalog.governed_revenue_ai_ops import (
    build_governed_revenue_ai_ops_blueprint,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering

__all__ = [
    "OFFERINGS",
    "SERVICE_IDS",
    "ServiceOffering",
    "build_governed_revenue_ai_ops_blueprint",
    "get_offering",
    "list_offerings",
]
