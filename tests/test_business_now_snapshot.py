"""Business NOW snapshot API and builder."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from dealix.business_now.snapshot_builder import PILLAR_KEYS, build_business_now_snapshot

client = TestClient(app)


def test_builder_has_eight_pillars() -> None:
    snap = build_business_now_snapshot(run_verify=False)
    assert "pillars" in snap
    for key in PILLAR_KEYS:
        assert key in snap["pillars"]
    assert "gtm" in snap["pillars"]
    assert snap["pillars"]["gtm"]["leads_endpoint"]
    assert "today_actions" in snap
    assert len(snap["today_actions"]) >= 1


def test_api_business_now_snapshot() -> None:
    res = client.get("/api/v1/business-now/snapshot")
    assert res.status_code == 200
    body = res.json()
    assert body["pillars"]["commercial"]["commercial_kpi_pending"] >= 0
    assert isinstance(body["pillars"]["commercial"]["offers"], list)
    assert len(body["pillars"]["commercial"]["offers"]) >= 1
    platform = body["pillars"]["platform"]
    assert "enterprise_control_plane_verdict" in platform
    assert "verdict_source" in platform
    compliance = body["pillars"]["compliance"]
    assert "pdpl_module_present" in compliance
    finance = body["pillars"]["finance"]
    assert finance["moyasar_live_allowed"] is False


def test_operator_signals_requires_admin() -> None:
    res = client.get("/api/v1/business-now/operator-signals")
    assert res.status_code in (401, 403, 422)
