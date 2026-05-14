"""Founder Launch Status — Wave 15 (A2)."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_public_endpoint_returns_required_fields():
    resp = client.get("/api/v1/founder/launch-status/public")
    assert resp.status_code == 200
    body = resp.json()
    for field in (
        "generated_at",
        "healthcheck_ok",
        "moyasar_mode",
        "zatca_mode",
        "gmail_configured",
        "calendly_url",
        "governance_decision",
    ):
        assert field in body, f"missing field: {field}"
    assert body["governance_decision"] == "allow"


def test_admin_endpoint_requires_admin_key():
    resp = client.get("/api/v1/founder/launch-status")
    assert resp.status_code in {401, 403}


def test_public_endpoint_does_not_leak_secrets():
    body = client.get("/api/v1/founder/launch-status/public").json()
    # Must never return raw keys.
    assert "MOYASAR_SECRET_KEY" not in str(body)
    assert "sk_live_" not in str(body)
    assert "sk_test_" not in str(body)
    assert "GMAIL_CLIENT_SECRET" not in str(body)


def test_moyasar_mode_one_of_known_values():
    body = client.get("/api/v1/founder/launch-status/public").json()
    assert body["moyasar_mode"] in {"live", "test", "unconfigured"}


def test_zatca_mode_one_of_known_values():
    body = client.get("/api/v1/founder/launch-status/public").json()
    assert body["zatca_mode"] in {"live", "sandbox"}
