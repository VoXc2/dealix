"""Experiment planner."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_experiment_returns_hypothesis() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "ex", "sector": "saas", "offer": "منصة", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/targets", json={"session_id": "ex"})
    c.post("/api/v1/company-growth-beast/offer", json={"session_id": "ex"})
    r = c.post("/api/v1/company-growth-beast/experiment", json={"session_id": "ex"})
    assert r.status_code == 200
    exp = r.json()["experiment"]
    assert exp["action_mode"] == "draft_only"
    assert "hypothesis" in exp
