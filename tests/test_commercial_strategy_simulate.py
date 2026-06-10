"""Commercial strategy simulate endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from dealix.business_now.commercial_strategy import build_commercial_strategy_snapshot

client = TestClient(app)


def test_simulate_invalid_budget_returns_422() -> None:
    res = client.post(
        "/api/v1/business-now/commercial-strategy/simulate",
        json={"monthly_budget_sar": "not-a-number"},
    )
    assert res.status_code == 422


def test_simulate_endpoint() -> None:
    res = client.post(
        "/api/v1/business-now/commercial-strategy/simulate",
        json={"industry": "clinics", "city": "Riyadh", "monthly_budget_sar": 3000},
    )
    assert res.status_code == 200
    body = res.json()
    assert body.get("is_estimate") is True
    assert "vertical" in body
    assert "plan_recommendation" in body
    assert "pipeline_sar" not in str(body).lower() or "influenced" in str(body).lower()


def test_snapshot_has_max_fields() -> None:
    snap = build_commercial_strategy_snapshot(
        commercial_kpi_pending=0,
        transformation_verdict="PASS",
        all_pilots_template_ready=False,
    )
    assert "next_best_actions" in snap
    assert len(snap["next_best_actions"]) >= 3
    assert snap["quality_scores_demo"]["is_estimate"] is True
    assert "gtm_first_10_summary" in snap
    assert "sales_playbook" in snap
