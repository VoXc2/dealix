"""Platform trust layer — /version and /api/v1/meta (Layer 0/3 probes)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


def test_version_endpoint() -> None:
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert body.get("version")
    assert body.get("meta") == "/api/v1/meta"


def test_api_v1_meta_endpoint() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/meta")
    assert r.status_code == 200
    body = r.json()
    assert body.get("version")
    assert body.get("surfaces") is not None
    assert body.get("canonical_links", {}).get("revenue_os_catalog")


def test_mcp_tools_read_only() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/mcp/tools")
    assert r.status_code == 200
    body = r.json()
    assert body.get("read_only") is True
    assert body.get("external_send") is False
    assert len(body.get("tools") or []) >= 3


def test_healthz_includes_version() -> None:
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body.get("version")
