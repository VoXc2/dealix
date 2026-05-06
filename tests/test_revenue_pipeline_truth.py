"""Revenue pipeline truth labels."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_revenue_pipeline_summary() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/revenue-pipeline/summary")
    assert r.status_code == 200
    data = r.json()
    assert "stages" in data
    assert "revenue_truth" in data
    assert "payment_received" in data["revenue_truth"]["revenue_requires"]
