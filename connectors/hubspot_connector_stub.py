"""HubSpot connector stub — implementation pending HUBSPOT_PRIVATE_APP_TOKEN."""
from __future__ import annotations

from base import BaseConnector, ConnectorManifest


class HubSpotConnectorStub(BaseConnector):
    manifest = ConnectorManifest(
        name="HubSpot CRM (official API)",
        source_type="hubspot",
        allowed_use="Read deals/contacts from a HubSpot portal the client owns",
        restricted_use=["Write to HubSpot", "Read from portals not owned by client"],
        risk_level="medium",
        terms_review_required=True,
        notes="Stub. Implementation requires HUBSPOT_PRIVATE_APP_TOKEN + OAuth scope review.",
    )

    def fetch_or_load(self):  # pragma: no cover
        raise NotImplementedError("HubSpot connector not yet implemented. Requires HUBSPOT_PRIVATE_APP_TOKEN.")

    def normalize(self, raw):  # pragma: no cover
        return raw

    def validate(self, record):  # pragma: no cover
        return False
