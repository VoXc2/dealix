"""Dealix Service Catalog.

Single source of truth for the canonical commercial catalog: a five-rung
service ladder (Free Diagnostic, Sprint, Pilot, Retainer/Managed Ops,
Enterprise/Custom AI) plus the Agency Partner distribution channel.
Backend + portal + WhatsApp + landing pages all read from here.

Article 8: commitment language only ("we will work at no extra cost until
the KPI is met"), no "guaranteed"/"نضمن".
Article 11: thin data registry — no business logic.
"""

from auto_client_acquisition.service_catalog.registry import (
    CHANNEL_OFFERINGS,
    OFFERINGS,
    RUNGS,
    SERVICE_IDS,
    get_offering,
    list_offerings,
    list_rungs,
)
from auto_client_acquisition.service_catalog.schemas import ServiceOffering

__all__ = [
    "CHANNEL_OFFERINGS",
    "OFFERINGS",
    "RUNGS",
    "SERVICE_IDS",
    "ServiceOffering",
    "get_offering",
    "list_offerings",
    "list_rungs",
]
