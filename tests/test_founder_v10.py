"""Tests for founder_v10 — composed daily brief."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.founder_v10 import (
    DailyBrief,
    build_daily_brief,
    compute_next_action,
    find_blockers,
    summarize_cost,
    summarize_evidence,
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_build_daily_brief_returns_bilingual_payload():
    brief = build_daily_brief()
    assert isinstance(brief, DailyBrief)
    assert brief.summary_ar
    assert brief.summary_en
    assert isinstance(brief.top_3_decisions, list)
    assert isinstance(brief.cost_summary_usd, float)
    assert isinstance(brief.evidence_summary, dict)


def test_find_blockers_returns_list():
    blockers = find_blockers()
    assert isinstance(blockers, list)
    # On a clean state, may be empty — both shapes are acceptable.
    for b in blockers:
        assert b.id
        assert b.severity in {"low", "medium", "high", "blocked"}


def test_summarize_evidence_returns_counts_no_pii():
    payload = summarize_evidence()
    assert isinstance(payload, dict)
    assert "total" in payload
    assert "by_type" in payload
    assert "by_month" in payload
    # Defensive: there must NEVER be a raw "events" or "customer_handle"
    # field — counts only.
    assert "events" not in payload
    assert "customer_handle" not in payload


def test_compute_next_action_returns_bilingual_dict():
    action = compute_next_action()
    assert isinstance(action, dict)
    assert "next_action_ar" in action
    assert "next_action_en" in action
    assert action["next_action_ar"]
    assert action["next_action_en"]


def test_summarize_cost_defaults_to_zero_when_module_absent():
    payload = summarize_cost(period_days=7)
    assert isinstance(payload, dict)
    assert payload["period_days"] == 7
    assert "total_usd" in payload
    assert payload["total_usd"] >= 0.0


def test_today_endpoint_returns_200(client: TestClient):
    resp = client.get("/api/v1/founder-v10/today")
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary_ar"]
    assert body["summary_en"]
    assert "top_3_decisions" in body
    assert "blockers" in body


def test_status_endpoint_advertises_canonical_guardrails(client: TestClient):
    resp = client.get("/api/v1/founder-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "founder_v10"
    assert body["guardrails"]["no_live_send"] is True
    assert body["guardrails"]["no_scraping"] is True
    assert body["guardrails"]["no_pii_in_brief"] is True


def test_blockers_endpoint_returns_list(client: TestClient):
    resp = client.get("/api/v1/founder-v10/blockers")
    assert resp.status_code == 200
    body = resp.json()
    assert "count" in body
    assert isinstance(body["items"], list)


def test_evidence_endpoint_returns_counts(client: TestClient):
    resp = client.get("/api/v1/founder-v10/evidence")
    assert resp.status_code == 200
    body = resp.json()
    assert "total" in body


def test_cost_endpoint_respects_days_param(client: TestClient):
    resp = client.get("/api/v1/founder-v10/cost?days=14")
    assert resp.status_code == 200
    assert resp.json()["period_days"] == 14


def test_next_action_endpoint_returns_bilingual(client: TestClient):
    resp = client.get("/api/v1/founder-v10/next-action")
    assert resp.status_code == 200
    body = resp.json()
    assert body["next_action_ar"]
    assert body["next_action_en"]
