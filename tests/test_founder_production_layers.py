"""Founder production-layers endpoint smoke tests."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import founder_launch_status, health, platform_meta


def _app() -> FastAPI:
    mini = FastAPI()
    mini.include_router(health.router)
    mini.include_router(platform_meta.router)
    mini.include_router(founder_launch_status.router)
    return mini


def test_production_layers_requires_admin_key() -> None:
    client = TestClient(_app())
    r = client.get("/api/v1/founder/production-layers")
    assert r.status_code in (401, 403, 422)


def test_production_layers_ok_with_admin_key(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin-key")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@localhost:5432/x")
    monkeypatch.setenv("APP_SECRET_KEY", "a" * 64)
    client = TestClient(_app())
    r = client.get(
        "/api/v1/founder/production-layers",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] in ("PASS", "WARN", "FAIL")
    assert len(body["layers"]) == 6
    assert body["trust_routes_registered"]["version"] is True
