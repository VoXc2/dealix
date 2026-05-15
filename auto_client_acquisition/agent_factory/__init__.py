"""Agent Factory — design-time templates for governed AI agents.

Defines reusable agent templates with bounded escalation, risk classes,
and memory policies, validates them against doctrine, and compiles them
to the runtime ``AgentSpec`` consumed by ``ai_workforce``.
"""

from __future__ import annotations

from auto_client_acquisition.agent_factory.template_registry import (
    TEMPLATE_IDS,
    get_template,
    list_templates,
    to_agent_spec,
)
from auto_client_acquisition.agent_factory.template_schema import (
    ACTION_MODES,
    FORBIDDEN_TOOL_TOKENS,
    AgentTemplate,
    EscalationRule,
    MemoryPolicy,
)
from auto_client_acquisition.agent_factory.template_validation import (
    all_templates_valid,
    validate_all,
    validate_template,
)

__all__ = [
    "ACTION_MODES",
    "FORBIDDEN_TOOL_TOKENS",
    "TEMPLATE_IDS",
    "AgentTemplate",
    "EscalationRule",
    "MemoryPolicy",
    "all_templates_valid",
    "get_template",
    "list_templates",
    "to_agent_spec",
    "validate_all",
    "validate_template",
]
