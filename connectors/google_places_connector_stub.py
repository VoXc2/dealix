"""Google Places connector stub — implementation pending GOOGLE_PLACES_API_KEY."""
from __future__ import annotations

from base import BaseConnector, ConnectorManifest


class GooglePlacesConnectorStub(BaseConnector):
    manifest = ConnectorManifest(
        name="Google Places API",
        source_type="google_places",
        allowed_use="Public business profile (address, hours, rating)",
        restricted_use=["Personal data", "Write calls"],
        risk_level="low",
        terms_review_required=True,
        notes="Stub. Implementation requires GOOGLE_PLACES_API_KEY + ToS review.",
    )

    def fetch_or_load(self):  # pragma: no cover
        raise NotImplementedError("Google Places connector not yet implemented. Requires GOOGLE_PLACES_API_KEY.")

    def normalize(self, raw):  # pragma: no cover
        return raw

    def validate(self, record):  # pragma: no cover
        return False
