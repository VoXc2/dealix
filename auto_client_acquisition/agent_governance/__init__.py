"""Agent Governance v5 — autonomy levels (L0-L5) + tool policy.

Thin extension over the existing ``SafeAgentRuntime`` at
``auto_client_acquisition/v3/agents.py``. Adds the NIST-style
"Govern / Map / Measure / Manage" framing the v5 spec asks for,
without rebuilding what the runtime already does.

Hard guarantees (each enforced by tests):

  - Default autonomy: L2_APPROVAL_REQUIRED.
  - L3+ requires ALLOWED_TOOLS to NOT contain any FORBIDDEN tool.
  - Forbidden tools: ``send_whatsapp_live``, ``linkedin_automation``,
    ``scrape_web``, ``charge_payment_live``, ``send_email_live``.
  - ``evaluate_action`` returns a typed verdict + the reason; never
    silently approves a forbidden combination.
"""
from auto_client_acquisition.agent_governance.schemas import (
    ActionEvaluation,
    AgentSpec,
    AutonomyLevel,
    ToolCategory,
    ToolPermission,
)
from auto_client_acquisition.agent_governance.agent_registry import (
    AGENT_REGISTRY,
    get_agent,
    list_agents,
)
from auto_client_acquisition.agent_governance.policy import (
    FORBIDDEN_TOOLS,
    evaluate_action,
    summary,
)

__all__ = [
    "ActionEvaluation",
    "AgentSpec",
    "AutonomyLevel",
    "ToolCategory",
    "ToolPermission",
    "AGENT_REGISTRY",
    "FORBIDDEN_TOOLS",
    "evaluate_action",
    "get_agent",
    "list_agents",
    "summary",
]
