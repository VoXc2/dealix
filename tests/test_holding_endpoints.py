"""Tests for /api/v1/holding/* and /api/v1/business-units/* — shape + safety."""
from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.business_units import router as bu_router
from api.routers.holding import router as holding_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(holding_router)
    app.include_router(bu_router)
    return TestClient(app)


def test_charter_returns_pinned_sha_and_principles():
    body = _client().get("/api/v1/holding/charter").json()
    assert body["name"] == "Dealix Group"
    assert "commit_sha" in body
    # 40-char sha or fallback.
    assert body["commit_sha"] == "unknown" or len(body["commit_sha"]) == 40
    assert "Cash now." in body["operating_principles"]
    assert "Proof always." in body["operating_principles"]
    assert "Governance by default." in body["operating_principles"]
    assert "Productize repetition." in body["operating_principles"]
    assert len(body["holding_non_negotiables"]) == 4


def test_portfolio_returns_safe_aggregate():
    body = _client().get("/api/v1/holding/portfolio").json()
    assert body["name"] == "Dealix Group"
    assert isinstance(body["count"], int)
    assert isinstance(body["by_status"], dict)
    assert isinstance(body["by_sector"], dict)
    assert isinstance(body["recent_units"], list)


def test_portfolio_recent_units_have_only_safe_fields():
    body = _client().get("/api/v1/holding/portfolio").json()
    for u in body["recent_units"]:
        assert set(u.keys()) <= {"slug", "name", "status"}, (
            f"recent_units leaked extra fields: {u.keys()}"
        )


def test_portfolio_never_includes_owner_or_kpi(tmp_path, monkeypatch):
    """Even when registry has owner+kpi+reason, public portfolio strips them."""
    registry = tmp_path / "bu.json"
    registry.write_text(json.dumps({
        "entries": [{
            "slug": "x", "name": "X BU", "status": "BUILD",
            "owner": "owner@private.com",
            "kpi": "secret KPI ratio",
            "sector": "fintech",
            "reason": "private rationale",
        }],
    }))
    monkeypatch.setattr("api.routers.holding.BU_REGISTRY", registry)
    body = _client().get("/api/v1/holding/portfolio").json()
    body_text = json.dumps(body)
    assert "owner@private.com" not in body_text
    assert "secret KPI ratio" not in body_text
    assert "private rationale" not in body_text


def test_board_returns_public_shape_with_no_pii():
    body = _client().get("/api/v1/holding/board").json()
    assert body["name"] == "Dealix Group Board"
    assert isinstance(body["members"], list)
    for m in body["members"]:
        # Only name + role + independence; no contact fields.
        assert set(m.keys()) <= {"name", "role", "independent"}


def test_bu_public_returns_safe_fields_only():
    r = _client().get("/api/v1/business-units/core-os/public")
    assert r.status_code == 200
    body = r.json()
    allowed_top = {"slug", "name", "status", "doctrine_version", "charter_path", "as_of", "links"}
    assert set(body.keys()) <= allowed_top
    # Must not leak owner / kpi / git_author / entry_id / created_at / reason.
    forbidden = ("owner", "kpi", "git_author", "entry_id", "created_at", "reason")
    body_text = json.dumps(body)
    for bad in forbidden:
        assert f'"{bad}":' not in body_text, f"public BU leaked: {bad}"


def test_bu_public_returns_404_for_unknown():
    r = _client().get("/api/v1/business-units/does-not-exist/public")
    assert r.status_code == 404


def test_bu_admin_returns_full_entry():
    r = _client().get("/api/v1/business-units/core-os")
    assert r.status_code == 200
    body = r.json()
    # Full view includes provenance fields.
    for key in ("entry_id", "git_author", "created_at"):
        assert key in body


def test_holding_portfolio_no_email_or_phone_patterns(tmp_path, monkeypatch):
    registry = tmp_path / "bu.json"
    registry.write_text(json.dumps({
        "entries": [{
            "slug": "x", "name": "X BU", "status": "BUILD",
            "owner": "founder@dealix.sa", "kpi": "k",
            "sector": "logistics",
            "phone": "+966500000000",
        }],
    }))
    monkeypatch.setattr("api.routers.holding.BU_REGISTRY", registry)
    text = _client().get("/api/v1/holding/portfolio").text
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    assert not re.search(r"\+?966\d{8,9}", text)
