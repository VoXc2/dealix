"""Tests for AI Workforce policy primitives.

Covers:
  - apply_policy vetoes forbidden tool tokens.
  - apply_policy vetoes forbidden marketing tokens.
  - cost_guard.enforce_budget rejects over-limit runs.
  - task_router invariants (CompanyBrainAgent first, ComplianceGuardAgent last).
  - WorkforceGoal Pydantic schema rejects empty company_handle.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.main import create_app
from auto_client_acquisition.ai_workforce import (
    AgentTask,
    RiskLevel,
    WorkforceGoal,
    apply_policy,
    enforce_budget,
    estimate_cost,
    route_for_goal,
)


def _draft_task(agent_id: str = "SaudiCopyAgent", **overrides) -> AgentTask:
    base = dict(
        agent_id=agent_id,
        role_ar="ar",
        role_en="en",
        action_summary_ar="مسوّدة",
        action_summary_en="draft",
        output={"body_en": "safe content"},
        action_mode="draft_only",
        approval_status="approval_required",
        risk_level=RiskLevel.MEDIUM.value,
        cost_estimate_usd=0.5,
        evidence_pointers=[],
    )
    base.update(overrides)
    return AgentTask(**base)


def test_apply_policy_blocks_forbidden_tool_token():
    """A task whose output references a forbidden tool must be flipped to blocked."""
    task = _draft_task(output={"plan": "use cold_whatsapp now"})
    out = apply_policy(task)
    assert out.action_mode == "blocked"
    assert out.approval_status == "blocked"
    assert out.risk_level == RiskLevel.BLOCKED.value


def test_apply_policy_blocks_forbidden_marketing_token():
    """Forbidden marketing claims are vetoed too."""
    for token, field in [
        ("نضمن", {"action_summary_ar": "نضمن لكم النتيجة"}),
        ("guaranteed", {"action_summary_en": "we offer guaranteed results"}),
        ("blast", {"action_summary_en": "blast the list"}),
        ("scrape", {"action_summary_en": "we scrape the directory"}),
    ]:
        task = _draft_task(**field)
        out = apply_policy(task)
        assert out.action_mode == "blocked", f"{token!r} should have blocked the task"


def test_apply_policy_passes_clean_task():
    """A task with no forbidden tokens stays in draft_only."""
    task = _draft_task(output={"body_en": "Schedule a 30 min diagnostic call."})
    out = apply_policy(task)
    assert out.action_mode == "draft_only"
    assert out.approval_status == "approval_required"


def test_compliance_guard_exempt_from_tool_token_scan():
    """ComplianceGuardAgent legitimately surfaces the tool list as DATA."""
    task = _draft_task(
        agent_id="ComplianceGuardAgent",
        output={"vetoed_tools": ["cold_whatsapp", "send_email_live"]},
        action_mode="approval_required",
    )
    out = apply_policy(task)
    assert out.action_mode == "approval_required"


def test_enforce_budget_rejects_runs_over_5_usd():
    """Sum strictly above 5.0 USD must be rejected."""
    assert enforce_budget([1.0, 1.0, 1.0]) is True
    assert enforce_budget([2.5, 2.5]) is True  # equal to limit, allowed
    assert enforce_budget([3.0, 3.0]) is False
    assert enforce_budget([5.5]) is False


def test_estimate_cost_returns_agent_budget():
    """estimate_cost must return the agent's static budget."""
    cost = estimate_cost("CompanyBrainAgent")
    assert cost > 0
    assert cost < 5.0
    assert estimate_cost("UnknownAgent") == 0.0


def test_route_for_goal_starts_with_company_brain():
    """First two agents must be CompanyBrainAgent + MarketRadarAgent."""
    plan = route_for_goal(WorkforceGoal(company_handle="ACME"))
    assert plan[0] == "CompanyBrainAgent"
    assert plan[1] == "MarketRadarAgent"


def test_route_for_goal_ends_with_compliance_guard():
    """Last agent must always be ComplianceGuardAgent."""
    plan = route_for_goal(WorkforceGoal(company_handle="ACME"))
    assert plan[-1] == "ComplianceGuardAgent"


def test_workforce_goal_rejects_empty_company_handle_via_pydantic():
    """Direct schema construction with an empty company_handle must raise."""
    with pytest.raises(ValidationError):
        WorkforceGoal(company_handle="")


def test_workforce_goal_router_rejects_empty_company_handle_with_422():
    """API path must surface the same rejection as a 422."""
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/ai-workforce/run",
        json={"company_handle": ""},
    )
    assert resp.status_code == 422


def test_workforce_goal_extra_field_returns_422():
    """WorkforceGoal is extra='forbid'; rogue fields must 422."""
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/ai-workforce/run",
        json={"company_handle": "ACME", "rogue_field": "no"},
    )
    assert resp.status_code == 422
