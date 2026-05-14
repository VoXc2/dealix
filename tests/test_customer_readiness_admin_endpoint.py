"""Admin (full) readiness endpoint tests."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.customer_readiness_gate import router as readiness_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(readiness_router)
    return TestClient(app)


def test_admin_endpoint_returns_full_breakdown():
    r = _client().get("/api/v1/customer/demo-proceed/readiness")
    assert r.status_code == 200
    body = r.json()
    required_keys = {
        "handle",
        "source_passport_status",
        "governance_decisions_7d",
        "proof_pack_count",
        "capital_asset_count",
        "has_signed_scope",
        "recommendation",
        "rationale",
    }
    assert required_keys.issubset(body.keys())
    assert body["handle"] == "demo-proceed"
    assert body["recommendation"] == "PROCEED"


def test_admin_endpoint_with_hold_for_scope():
    body = _client().get("/api/v1/customer/demo-hold-scope/readiness").json()
    assert body["recommendation"] == "HOLD_FOR_SCOPE"
    assert body["has_signed_scope"] is False


def test_admin_endpoint_with_hold_for_governance():
    body = _client().get("/api/v1/customer/demo-hold-governance/readiness").json()
    assert body["recommendation"] == "HOLD_FOR_GOVERNANCE"
    assert "source_passport_not_present" in body["rationale"]


def test_admin_endpoint_unknown_handle_defaults_to_governance_hold():
    body = _client().get("/api/v1/customer/some-unknown/readiness").json()
    assert body["recommendation"] == "HOLD_FOR_GOVERNANCE"
    assert body["source_passport_status"] == "unknown"
