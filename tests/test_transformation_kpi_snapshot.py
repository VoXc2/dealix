"""Transformation KPI snapshot API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_kpi_snapshot_returns_snapshots() -> None:
    res = client.get("/api/v1/transformation/kpi-snapshot")
    assert res.status_code == 200
    body = res.json()
    assert "snapshots" in body
    assert "commercial_registry" in body
    assert "reliability_posture_score" in body["snapshots"]
    assert body["commercial_registry"]["pending_count"] >= 0
