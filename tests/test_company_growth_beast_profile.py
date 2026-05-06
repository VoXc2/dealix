"""Company Growth Beast — profile."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_profile_200_and_saves_session() -> None:
    c = TestClient(create_app())
    body = {
        "session_id": "t1",
        "sector": "وكالة تسويق",
        "offer": "تقارير أداء لعملاء الوكالة",
        "ideal_customer": "شركات لديها 10–50 موظف",
        "consent_for_diagnostic": True,
    }
    r = c.post("/api/v1/company-growth-beast/profile", json=body)
    assert r.status_code == 200
    data = r.json()
    assert data["session_id"] == "t1"
    assert data["profile"]["sector"] == "وكالة تسويق"
    assert data["action_mode"] == "draft_only"


def test_profile_blocked_on_unsafe_phrase() -> None:
    c = TestClient(create_app())
    r = c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "bad", "sector": "x", "offer": "we enable auto_send for you", "consent_for_diagnostic": True},
    )
    assert r.status_code == 200
    assert r.json()["safety"]["safe"] is False
    assert r.json()["action_mode"] == "blocked"
