"""Agent OS — identity, lifecycle, and tool boundary contracts (governed Dealix)."""

from auto_client_acquisition.agent_os.agent_card import (
    AgentCard,
    AgentStatus,
    agent_card_valid,
)
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    lifecycle_allows_production_tools,
    new_card,
)
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    clear_for_test,
    get_agent,
    kill_agent,
    list_agents,
    register_agent,
    set_agent_status,
)
from auto_client_acquisition.agent_os.autonomy_levels import (
    KILL_SWITCH_REQUIRED_FROM,
    MAX_AUTONOMY_MVP,
    AutonomyLevel,
    autonomy_allowed_mvp,
    autonomy_requires_kill_switch,
)
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    is_tool_allowed,
    tool_allowed_mvp,
)

__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "KILL_SWITCH_REQUIRED_FROM",
    "MAX_AUTONOMY_MVP",
    "AgentCard",
    "AgentLifecycleState",
    "AgentStatus",
    "AutonomyLevel",
    "agent_card_valid",
    "autonomy_allowed_mvp",
    "autonomy_requires_kill_switch",
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "is_tool_allowed",
    "kill_agent",
    "lifecycle_allows_production_tools",
    "list_agents",
    "new_card",
    "register_agent",
    "set_agent_status",
    "tool_allowed_mvp",
]
