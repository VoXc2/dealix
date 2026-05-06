"""Command center GET."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_command_center_full_flow_session() -> None:
    c = TestClient(create_app())
    sid = "cc1"
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": sid, "sector": "وكالة تسويق", "offer": "تصميم", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/diagnostic", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/targets", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/offer", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/content-pack", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/warm-route", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/experiment", json={"session_id": sid})
    c.post("/api/v1/company-growth-beast/support-to-growth", json={"session_id": sid, "support_questions": "help"})
    c.post("/api/v1/company-growth-beast/proof-loop", json={"session_id": sid})

    r = c.get("/api/v1/company-growth-beast/command-center", params={"session_id": sid})
    assert r.status_code == 200
    body = r.json()
    assert body["language_primary"] == "ar"
    assert len(body["next_best_actions"]) == 3
    assert "cold_whatsapp" in body["blocked_actions"]


def test_weekly_report() -> None:
    c = TestClient(create_app())
    sid = "wr1"
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": sid, "sector": "consulting", "offer": "ورش عمل", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/targets", json={"session_id": sid})
    r = c.get("/api/v1/company-growth-beast/weekly-report", params={"session_id": sid})
    assert r.status_code == 200
    rep = r.json()["weekly_growth_report"]
    assert len(rep["top_3_decisions"]) == 3
