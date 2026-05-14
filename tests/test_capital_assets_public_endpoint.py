"""Tests for /api/v1/capital-assets/public — shape and safety."""
from __future__ import annotations

import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.capital_assets import (
    CAPITAL_ASSET_INDEX,
    router as capital_assets_router,
)


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(capital_assets_router)
    return TestClient(app)


def test_capital_assets_public_returns_200():
    r = _client().get("/api/v1/capital-assets/public")
    assert r.status_code == 200


def test_capital_assets_public_shape():
    body = _client().get("/api/v1/capital-assets/public").json()
    assert "count" in body
    assert "by_type" in body
    assert "recent_titles_safe" in body
    assert "generated_at" in body
    assert "source" in body
    assert "disclaimer" in body


def test_capital_assets_public_handles_missing_index_file(tmp_path, monkeypatch):
    """If the index file doesn't exist, endpoint returns count 0, not 500."""
    missing = tmp_path / "absent.json"
    monkeypatch.setattr(
        "api.routers.capital_assets.CAPITAL_ASSET_INDEX", missing
    )
    body = _client().get("/api/v1/capital-assets/public").json()
    assert body["count"] == 0
    assert body["by_type"] == {}
    assert body["recent_titles_safe"] == []


def test_capital_assets_public_counts_by_type(tmp_path, monkeypatch):
    """Counts are grouped by CapitalAssetType."""
    index = tmp_path / "idx.json"
    index.write_text(json.dumps({
        "entries": [
            {"asset_type": "proof_example", "title": "A"},
            {"asset_type": "proof_example", "title": "B"},
            {"asset_type": "scoring_rule", "title": "C"},
            {"asset_type": "invalid_type", "title": "D"},  # ignored
        ]
    }))
    monkeypatch.setattr("api.routers.capital_assets.CAPITAL_ASSET_INDEX", index)
    body = _client().get("/api/v1/capital-assets/public").json()
    assert body["count"] == 3
    assert body["by_type"]["proof_example"] == 2
    assert body["by_type"]["scoring_rule"] == 1
    assert "invalid_type" not in body["by_type"]


def test_capital_assets_public_recent_is_truncated_to_10(tmp_path, monkeypatch):
    index = tmp_path / "idx.json"
    index.write_text(json.dumps({
        "entries": [
            {"asset_type": "proof_example", "title": f"T{i}"} for i in range(25)
        ]
    }))
    monkeypatch.setattr("api.routers.capital_assets.CAPITAL_ASSET_INDEX", index)
    body = _client().get("/api/v1/capital-assets/public").json()
    assert len(body["recent_titles_safe"]) == 10
    # And it's the LAST 10.
    last_titles = [r["title_safe"] for r in body["recent_titles_safe"]]
    assert last_titles == [f"T{i}" for i in range(15, 25)]
