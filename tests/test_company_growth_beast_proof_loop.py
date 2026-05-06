"""Proof loop suggestions."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_proof_loop_requires_approval_for_snippets() -> None:
    c = TestClient(create_app())
    c.post(
        "/api/v1/company-growth-beast/profile",
        json={"session_id": "pf", "sector": "b2b", "offer": "خدمة", "consent_for_diagnostic": True},
    )
    c.post("/api/v1/company-growth-beast/diagnostic", json={"session_id": "pf"})
    c.post(
        "/api/v1/company-growth-beast/support-to-growth",
        json={"session_id": "pf", "support_questions": "pricing question"},
    )
    r = c.post("/api/v1/company-growth-beast/proof-loop", json={"session_id": "pf"})
    assert r.status_code == 200
    assert r.json()["no_fake_metrics"] is True
    ideas = r.json()["content_from_proof_ar"]
    assert all(i.get("approval_required") for i in ideas)
