"""Compliance action-check matrix."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_cold_whatsapp_blocked() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/compliance-os/action-check", json={"action_type": "cold_whatsapp"})
    assert r.status_code == 200
    assert r.json()["decision"] == "blocked"


def test_warm_intro_requires_approval() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/compliance-os/action-check", json={"action_type": "warm_intro_message_send"})
    assert r.status_code == 200
    assert r.json()["action_mode"] == "approval_required"


def test_warm_intro_allowed_manual_with_flags() -> None:
    c = TestClient(create_app())
    r = c.post(
        "/api/v1/compliance-os/action-check",
        json={"action_type": "warm_intro_message_send", "has_consent": True, "founder_approved": True},
    )
    assert r.status_code == 200
    assert r.json()["action_mode"] == "approved_manual"
