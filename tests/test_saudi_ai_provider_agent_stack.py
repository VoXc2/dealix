from __future__ import annotations

from saudi_ai_provider.agent_stack import (
    build_agent_application_plan,
    recommended_profile_for_service,
    render_agent_application_plan,
    render_segment_rollout_plan,
)


def test_recommended_profile_for_governance_service() -> None:
    profile = recommended_profile_for_service("AI_GOVERNANCE_OS")
    assert profile == "openclaw_runtime"


def test_build_agent_application_plan_has_guardrails() -> None:
    plan = build_agent_application_plan("AI_REVENUE_COMMAND_CENTER")
    assert plan.profile in {"hermes_agents", "openclaw_runtime", "hybrid_governed_execution"}
    assert "no_cold_whatsapp" in plan.guardrails
    assert len(plan.applications) >= 2


def test_render_agent_application_plan_arabic_title() -> None:
    text = render_agent_application_plan("AI_CUSTOMER_OPERATIONS_PLATFORM", lang="ar")
    assert "خطة تطبيق Hermes/OpenClaw" in text
    assert "AI_CUSTOMER_OPERATIONS_PLATFORM" in text


def test_render_segment_rollout_plan_includes_enterprise_services() -> None:
    text = render_segment_rollout_plan("enterprise", lang="en")
    assert "AI_GOVERNANCE_OS" in text
    assert "SOVEREIGN_AI_INFRASTRUCTURE" in text
