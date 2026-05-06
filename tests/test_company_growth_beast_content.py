"""Content pack."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_content_pack_draft_only() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "cp", "sector": "B2B", "offer": "تطوير برمجيات", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/offer", json={"session_id": "cp"})
    r = c.post("/api/v1/company-growth-beast/content-pack", json={"session_id": "cp"})
    assert r.status_code == 200
    assert r.json()["action_mode"] == "draft_only"
    assert "linkedin_post_draft_ar" in r.json()
    assert r.json()["approval_required"] is True
