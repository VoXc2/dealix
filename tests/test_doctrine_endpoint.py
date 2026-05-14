"""Tests for the public /api/v1/doctrine endpoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.doctrine import router as doctrine_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(doctrine_router)
    return TestClient(app)


def test_doctrine_endpoint_returns_200():
    r = _client().get("/api/v1/doctrine")
    assert r.status_code == 200


def test_doctrine_endpoint_pinned_to_commit_sha():
    body = _client().get("/api/v1/doctrine").json()
    sha = body["commit_sha"]
    assert isinstance(sha, str)
    # Either a real 40-char hex sha, or the explicit fallback.
    assert sha == "unknown" or len(sha) == 40


def test_doctrine_endpoint_lists_open_doctrine_files():
    body = _client().get("/api/v1/doctrine").json()
    files = body["sources"]["open_doctrine_files"]
    assert "open-doctrine/README.md" in files
    assert "open-doctrine/11_NON_NEGOTIABLES.md" in files
    assert "open-doctrine/CONTROL_MAPPING.md" in files


def test_doctrine_endpoint_includes_control_mapping():
    body = _client().get("/api/v1/doctrine").json()
    mapping = body["control_mapping"]
    assert len(mapping) == 11
    numbers = sorted(row["number"] for row in mapping)
    assert numbers == list(range(1, 12))


def test_doctrine_endpoint_links_to_companion_endpoints():
    body = _client().get("/api/v1/doctrine").json()
    links = body["links"]
    assert links["promise_endpoint"] == "/api/v1/dealix-promise"
    assert links["capital_assets_public"] == "/api/v1/capital-assets/public"
    assert "verifier-report.json" in links["verifier_report"]


def test_doctrine_endpoint_has_disclaimer():
    body = _client().get("/api/v1/doctrine").json()
    assert "not legal advice" in body["disclaimer"]
