"""
Unit tests — webhook HMAC signature verification.
اختبارات الوحدة — التحقق من توقيع HMAC للـ webhooks.

Tests HubSpot v3 and Calendly signature verification functions from
api.security.webhook_signatures.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from unittest.mock import patch

import pytest

from api.security.webhook_signatures import (
    verify_calendly_signature,
    verify_hubspot_signature,
)


# ── Helpers ────────────────────────────────────────────────────────

def _hubspot_signature(
    secret: str, method: str, url: str, body: bytes, timestamp: str
) -> str:
    """Recompute the expected HubSpot v3 signature for test assertions."""
    source = f"{method.upper()}{url}{body.decode('utf-8', 'replace')}{timestamp}"
    digest = hmac.new(secret.encode(), source.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def _calendly_header(secret: str, body: bytes, ts: str | None = None) -> str:
    """Build a valid Calendly webhook header string."""
    ts = ts or str(int(time.time()))
    signed = f"{ts}.{body.decode('utf-8', 'replace')}"
    sig = hmac.new(secret.encode(), signed.encode(), hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"


# ── HubSpot tests ─────────────────────────────────────────────────

class TestHubSpotHMAC:
    SECRET = "hubspot-test-secret-key"
    URL = "https://api.dealix.ai/webhooks/hubspot"
    BODY = b'{"event_type":"contact.creation","objectId":12345}'
    METHOD = "POST"
    TS = "1700000000000"

    def _sig(self) -> str:
        return _hubspot_signature(self.SECRET, self.METHOD, self.URL, self.BODY, self.TS)

    def test_valid_signature_passes(self):
        with patch.dict("os.environ", {"HUBSPOT_APP_SECRET": self.SECRET}):
            assert verify_hubspot_signature(
                method=self.METHOD,
                url=self.URL,
                body=self.BODY,
                timestamp=self.TS,
                signature=self._sig(),
            ) is True

    def test_tampered_body_fails(self):
        with patch.dict("os.environ", {"HUBSPOT_APP_SECRET": self.SECRET}):
            tampered = b'{"event_type":"contact.creation","objectId":99999}'
            assert verify_hubspot_signature(
                method=self.METHOD,
                url=self.URL,
                body=tampered,
                timestamp=self.TS,
                signature=self._sig(),
            ) is False

    def test_wrong_secret_fails(self):
        with patch.dict("os.environ", {"HUBSPOT_APP_SECRET": "wrong-secret"}):
            assert verify_hubspot_signature(
                method=self.METHOD,
                url=self.URL,
                body=self.BODY,
                timestamp=self.TS,
                signature=self._sig(),
            ) is False

    def test_missing_secret_fails(self):
        # No env var, no override
        with patch.dict("os.environ", {}, clear=True):
            assert verify_hubspot_signature(
                method=self.METHOD,
                url=self.URL,
                body=self.BODY,
                timestamp=self.TS,
                signature=self._sig(),
            ) is False

    def test_missing_timestamp_fails(self):
        with patch.dict("os.environ", {"HUBSPOT_APP_SECRET": self.SECRET}):
            assert verify_hubspot_signature(
                method=self.METHOD,
                url=self.URL,
                body=self.BODY,
                timestamp=None,
                signature=self._sig(),
            ) is False

    def test_secret_override_kwarg(self):
        """Secret can be passed directly without env var."""
        assert verify_hubspot_signature(
            method=self.METHOD,
            url=self.URL,
            body=self.BODY,
            timestamp=self.TS,
            signature=self._sig(),
            secret=self.SECRET,
        ) is True


# ── Calendly tests ────────────────────────────────────────────────

class TestCalendlyHMAC:
    SECRET = "calendly-test-webhook-secret"
    BODY = b'{"event":"invitee.created","payload":{"uri":"https://example.com"}}'

    def test_valid_signature_passes(self):
        header = _calendly_header(self.SECRET, self.BODY)
        with patch.dict("os.environ", {"CALENDLY_WEBHOOK_SECRET": self.SECRET}):
            assert verify_calendly_signature(body=self.BODY, header=header) is True

    def test_tampered_body_fails(self):
        header = _calendly_header(self.SECRET, self.BODY)
        tampered = b'{"event":"invitee.canceled","payload":{}}'
        with patch.dict("os.environ", {"CALENDLY_WEBHOOK_SECRET": self.SECRET}):
            assert verify_calendly_signature(body=tampered, header=header) is False

    def test_missing_header_fails(self):
        with patch.dict("os.environ", {"CALENDLY_WEBHOOK_SECRET": self.SECRET}):
            assert verify_calendly_signature(body=self.BODY, header=None) is False

    def test_malformed_header_fails(self):
        with patch.dict("os.environ", {"CALENDLY_WEBHOOK_SECRET": self.SECRET}):
            assert verify_calendly_signature(
                body=self.BODY, header="not-a-valid-header"
            ) is False

    def test_secret_override_kwarg(self):
        header = _calendly_header(self.SECRET, self.BODY)
        assert verify_calendly_signature(
            body=self.BODY, header=header, secret=self.SECRET
        ) is True
