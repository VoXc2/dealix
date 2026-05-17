"""Smoke + auth tests for the Ops Console domain (/api/v1/ops/*).

اختبارات غرفة التشغيل — التحقق من الوصول والاستجابة.

Covers all 8 surfaces: each returns 200 with an admin key, 403 without one,
and emits the doctrine `governance_decision` field.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app

ADMIN_KEY = "test-ops-admin-key"
HEADERS = {"X-Admin-API-Key": ADMIN_KEY}

GET_SURFACES = [
    "/api/v1/ops/command-center",
    "/api/v1/ops/catalog",
    "/api/v1/ops/market-proof",
    "/api/v1/ops/revenue",
    "/api/v1/ops/evidence",
    "/api/v1/ops/evidence/levels",
    "/api/v1/ops/billing",
    "/api/v1/ops/board",
    "/api/v1/ops/proof-pack/template",
]


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    return TestClient(app)


@pytest.mark.parametrize("path", GET_SURFACES)
def test_surface_returns_200_with_admin_key(client, path):
    resp = client.get(path, headers=HEADERS)
    assert resp.status_code == 200
    body = resp.json()
    assert body["governance_decision"] == "allow"
    assert "is_estimate" in body
    assert "generated_at" in body


@pytest.mark.parametrize("path", GET_SURFACES)
def test_surface_requires_admin_key(client, path):
    resp = client.get(path)  # no X-Admin-API-Key header
    assert resp.status_code == 403


def test_proof_pack_preview_returns_200(client):
    resp = client.post(
        "/api/v1/ops/proof-pack/preview",
        json={"company": "Acme Co", "sector": "b2b_services"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["governance_decision"] == "allow"
    assert "proof_pack" in body
    assert "diagnostic" in body
    assert "strength_band" in body


def test_proof_pack_preview_requires_admin_key(client):
    resp = client.post(
        "/api/v1/ops/proof-pack/preview",
        json={"company": "Acme Co"},
    )
    assert resp.status_code == 403


def test_proof_pack_preview_rejects_unknown_fields(client):
    resp = client.post(
        "/api/v1/ops/proof-pack/preview",
        json={"company": "Acme Co", "not_a_field": "x"},
        headers=HEADERS,
    )
    assert resp.status_code == 422


def test_catalog_returns_offer_ladder(client):
    body = client.get("/api/v1/ops/catalog", headers=HEADERS).json()
    assert body["offer_count"] >= 1
    assert isinstance(body["ladder"], list)
    assert body["ladder"][0]["rung"] == 1


def test_command_center_surfaces_top_actions(client):
    body = client.get("/api/v1/ops/command-center", headers=HEADERS).json()
    assert isinstance(body["top_3_actions"], list)
    assert 1 <= len(body["top_3_actions"]) <= 3
