"""GTM public surfaces registry tests."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import health, platform_meta
from dealix.commercial_ops.gtm_public_surfaces import (
    build_gtm_public_surfaces_snapshot,
    verify_gtm_public_surfaces_repo,
)


def test_gtm_public_surfaces_repo_ok() -> None:
    repo = verify_gtm_public_surfaces_repo()
    assert repo["ok"], repo["issues"]


def test_gtm_public_surfaces_snapshot_has_routes() -> None:
    snap = build_gtm_public_surfaces_snapshot()
    assert len(snap["frontend_public_routes"]) >= 5
    assert len(snap["api_trust_endpoints"]) >= 4


def _trust_layer_app() -> FastAPI:
    """Minimal app — avoids full api.main optional-router import chain."""
    mini = FastAPI()
    mini.include_router(health.router)
    mini.include_router(platform_meta.router)
    return mini


def test_version_and_meta_public() -> None:
    client = TestClient(_trust_layer_app())
    ver = client.get("/version")
    assert ver.status_code == 200
    body = ver.json()
    assert body["status"] == "ok"
    assert "version" in body

    meta = client.get("/api/v1/meta")
    assert meta.status_code == 200
    assert "surfaces" in meta.json()


def test_healthz_includes_version() -> None:
    client = TestClient(_trust_layer_app())
    hz = client.get("/healthz")
    assert hz.status_code == 200
    assert hz.json().get("version")
