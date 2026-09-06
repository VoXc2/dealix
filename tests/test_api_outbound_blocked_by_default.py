"""Tests that outbound send endpoints are blocked by default."""

import os

from fastapi.testclient import TestClient

import app.outbound.policy_gate as policy_gate

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dealix_test_outbound.db")
os.environ.setdefault("APP_SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("API_KEYS", "test")
os.environ.setdefault("ADMIN_API_KEYS", "admin")
os.environ.setdefault("EXTERNAL_SEND_ENABLED", "false")
os.environ.setdefault("OUTBOUND_MODE", "draft_only")
os.environ.setdefault("EMAIL_SEND_ENABLED", "false")
os.environ.setdefault("WHATSAPP_SEND_ENABLED", "false")
os.environ.setdefault("WHATSAPP_ALLOW_LIVE_SEND", "false")
os.environ.setdefault("SMS_SEND_ENABLED", "false")

from api.main import app

client = TestClient(app, raise_server_exceptions=False)


class TestOutboundBlockedByDefault:
    def test_send_email_blocked(self):
        response = client.post("/api/outbound/send/email", json={
            "channel": "email", "to": "test@example.com", "subject": "Test", "body": "Test body",
        })
        data = response.json()
        assert response.status_code == 200
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        assert data["mode"] == "draft_only"
        assert data["reason"] == "external_send_disabled"

    def test_send_whatsapp_blocked(self):
        response = client.post("/api/outbound/send/whatsapp", json={
            "channel": "whatsapp", "to": "+966****0000", "body": "Test message",
        })
        data = response.json()
        assert response.status_code == 200
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        assert data["reason"] in ("external_send_disabled", "whatsapp_not_enabled_or_not_live")

    def test_send_sms_blocked(self):
        response = client.post("/api/outbound/send/sms", json={
            "channel": "sms", "to": "+966500000000", "body": "Test SMS",
        })
        data = response.json()
        assert response.status_code == 200
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        assert data["reason"] == "external_send_disabled"

    def test_outbound_safety_status(self):
        data = client.get("/api/outbound/safety").json()
        assert data["external_send_enabled"] is False
        assert data["outbound_mode"] == "draft_only"
        assert data["email_send_enabled"] is False
        assert data["whatsapp_send_enabled"] is False
        assert data["whatsapp_allow_live_send"] is False
        assert data["sms_send_enabled"] is False
        assert data["persistent_suppression_ready"] is False
        assert data["persistent_consent_ready"] is False
        assert data["safe_to_send"] is False

    def test_outbound_channels(self):
        data = client.get("/api/outbound/channels").json()
        assert set(("email", "whatsapp", "sms")).issubset(data)
        assert data["email"]["enabled"] is False
        assert data["whatsapp"]["enabled"] is False
        assert data["sms"]["enabled"] is False

    def test_email_readiness_not_ready(self):
        assert client.get("/api/outbound/readiness/email").json()["ready"] is False

    def test_whatsapp_readiness_not_ready(self):
        assert client.get("/api/outbound/readiness/whatsapp").json()["ready"] is False

    def test_sms_readiness_not_ready(self):
        assert client.get("/api/outbound/readiness/sms").json()["ready"] is False


def test_controlled_live_api_blocks_memory_suppression_backend(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")

    data = client.post(
        "/api/outbound/send/email",
        json={"channel": "email", "to": "test@example.com", "subject": "Test", "body": "Test body. Unsubscribe anytime."},
    ).json()
    assert data["allowed"] is False
    assert data["safe_to_send"] is False
    assert "persistent suppression backend is not verified" in data["reasons"]

    readiness = client.get("/api/outbound/readiness/email").json()
    assert readiness["ready"] is False
    assert readiness["reason"] == "persistent_suppression_not_verified"

    safety = client.get("/api/outbound/safety").json()
    assert safety["safe_to_send"] is False
    assert safety["persistent_suppression_ready"] is False
    assert safety["persistent_consent_ready"] is False
    assert safety["reason"] == "persistent_suppression_not_verified"


def test_controlled_live_api_blocks_memory_consent_after_suppression_is_durable(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)

    readiness = client.get("/api/outbound/readiness/email").json()
    assert readiness["ready"] is False
    assert readiness["reason"] == "persistent_consent_not_verified"

    safety = client.get("/api/outbound/safety").json()
    assert safety["persistent_suppression_ready"] is True
    assert safety["persistent_consent_ready"] is False
    assert safety["reason"] == "persistent_consent_not_verified"


def test_active_api_requires_recipient_policy_evidence_even_when_durable(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)
    monkeypatch.setattr(policy_gate, "persistent_consent_ready", lambda: True)

    data = client.post(
        "/api/outbound/send/email",
        json={"channel": "email", "to": "test@example.com", "subject": "Test", "body": "Test body. Unsubscribe anytime."},
    ).json()
    assert data["allowed"] is False
    assert data["safe_to_send"] is False
    assert data["reason"] == "message.status must be approved"
