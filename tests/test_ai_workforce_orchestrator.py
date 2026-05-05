"""Tests for the AI Workforce orchestrator end-to-end pipeline.

Pure local composition — these tests verify the orchestrator wires
the registry + policy + risk_guard + cost_guard correctly without
ever calling an LLM or making an external request.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.ai_workforce import (
    WorkforceGoal,
    WorkforceRun,
    run_workforce_goal,
)
from auto_client_acquisition.company_brain_v6.service_matcher import (
    CUSTOMER_FACING_BUNDLES,
)


def _goal(**overrides) -> WorkforceGoal:
    base = dict(
        company_handle="ACME-SAUDI",
        company_context="B2B services in KSA, founder-led.",
        goal_ar="جذب عملاء جدد بدون أيّ إرسال آلي.",
        goal_en="Acquire new customers without automated sending.",
        desired_outcome="3 booked diagnostics next month",
        available_assets=["case_study_01", "founder_linkedin_post"],
        approved_channels=["warm_intro", "manual_email"],
        blocked_channels=[],
        budget_sar=2000.0,
        urgency="medium",
        language_preference="ar",
        founder_mode=True,
    )
    base.update(overrides)
    return WorkforceGoal(**base)


def test_run_workforce_goal_returns_populated_workforce_run():
    """Happy path: a valid goal must produce a fully populated WorkforceRun."""
    run = run_workforce_goal(_goal())
    assert isinstance(run, WorkforceRun)
    assert run.run_id.startswith("run_")
    assert run.summary_ar
    assert run.summary_en
    assert run.assigned_agents
    assert run.task_plan
    assert run.recommended_service
    assert run.next_best_action
    assert run.cost_estimate_usd >= 0
    assert run.guardrails


def test_task_plan_includes_every_assigned_agent():
    """No agent assigned by the router may be silently skipped."""
    run = run_workforce_goal(_goal())
    task_ids = [t.agent_id for t in run.task_plan]
    assert task_ids == run.assigned_agents
    assert len(task_ids) == len(set(task_ids)), "duplicate agent in task_plan"


def test_recommended_service_is_one_of_five_customer_bundles():
    """The recommended service must be one of the 5 customer-facing bundles."""
    run = run_workforce_goal(_goal())
    assert len(CUSTOMER_FACING_BUNDLES) == 5
    assert run.recommended_service in CUSTOMER_FACING_BUNDLES


def test_cost_estimate_is_non_negative():
    run = run_workforce_goal(_goal())
    assert run.cost_estimate_usd >= 0.0


def test_guardrails_has_all_five_canonical_keys_true():
    """All 5 canonical guardrail flags must be True on every run."""
    run = run_workforce_goal(_goal())
    expected_keys = {
        "no_live_send",
        "no_scraping",
        "no_cold_outreach",
        "approval_required_for_external_actions",
        "no_llm_calls",
    }
    assert expected_keys.issubset(run.guardrails.keys())
    for key in expected_keys:
        assert run.guardrails[key] is True, f"guardrail {key!r} not True"


def test_blocked_channels_does_not_break_legitimate_run():
    """A goal with cold_whatsapp on the BLOCKED list survives the run.

    ComplianceGuard blocks attempts to USE forbidden tools — not the
    legitimate act of listing them as blocked.
    """
    run = run_workforce_goal(_goal(blocked_channels=["cold_whatsapp"]))
    assert isinstance(run, WorkforceRun)
    # CompanyBrain ran successfully — the blocked channel was honored.
    brain_task = next(
        (t for t in run.task_plan if t.agent_id == "CompanyBrainAgent"),
        None,
    )
    assert brain_task is not None
    assert brain_task.action_mode != "blocked"


def test_compliance_guard_runs_last_in_task_plan():
    run = run_workforce_goal(_goal())
    assert run.task_plan[-1].agent_id == "ComplianceGuardAgent"


def test_router_run_endpoint_returns_full_workforce_run():
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/ai-workforce/run",
        json={
            "company_handle": "ACME-SAUDI",
            "goal_ar": "جذب عملاء جدد",
            "language_preference": "ar",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["run_id"].startswith("run_")
    assert body["recommended_service"] in CUSTOMER_FACING_BUNDLES
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["guardrails"]["no_live_send"] is True


def test_router_status_endpoint_reports_twelve_agents():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "ai_workforce"
    assert body["agents_registered"] == 12


def test_router_agents_listing_returns_all_twelve():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/agents")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 12
    assert len(body["agents"]) == 12


def test_router_agent_detail_returns_404_for_unknown():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/agents/NonExistentAgent")
    assert resp.status_code == 404


def test_router_agent_detail_returns_known_agent():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/agents/ComplianceGuardAgent")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_id"] == "ComplianceGuardAgent"
    assert body["autonomy_level"] == "approval_required"
