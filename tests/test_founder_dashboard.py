"""Tests for /api/v1/founder/dashboard — aggregate read-only snapshot.

Hard guarantees:
  - Always returns 200 (never 5xx) — even if a single layer probe fails.
  - No live-action gate ever reports 'ALLOWED' on a clean checkout.
  - All 6 expected sections present in the payload.
  - Bilingual title fields populated.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_founder_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "founder"
    assert body["guardrails"]["no_live_send"] is True
    assert body["guardrails"]["no_scraping"] is True
    assert "/dashboard" in body["endpoints"]


def test_founder_dashboard_returns_200_with_required_sections(
    client: TestClient,
) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    assert resp.status_code == 200
    body = resp.json()

    required = {
        "schema_version",
        "generated_at",
        "title_ar",
        "title_en",
        "services",
        "reliability",
        "live_gates",
        "daily_loop",
        "weekly_scorecard",
        "ceo_brief",
        "guardrails",
    }
    missing = required - set(body.keys())
    assert not missing, f"missing keys in dashboard: {missing}"

    # Bilingual titles must be non-empty
    assert body["title_ar"]
    assert body["title_en"]
    assert "Dealix" in body["title_en"]


def test_founder_dashboard_live_gates_all_blocked(client: TestClient) -> None:
    """Hard rule: a clean production deploy reports BLOCKED on every
    live-action gate. ALLOWED would mean misconfiguration — fail loud.
    """
    resp = client.get("/api/v1/founder/dashboard")
    assert resp.status_code == 200
    gates = resp.json()["live_gates"]

    expected = {
        "live_charge",
        "whatsapp_live_send",
        "email_live_send",
        "linkedin_and_scraping",
    }
    missing = expected - set(gates.keys())
    assert not missing, f"missing gates: {missing}"

    for name, status in gates.items():
        assert "ALLOWED" not in status, (
            f"gate {name} reports ALLOWED on test client: {status!r}"
        )


def test_founder_dashboard_services_counts_present(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    services = resp.json()["services"]
    if "_error" in services:
        pytest.fail(f"services section errored: {services}")
    # As of v5 close, the matrix has 32 services
    assert services.get("total") == 32


def test_founder_dashboard_reliability_overall_present(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    rel = resp.json()["reliability"]
    if "_error" in rel:
        pytest.fail(f"reliability section errored: {rel}")
    assert "overall_status" in rel
    assert "subsystems" in rel
    # 9 subsystems exist in the v5 matrix
    assert len(rel["subsystems"]) == 9


def test_founder_dashboard_guardrails_re_asserted(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    g = resp.json()["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True
    assert g["approval_required_for_external_actions"] is True
