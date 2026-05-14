"""Founder Command Center — Wave 18."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)
ADMIN_HEADER = "X-Admin-API-Key"


def test_command_center_admin_endpoint_requires_admin_key():
    resp = client.get("/api/v1/founder/command-center")
    assert resp.status_code in {401, 403}


def test_command_center_admin_endpoint_returns_full_aggregate(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_command_center_shape")
    resp = client.get(
        "/api/v1/founder/command-center",
        headers={ADMIN_HEADER: "test_command_center_shape"},
    )
    assert resp.status_code == 200
    body = resp.json()
    for field in (
        "generated_at",
        "deploy_health",
        "doctrine_health",
        "offer_ladder",
        "daily_routine",
        "anchor_partners",
        "arr_pacing",
        "capital_assets_this_week",
        "top_three_next_actions",
        "manifesto_endpoint",
        "commercial_map_endpoint",
        "post_deploy_check_endpoint",
        "governance_decision",
        "is_estimate",
    ):
        assert field in body, f"missing field: {field}"
    assert body["governance_decision"] == "allow"
    assert body["is_estimate"] is False
    assert isinstance(body["top_three_next_actions"], list)
    assert len(body["top_three_next_actions"]) == 3


def test_command_center_deploy_health_reports_all_canonical_modules_loadable(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_command_center_deploy")
    body = client.get(
        "/api/v1/founder/command-center",
        headers={ADMIN_HEADER: "test_command_center_deploy"},
    ).json()
    health = body["deploy_health"]
    assert health["checked"] >= 5
    assert health["all_green"] is True, f"unloadable modules: {health['failed']}"


def test_command_center_doctrine_health_eleven_commitments_all_enforced(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_command_center_doctrine")
    body = client.get(
        "/api/v1/founder/command-center",
        headers={ADMIN_HEADER: "test_command_center_doctrine"},
    ).json()
    doc = body["doctrine_health"]
    assert doc["commitments_count"] == 11
    assert doc["all_enforcers_exist"] is True, (
        f"missing enforcer files: {doc['missing_enforcers']}"
    )


def test_command_center_offer_ladder_reflects_2026_q2_reframe(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_command_center_offers")
    body = client.get(
        "/api/v1/founder/command-center",
        headers={ADMIN_HEADER: "test_command_center_offers"},
    ).json()
    ladder = body["offer_ladder"]
    assert ladder["offer_count"] == 3
    assert ladder["paid_floor_sar_per_month"] >= 4999.0
    assert ladder["flagship_sar_one_time"] >= 25000.0


def test_command_center_public_endpoint_no_admin_required():
    """Public view exposes only doctrine + offer count — no commercial-sensitive
    numbers — and reaches the reviewer/CISO without an admin key."""
    resp = client.get("/api/v1/founder/command-center/public")
    assert resp.status_code == 200
    body = resp.json()
    assert body["doctrine_health"]["commitments_count"] == 11
    assert body["offer_ladder"]["offer_count"] == 3
    # Public view MUST NOT leak commercial-sensitive fields
    assert "arr_pacing" not in body
    assert "anchor_partners" not in body
    assert "top_three_next_actions" not in body
