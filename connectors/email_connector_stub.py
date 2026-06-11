"""Email connector stub — implementation pending token."""
from __future__ import annotations

from base import BaseConnector, ConnectorManifest


class EmailConnectorStub(BaseConnector):
    manifest = ConnectorManifest(
        name="Email (SMTP/transactional)",
        source_type="email_provider",
        allowed_use="Send approved outreach drafts",
        restricted_use=["Bulk unsolicited", "Without unsubscribe link"],
        risk_level="medium",
        terms_review_required=True,
        notes="Stub. Implementation requires EMAIL_PROVIDER_API_KEY.",
    )

    def fetch_or_load(self):
        raise NotImplementedError

    def normalize(self, raw):
        return raw

    def validate(self, record):
        return False
