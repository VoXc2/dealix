"""Delivery OS thin router delegates to delivery_factory."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_delivery_os_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/delivery-os/status")
    assert r.status_code == 200
    assert r.json()["module"] == "delivery_os"
