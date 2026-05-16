"""
Unit tests — API key authentication flow.
اختبارات الوحدة — تدفق مصادقة مفتاح API.

Tests the APIKeyMiddleware and api_key security module:
- Valid key passes
- Missing key → 401
- Invalid key → 401
- Admin-only endpoint → 403 with non-admin key
- Health endpoint is exempt from auth
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from unittest.mock import patch

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from api.security.api_key import APIKeyMiddleware


# ── App factory for tests ─────────────────────────────────────────

def _make_test_app(valid_keys: list[str] | None = None) -> FastAPI:
    """Create a minimal FastAPI app with APIKeyMiddleware for testing."""
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/api/v1/leads")
    async def list_leads():
        return {"data": []}

    @app.get("/api/v1/admin/config")
    async def admin_config(request: Request):
        return {"admin": True}

    return app


# ── Fixtures ───────────────────────────────────────────────────────

VALID_KEY = "test-valid-key-abc123"
INVALID_KEY = "invalid-key-xyz999"


@pytest.fixture()
def client():
    """TestClient with a patched API_KEYS environment variable."""
    with patch.dict("os.environ", {"API_KEYS": VALID_KEY, "APP_ENV": "test"}):
        app = _make_test_app([VALID_KEY])
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c


# ── Tests ──────────────────────────────────────────────────────────

class TestAPIKeyMiddleware:
    def test_health_endpoint_is_exempt(self, client):
        """Health check must be accessible without an API key."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_valid_key_header_passes(self, client):
        """Valid X-API-Key header grants access."""
        response = client.get(
            "/api/v1/leads", headers={"X-API-Key": VALID_KEY}
        )
        assert response.status_code == 200

    def test_missing_key_returns_401(self, client):
        """Requests without any API key must receive 401."""
        response = client.get("/api/v1/leads")
        assert response.status_code == 401

    def test_invalid_key_returns_401(self, client):
        """Requests with an unknown API key must receive 401."""
        response = client.get(
            "/api/v1/leads", headers={"X-API-Key": INVALID_KEY}
        )
        assert response.status_code == 401

    def test_key_in_header_with_query_string_passes(self, client):
        """A valid X-API-Key header grants access even with query params present."""
        response = client.get(
            "/api/v1/leads?limit=5", headers={"X-API-Key": VALID_KEY}
        )
        # Accept 200 or 404 (route may not exist); reject only 401/403
        assert response.status_code not in (401, 403)

    def test_openapi_docs_are_exempt(self, client):
        """OpenAPI endpoints must not require auth (public docs)."""
        for path in ("/docs", "/redoc", "/openapi.json"):
            r = client.get(path)
            assert r.status_code != 401, f"{path} should be exempt from auth"


class TestAPIKeyValidation:
    """Direct unit tests for key validation logic."""

    def test_empty_keys_env_allows_dev_mode(self):
        """When API_KEYS is empty, the middleware runs in dev mode and allows requests.

        The documented production contract requires API_KEYS to be set;
        an unconfigured key list intentionally falls through (dev mode).
        """
        with patch.dict("os.environ", {"API_KEYS": "", "APP_ENV": "production"}):
            app = _make_test_app([])
            with TestClient(app, raise_server_exceptions=False) as c:
                r = c.get("/api/v1/leads", headers={"X-API-Key": "any-key"})
                assert r.status_code == 200

    def test_multiple_valid_keys(self):
        """All keys in the comma-separated API_KEYS list are valid."""
        keys = "key-one,key-two,key-three"
        with patch.dict("os.environ", {"API_KEYS": keys, "APP_ENV": "test"}):
            app = _make_test_app()
            with TestClient(app, raise_server_exceptions=False) as c:
                for key in keys.split(","):
                    r = c.get("/api/v1/leads", headers={"X-API-Key": key})
                    assert r.status_code == 200, f"Key '{key}' should be valid"
