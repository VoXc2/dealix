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


# ─── v6 additions ───────────────────────────────────────────────────


def test_founder_dashboard_first_3_customers_present(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    body = resp.json()
    assert "first_3_customers" in body
    section = body["first_3_customers"]
    if "_error" in section:
        pytest.fail(f"first_3_customers errored: {section}")
    # Three slots are surfaced from the placeholder board.
    assert isinstance(section.get("slots"), list)
    assert len(section["slots"]) == 3
    # Status counts are present and shaped per the loop board.
    assert "status_counts" in section
    # Real customer names must NOT leak — the doc only uses placeholders.
    for slot in section["slots"]:
        assert slot["slot"] in {"A", "B", "C"}
        # placeholder column always reads "Slot-A" / "Slot-B" / "Slot-C"
        assert slot["placeholder"].startswith("Slot-")


def test_founder_dashboard_pending_approvals_present(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    body = resp.json()
    assert "pending_approvals" in body
    section = body["pending_approvals"]
    if "_error" in section:
        pytest.fail(f"pending_approvals errored: {section}")
    assert "count" in section
    assert isinstance(section["count"], int)
    assert "first_3" in section
    assert isinstance(section["first_3"], list)
    # At most 3 cards regardless of queue depth.
    assert len(section["first_3"]) <= 3


def test_founder_dashboard_unsafe_blocks_present_with_min_5(
    client: TestClient,
) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    body = resp.json()
    assert "unsafe_blocks" in body
    section = body["unsafe_blocks"]
    if "_error" in section:
        pytest.fail(f"unsafe_blocks errored: {section}")
    assert section["count"] >= 5
    # Each known v6 forbidden tool appears in the surfaced names.
    expected = {
        "send_whatsapp_live",
        "linkedin_automation",
        "scrape_web",
        "charge_payment_live",
        "send_email_live",
    }
    assert expected.issubset(set(section["names"]))


def test_founder_dashboard_next_founder_action_present(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/dashboard")
    body = resp.json()
    assert "next_founder_action" in body
    action = body["next_founder_action"]
    # _safe could wrap into a dict on error — but the contract is:
    # either a non-empty string, or the literal "no_action_today".
    assert isinstance(action, str)
    assert action == "no_action_today" or action.strip() != ""
