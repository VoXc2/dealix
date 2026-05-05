"""Tests for ai_workforce_v10."""
from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta
from typing import get_args

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.ai_workforce_v10 import (
    PlannerOutput,
    ReviewerOutput,
    ReviewerVerdict,
    WorkforceMemoryEntry,
    list_memory,
    recall_memory,
    record_memory,
    reset_memory,
    run_planner,
    run_reviewer,
    run_workforce_v10,
)
from auto_client_acquisition.ai_workforce import WorkforceGoal


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture(autouse=True)
def _wipe_memory():
    reset_memory()
    yield
    reset_memory()


def test_reviewer_verdict_has_three_values():
    verdicts = set(get_args(ReviewerVerdict))
    assert verdicts == {"approved", "needs_revision", "blocked"}


def test_run_reviewer_clean_outputs_approves():
    out = run_reviewer([
        {"summary_en": "drafted bilingual outreach copy"},
        {"summary_en": "qualified the lead with 3 questions"},
    ])
    assert out.verdict == "approved"
    assert out.blocked_tokens == []


def test_run_reviewer_blocks_on_forbidden_token():
    out = run_reviewer([
        {"summary_en": "Guaranteed ROI promised to lead"},
    ])
    assert out.verdict == "blocked"
    assert "guaranteed roi" in out.blocked_tokens


def test_run_reviewer_blocks_on_scraping_marker():
    out = run_reviewer([
        {"summary_en": "We will scrape LinkedIn for prospects"},
    ])
    assert out.verdict == "blocked"
    assert "scrape linkedin" in out.blocked_tokens


def test_run_reviewer_empty_inputs_needs_revision():
    out = run_reviewer([])
    assert out.verdict == "needs_revision"


def test_run_planner_lead_intake_includes_company_brain_and_compliance():
    plan: PlannerOutput = run_planner("استقطاب عملاء", "lead intake", [])
    assert "CompanyBrainAgent" in plan.assigned_agents
    assert "ComplianceGuardAgent" in plan.assigned_agents


def test_run_planner_growth_includes_market_radar():
    plan = run_planner("نمو", "growth scaling", [])
    assert "MarketRadarAgent" in plan.assigned_agents
    assert "ComplianceGuardAgent" in plan.assigned_agents


def test_run_planner_always_includes_compliance_guard():
    plan = run_planner("any goal", "anything else", [])
    assert plan.assigned_agents[-1] == "ComplianceGuardAgent"


def test_memory_record_then_recall_returns_entry():
    record_memory(WorkforceMemoryEntry(
        customer_handle="ACME-SAUDI",
        key="last_diagnostic",
        value_redacted="diagnostic_complete",
    ))
    entries = recall_memory("ACME-SAUDI", "last_diagnostic")
    assert len(entries) == 1
    assert entries[0].value_redacted == "diagnostic_complete"


def test_memory_does_not_cross_customer_boundary():
    record_memory(WorkforceMemoryEntry(
        customer_handle="ACME-SAUDI", key="k", value_redacted="v",
    ))
    assert recall_memory("OTHER-CUSTOMER", "k") == []


def test_memory_expired_entries_not_returned():
    entry = WorkforceMemoryEntry(
        customer_handle="ACME-SAUDI",
        key="stale",
        value_redacted="x",
        ttl_hours=24,
    )
    # Backdate
    object.__setattr__(entry, "created_at", datetime.now(UTC) - timedelta(hours=2))
    record_memory(entry)
    # max_age_hours=0 → nothing fresh
    assert recall_memory("ACME-SAUDI", "stale", max_age_hours=0) == []


def test_memory_list_memory_returns_all_no_ttl_filter():
    record_memory(WorkforceMemoryEntry(
        customer_handle="X", key="a", value_redacted="1",
    ))
    record_memory(WorkforceMemoryEntry(
        customer_handle="X", key="b", value_redacted="2",
    ))
    assert len(list_memory("X")) == 2


def test_plan_endpoint_returns_200(client: TestClient):
    resp = client.post(
        "/api/v1/ai-workforce-v10/plan",
        json={"goal_ar": "نمو", "goal_en": "growth", "available_agents": []},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "ComplianceGuardAgent" in body["assigned_agents"]


def test_review_endpoint_returns_200(client: TestClient):
    resp = client.post(
        "/api/v1/ai-workforce-v10/review",
        json={"prior_outputs": [{"summary_en": "clean output"}]},
    )
    assert resp.status_code == 200
    assert resp.json()["verdict"] == "approved"


def test_run_endpoint_extends_workforce_run_with_planner_and_reviewer(client: TestClient):
    payload = {
        "company_handle": "ACME-SAUDI",
        "company_context": "B2B services in KSA",
        "goal_ar": "جذب عملاء",
        "goal_en": "lead intake",
        "desired_outcome": "3 diagnostics",
        "available_assets": [],
        "approved_channels": ["warm_intro"],
        "blocked_channels": [],
        "budget_sar": 1000.0,
        "urgency": "medium",
        "language_preference": "ar",
        "founder_mode": True,
    }
    resp = client.post("/api/v1/ai-workforce-v10/run", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "planner" in body
    assert "workforce_run" in body
    assert "reviewer" in body
    assert "guardrails" in body
    assert body["guardrails"]["memory_never_crosses_customers"] is True


def test_run_workforce_v10_direct_call_returns_envelope():
    goal = WorkforceGoal(
        company_handle="ACME-SAUDI", goal_ar="نمو", goal_en="growth",
    )
    out = run_workforce_v10(goal)
    assert "planner" in out
    assert "reviewer" in out
    assert "workforce_run" in out


def test_status_endpoint_advertises_canonical_guardrails(client: TestClient):
    resp = client.get("/api/v1/ai-workforce-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["guardrails"]["memory_never_crosses_customers"] is True
