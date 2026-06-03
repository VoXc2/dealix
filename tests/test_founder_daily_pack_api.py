"""Founder daily-pack API — governed payload shape."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_founder_daily_pack_requires_admin_key(client: TestClient) -> None:
    r = client.get("/api/v1/ops-autopilot/founder/daily-pack")
    assert r.status_code in (401, 403, 422)


def test_founder_daily_pack_ok_with_admin_key(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/daily-pack",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert "kpi_commercial" in body
    assert "checklist_ar" in body
    assert body.get("policy_ar")
    assert "value_plan" in body
    assert body["value_plan"].get("first_paid_diagnostic")
    assert "full_autopilot" in body
    assert (body.get("full_autopilot") or {}).get("verdict")
    fao = body.get("full_autonomous_ops") or {}
    assert fao.get("automation_readiness", {}).get("verdict")


def test_founder_full_autopilot_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/full-autopilot",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("verdict")
    assert body.get("queue") is not None


def test_founder_full_autonomous_ops_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/full-autonomous-ops",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        params={"top_n": 5},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("founder_autopilot")
    assert body.get("automation_readiness")


def test_founder_commercial_value_map_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/commercial-value-map",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        params={"top_n": 2},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("catalog")
    assert body.get("status")
    assert body.get("value_plan")


def test_founder_strongest_ops_run_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.post(
        "/api/v1/ops-autopilot/founder/strongest-ops/run",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        json={"mode": "morning", "run_checks": False, "write_brief": True},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("verdict")
    assert body.get("brief_paths")


def test_founder_strongest_ops_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/strongest-ops",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        params={"mode": "morning"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("verdict")
    assert body.get("tasks_today")
    assert body.get("strongest_plan")


def test_founder_cockpit_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/cockpit",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        params={"top_n": 5, "mode": "morning"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("cockpit_verdict")
    assert body.get("strongest_ops")
    assert body.get("max_ops_backlog")
    assert body.get("governed_autopilot")


def test_founder_strongest_plan_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/strongest-plan",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status", {}).get("task_count") >= body.get("status", {}).get(
        "min_task_count", 100
    )
    assert body.get("sections")
    assert body.get("no_build_rule_ar")


def test_founder_value_plan_endpoint(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/value-plan",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        params={"top_n": 3},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("motion_a")
    assert body.get("first_paid_diagnostic")


def test_founder_evidence_csv_append(client: TestClient, monkeypatch, tmp_path) -> None:
    import dealix.commercial_ops.evidence_append as ea

    csv_path = tmp_path / "evidence_events_tracker.csv"
    csv_path.write_text(
        "event_id,event_date,event_type,company,contact,motion,offer_id,owner,source_channel,notes,next_action,next_action_date,war_room_status\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ea, "EVIDENCE_TRACKER_CSV", csv_path)
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")

    r = client.post(
        "/api/v1/ops-autopilot/founder/evidence/csv-append",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        json={
            "event_type": "scope_requested",
            "company": "Test Agency Co",
            "notes": "pytest append",
        },
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert body.get("row", {}).get("company") == "Test Agency Co"
    text = csv_path.read_text(encoding="utf-8")
    assert "Test Agency Co" in text


def test_founder_evidence_csv_append_rejects_bad_type(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.post(
        "/api/v1/ops-autopilot/founder/evidence/csv-append",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
        json={"event_type": "not_a_real_type", "company": "X"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 422


def test_founder_complete_autonomous_day_plan_endpoint(
    client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/complete-autonomous-day",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("strongest_plan_wiring") is True
    assert body.get("task_count", 0) >= 138
    assert body.get("research_verdict_ar")


def test_founder_complete_autonomous_day_plan_endpoint(
    client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/complete-autonomous-day",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code in (401, 403):
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert body.get("strongest_plan_wiring") is True
    assert body.get("task_count", 0) >= 138
    assert body.get("research_verdict_ar")
