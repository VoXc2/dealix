"""Validation that every agent template is bounded and governed.

Enforces ``no_unbounded_agents``: an agent template with no escalation
path, no risk class, or a forbidden tool in its allowed list is a
violation and must never be compiled to a runtime spec.
"""

from __future__ import annotations

from auto_client_acquisition.agent_factory.template_registry import list_templates
from auto_client_acquisition.agent_factory.template_schema import (
    ACTION_MODES,
    FORBIDDEN_TOOL_TOKENS,
    AgentTemplate,
)
from auto_client_acquisition.ai_workforce.schemas import RiskLevel


def validate_template(template: AgentTemplate) -> list[str]:
    """Return a list of doctrine violations for one template (empty = ok)."""
    violations: list[str] = []

    if not template.template_id:
        violations.append("template_id is empty")

    # no_unbounded_agents: every agent needs a human escalation path.
    if not template.escalation_rules:
        violations.append("escalation_rules is empty (no_unbounded_agents)")
    for rule in template.escalation_rules:
        if not rule.escalate_to:
            violations.append(f"escalation rule {rule.trigger!r} has no escalate_to")
        if rule.action_mode not in ACTION_MODES:
            violations.append(
                f"escalation rule {rule.trigger!r} action_mode {rule.action_mode!r} "
                "not in the 5 permitted action modes"
            )

    # risk_class must be an explicit, non-blocked level.
    if template.risk_class not in {RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH}:
        violations.append(f"risk_class {template.risk_class!r} is not a valid level")

    # cost budget must be a positive bound.
    if template.cost_budget_usd <= 0:
        violations.append("cost_budget_usd must be positive (bounded spend)")

    # tenant isolation: no cross-customer memory.
    if template.memory_policy.cross_customer:
        violations.append("memory_policy.cross_customer must be False")

    # no forbidden tool token may be live-callable.
    leaked = sorted(set(template.allowed_tools) & FORBIDDEN_TOOL_TOKENS)
    for tool in leaked:
        violations.append(f"allowed_tools contains forbidden token {tool!r}")

    # default action mode must be one of the 5 permitted.
    if template.default_action_mode not in ACTION_MODES:
        violations.append(
            f"default_action_mode {template.default_action_mode!r} "
            "not in the 5 permitted action modes"
        )

    return violations


def validate_all() -> dict[str, list[str]]:
    """Validate every registered template; map template_id to violations."""
    return {t.template_id: validate_template(t) for t in list_templates()}


def all_templates_valid() -> bool:
    """True when no registered template has any violation."""
    return all(not v for v in validate_all().values())
