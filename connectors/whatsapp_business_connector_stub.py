"""WhatsApp Business connector stub — implementation pending token + template approval."""
from __future__ import annotations

from base import BaseConnector, ConnectorManifest


class WhatsAppBusinessConnectorStub(BaseConnector):
    manifest = ConnectorManifest(
        name="WhatsApp Business (official API)",
        source_type="whatsapp_business",
        allowed_use="Send approved outreach drafts via approved templates",
        restricted_use=["Unapproved templates", "Group messages to non-consenting contacts", "Bulk unsolicited"],
        risk_level="high",
        terms_review_required=True,
        notes="Stub. Implementation requires WHATSAPP_BUSINESS_TOKEN + approved templates.",
    )

    def fetch_or_load(self):  # pragma: no cover
        raise NotImplementedError("WhatsApp Business connector not yet implemented.")

    def normalize(self, raw):  # pragma: no cover
        return raw

    def validate(self, record):  # pragma: no cover
        return False
