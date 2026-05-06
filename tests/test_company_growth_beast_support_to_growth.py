"""Support themes → growth (no PII)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.company_growth_beast.session_store import reset_all


def setup_function() -> None:
    reset_all()


def test_support_redacts_email() -> None:
    c = TestClient(create_app())
    r = c.post(
        "/api/v1/company-growth-beast/support-to-growth",
        json={"session_id": "s1", "support_questions": "Refund please contact me@x.com +966501234567"},
    )
    assert r.status_code == 200
    assert r.json()["action_mode"] == "suggest_only"
    themes = r.json()["themes"]
    assert "refund_policy_clarity" in themes


def test_support_privacy_theme() -> None:
    c = TestClient(create_app())
    r = c.post(
        "/api/v1/company-growth-beast/support-to-growth",
        json={"session_id": "s2", "support_questions": "PDPL data deletion request"},
    )
    assert "privacy_and_consent" in r.json()["themes"]
