"""Target segments ranking."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_targets_rank_agency_high() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "tg", "sector": "وكالة تسويق", "offer": "إدارة حملات", "consent_for_diagnostic": True},
    )
    r = c.post("/api/v1/company-growth-beast/targets", json={"session_id": "tg"})
    assert r.status_code == 200
    targets = r.json()["targets"]
    assert len(targets) >= 2
    assert targets[0]["segment_name_ar"]
    assert targets[0]["action_mode"] == "draft_only"
