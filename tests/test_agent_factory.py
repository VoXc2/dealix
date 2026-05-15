"""Agent Factory — template registry, validation, AgentSpec compilation."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_factory import (
    AgentTemplate,
    EscalationRule,
    MemoryPolicy,
    all_templates_valid,
    get_template,
    list_templates,
    to_agent_spec,
    validate_all,
    validate_template,
)
from auto_client_acquisition.ai_workforce.schemas import AgentSpec, AutonomyLevel, RiskLevel

_EXPECTED = {
    "sales_agent",
    "support_agent",
    "ops_agent",
    "research_agent",
    "executive_agent",
    "governance_agent",
}


def test_six_templates_registered() -> None:
    templates = list_templates()
    assert len(templates) == 6
    assert {t.template_id for t in templates} == _EXPECTED


def test_get_template_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_template("nonexistent")


def test_every_template_has_bounded_escalation() -> None:
    for t in list_templates():
        assert t.escalation_rules, f"{t.template_id} has no escalation path"
        for rule in t.escalation_rules:
            assert rule.escalate_to


def test_every_template_has_risk_class() -> None:
    for t in list_templates():
        assert t.risk_class in {RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH}


def test_no_template_allows_cross_customer_memory() -> None:
    for t in list_templates():
        assert t.memory_policy.cross_customer is False


def test_all_registered_templates_valid() -> None:
    violations = validate_all()
    assert all(not v for v in violations.values()), violations
    assert all_templates_valid() is True


def test_validate_template_flags_missing_escalation() -> None:
    bad = AgentTemplate(
        template_id="bad_agent",
        role_en="Bad",
        role_ar="سيئ",
        goals=("x",),
        allowed_tools=(),
        forbidden_tools=(),
        permissions=("viewer",),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=MemoryPolicy(False, False, False, 1),
        escalation_rules=(),
        eval_metrics=(),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.1,
    )
    violations = validate_template(bad)
    assert any("escalation_rules is empty" in v for v in violations)


def test_validate_template_flags_forbidden_tool_leak() -> None:
    bad = AgentTemplate(
        template_id="leaky_agent",
        role_en="Leaky",
        role_ar="مسرّب",
        goals=("x",),
        allowed_tools=("cold_whatsapp",),
        forbidden_tools=(),
        permissions=("viewer",),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=MemoryPolicy(False, False, False, 1),
        escalation_rules=(EscalationRule("t", "sales_manager", "approval_required"),),
        eval_metrics=(),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.1,
    )
    violations = validate_template(bad)
    assert any("forbidden token" in v for v in violations)


def test_validate_template_flags_cross_customer_memory() -> None:
    bad = AgentTemplate(
        template_id="memory_agent",
        role_en="Memory",
        role_ar="ذاكرة",
        goals=("x",),
        allowed_tools=(),
        forbidden_tools=(),
        permissions=("viewer",),
        autonomy_level=AutonomyLevel.DRAFT_ONLY,
        memory_policy=MemoryPolicy(True, True, True, 1),
        escalation_rules=(EscalationRule("t", "sales_manager", "approval_required"),),
        eval_metrics=(),
        risk_class=RiskLevel.LOW,
        cost_budget_usd=0.1,
    )
    violations = validate_template(bad)
    assert any("cross_customer" in v for v in violations)


def test_to_agent_spec_compiles_valid_spec() -> None:
    template = get_template("sales_agent")
    spec = to_agent_spec(template, agent_id="SalesAgentRun1")
    assert isinstance(spec, AgentSpec)
    assert spec.agent_id == "SalesAgentRun1"
    assert spec.requires_approval is True
    assert "cold_whatsapp" not in spec.allowed_tools


def test_to_agent_spec_requires_agent_id() -> None:
    with pytest.raises(ValueError):
        to_agent_spec(get_template("ops_agent"), agent_id="")
