"""Diagnostic endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_diagnostic_requires_profile() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/company-growth-beast/diagnostic", json={"session_id": "nope"})
    assert r.status_code == 200
    assert r.json().get("error") == "missing_profile"


def test_diagnostic_after_profile() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "d1", "sector": "استشارات", "offer": "برامج تدريب", "consent_for_diagnostic": True},
    )
    r = c.post("/api/v1/company-growth-beast/diagnostic", json={"session_id": "d1"})
    assert r.status_code == 200
    d = r.json()["diagnostic"]
    assert d["action_mode"] == "draft_only"
    assert "seven_day_outline_ar" in d
    assert d["language_primary"] == "ar"
