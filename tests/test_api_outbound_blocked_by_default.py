"""Tests that outbound send endpoints are blocked by default."""

import os

import pytest
from fastapi.testclient import TestClient

import app.outbound.policy_gate as policy_gate

# Set safe env before importing app
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
            "channel": "email",
            "to": "test@example.com",
            "subject": "Test",
            "body": "Test body",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        assert data["mode"] == "draft_only"
        assert data["reason"] == "external_send_disabled"

    def test_send_whatsapp_blocked(self):
        response = client.post("/api/outbound/send/whatsapp", json={
            "channel": "whatsapp",
            "to": "+966****0000",
            "body": "Test message",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        # WhatsApp may be blocked because it's not enabled/live, or because
        # external send is globally disabled. Both are valid safety responses.
        assert data["reason"] in ("external_send_disabled", "whatsapp_not_enabled_or_not_live")

    def test_send_sms_blocked(self):
        response = client.post("/api/outbound/send/sms", json={
            "channel": "sms",
            "to": "+966500000000",
            "body": "Test SMS",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is False
        assert data["safe_to_send"] is False
        assert data["reason"] == "external_send_disabled"

    def test_outbound_safety_status(self):
        response = client.get("/api/outbound/safety")
        assert response.status_code == 200
        data = response.json()
        assert data["external_send_enabled"] is False
        assert data["outbound_mode"] == "draft_only"
        assert data["email_send_enabled"] is False
        assert data["whatsapp_send_enabled"] is False
        assert data["whatsapp_allow_live_send"] is False
        assert data["sms_send_enabled"] is False
        assert data["safe_to_send"] is False

    def test_outbound_channels(self):
        response = client.get("/api/outbound/channels")
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "whatsapp" in data
        assert "sms" in data
        assert data["email"]["enabled"] is False
        assert data["whatsapp"]["enabled"] is False
        assert data["sms"]["enabled"] is False

    def test_email_readiness_not_ready(self):
        response = client.get("/api/outbound/readiness/email")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is False

    def test_whatsapp_readiness_not_ready(self):
        response = client.get("/api/outbound/readiness/whatsapp")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is False

    def test_sms_readiness_not_ready(self):
        response = client.get("/api/outbound/readiness/sms")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is False


def test_controlled_live_api_blocks_memory_suppression_backend(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")

    response = client.post(
        "/api/outbound/send/email",
        json={
            "channel": "email",
            "to": "test@example.com",
            "subject": "Test",
            "body": "Test body. Unsubscribe anytime.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is False
    assert data["safe_to_send"] is False
    assert "persistent suppression backend is not verified" in data["reasons"]

    readiness = client.get("/api/outbound/readiness/email").json()
    assert readiness["ready"] is False
    assert readiness["reason"] == "persistent_suppression_not_verified"

    safety = client.get("/api/outbound/safety").json()
    assert safety["safe_to_send"] is False
    assert safety["persistent_suppression_ready"] is False
    assert safety["reason"] == "persistent_suppression_not_verified"


def test_active_api_requires_recipient_policy_evidence_even_when_durable(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setattr(policy_gate, "persistent_suppression_ready", lambda: True)

    response = client.post(
        "/api/outbound/send/email",
        json={
            "channel": "email",
            "to": "test@example.com",
            "subject": "Test",
            "body": "Test body. Unsubscribe anytime.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is False
    assert data["safe_to_send"] is False
    assert data["reason"] == "message.status must be approved"
