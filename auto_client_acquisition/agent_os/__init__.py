"""Agent OS — identity + tool boundary contracts (governed Dealix)."""

from auto_client_acquisition.agent_os.agent_card import (
    AgentCard,
    AgentStatus,
    agent_card_valid,
    new_card,
)
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    lifecycle_allows_production_tools,
)
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    clear_for_test,
    get_agent,
    kill_agent,
    list_agents,
    register_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    is_tool_allowed,
    tool_allowed_mvp,
)

__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "AgentCard",
    "AgentLifecycleState",
    "AgentStatus",
    "AutonomyLevel",
    "agent_card_valid",
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "is_tool_allowed",
    "kill_agent",
    "lifecycle_allows_production_tools",
    "list_agents",
    "new_card",
    "register_agent",
    "tool_allowed_mvp",
]
