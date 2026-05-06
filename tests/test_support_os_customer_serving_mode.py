"""Support OS classify — escalation and no-live-send policy."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_support_os_status_guardrails() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/support-os/status")
    assert r.status_code == 200
    g = r.json()["guardrails"]
    assert g["no_live_send"] is True


def test_classify_refund_escalates() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/support-os/classify", json={"message": "I need a refund please"})
    assert r.status_code == 200
    cls = r.json()["classification"]
    assert cls["escalate"] is True
    assert cls["priority"] == "P0"


def test_classify_empty_unknown() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/support-os/classify", json={"message": ""})
    assert r.status_code == 200
    assert r.json()["classification"]["category"] == "unknown"
