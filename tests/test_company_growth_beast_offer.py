"""Offer matcher."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_offer_matches_agency_sector() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "of", "sector": "وكالة تسويق", "offer": "خدمات إبداعية", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/diagnostic", json={"session_id": "of"})
    r = c.post("/api/v1/company-growth-beast/offer", json={"session_id": "of"})
    assert r.status_code == 200
    off = r.json()["offer"]
    assert "إثبات" in off["offer_name_ar"] or "Proof" in off["offer_name_en"]
    assert "لا نضمن" in off["non_promise"] or "guarantee" in off["non_promise"].lower()
