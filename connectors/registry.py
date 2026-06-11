"""Registry of all known connectors."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from csv_connector import CSVConnector
from manual_research_connector import ManualResearchConnector
from website_signal_analyzer import WebsiteSignalAnalyzer
from hubspot_connector_stub import HubSpotConnectorStub
from google_places_connector_stub import GooglePlacesConnectorStub
from whatsapp_business_connector_stub import WhatsAppBusinessConnectorStub
from email_connector_stub import EmailConnectorStub


def all_connectors():
    return [
        CSVConnector(),
        ManualResearchConnector(),
        WebsiteSignalAnalyzer(),
        HubSpotConnectorStub(),
        GooglePlacesConnectorStub(),
        WhatsAppBusinessConnectorStub(),
        EmailConnectorStub(),
    ]
