"""Tests for the AI Workforce orchestrator end-to-end pipeline.

Pure local composition — these tests verify the orchestrator wires
registry + canonical delegation + policy + risk/cost guards correctly without
calling an LLM or making an external request.

The historical 12 specialist roles remain compatibility workloads under the
five canonical Dealix agents. They do not create a second permanent fleet and
may not resurrect retired fixed-price customer bundles as commercial authority.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.ai_workforce import (
    WorkforceGoal,
    WorkforceRun,
    run_workforce_goal,
)
from auto_client_acquisition.ai_workforce.orchestrator import CANONICAL_ENTRY_OFFER


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
    """No specialist role assigned by the router may be silently skipped."""
    run = run_workforce_goal(_goal())
    task_ids = [t.agent_id for t in run.task_plan]
    assert task_ids == run.assigned_agents
    assert len(task_ids) == len(set(task_ids)), "duplicate specialist role in task_plan"


def test_recommended_service_is_current_canonical_entry_offer():
    """Legacy workforce cannot restore historical bundle/pricing authority."""
    run = run_workforce_goal(_goal())
    assert CANONICAL_ENTRY_OFFER == "free_mini_diagnostic"
    assert run.recommended_service == CANONICAL_ENTRY_OFFER
    assert run.guardrails["no_autonomous_pricing"] is True
    assert run.guardrails["no_autonomous_payment"] is True


def test_cost_estimate_is_non_negative():
    run = run_workforce_goal(_goal())
    assert run.cost_estimate_usd >= 0.0


def test_guardrails_has_all_five_canonical_keys_true():
    """Every run keeps the core fail-closed safety contract."""
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
    assert body["recommended_service"] == CANONICAL_ENTRY_OFFER
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["guardrails"]["no_live_send"] is True
    assert body["guardrails"]["no_autonomous_pricing"] is True
    assert body["guardrails"]["no_autonomous_payment"] is True


def test_router_status_endpoint_reports_twelve_specialist_roles():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "ai_workforce"
    assert body["agents_registered"] == 12


def test_router_agents_listing_returns_all_twelve_specialist_roles():
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


def test_router_agent_detail_returns_known_specialist_role():
    client = TestClient(create_app())
    resp = client.get("/api/v1/ai-workforce/agents/ComplianceGuardAgent")
    assert resp.status_code == 200
    body = resp.json()
    assert body["agent_id"] == "ComplianceGuardAgent"
    assert body["autonomy_level"] == "approval_required"
