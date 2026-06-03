"""Founder Command Summary — API smoke + registry wiring."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.founder_command_summary import (
    clear_all_for_tests,
    merge_pipeline_stage,
)


@pytest.fixture(autouse=True)
def _clear_engagement_registry() -> None:
    clear_all_for_tests()
    yield
    clear_all_for_tests()


def test_founder_summary_routes_exist() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/founder-summary")
    assert r.status_code == 200
    body = r.json()
    assert body["governance_decision"] == "ALLOW"
    assert "brief" in body
    assert body["brief"]["questions"]["q1_top_revenue"]["en"]

    w = client.get("/api/v1/founder-summary/weekly/agenda")
    assert w.status_code == 200
    assert len(w.json()["agenda"]["sections"]) == 10


def test_per_engagement_not_found() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/founder-summary/e_unknown")
    assert r.status_code == 404


def test_per_engagement_with_snapshot() -> None:
    merge_pipeline_stage(
        "e_ri_demo",
        client_label="Demo Co",
        import_done=True,
        data_quality_score=72.0,
    )
    client = TestClient(app)
    r = client.get("/api/v1/founder-summary/e_ri_demo")
    assert r.status_code == 200
    data = r.json()
    assert data["blocker_category"] == "pipeline_stall"
    assert data["governance_decision"] in ("ALLOW", "ALLOW_WITH_REVIEW")
    assert data["snapshot"]["stages"]["import"] is True
