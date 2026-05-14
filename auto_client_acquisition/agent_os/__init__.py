"""Canonical Agent OS — Wave 4 lite (14F).

Every AI agent in Dealix has an AgentCard with identity, owner,
autonomy_level, kill_switch_owner, allowed/forbidden tools, status. No
agent in production without a complete card.
"""
from auto_client_acquisition.agent_os.autonomy_levels import (
    AutonomyLevel,
    MVP_MAX_AUTONOMY,
    requires_per_session_approval,
)
from auto_client_acquisition.agent_os.agent_card import (
    AgentCard,
    AgentStatus,
    new_card,
)
from auto_client_acquisition.agent_os.agent_registry import (
    clear_for_test,
    get_agent,
    kill_agent,
    list_agents,
    register_agent,
    update_status,
)
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_MVP_TOOLS,
    FORBIDDEN_MVP_TOOLS,
    is_tool_allowed,
)

__all__ = [
    "ALLOWED_MVP_TOOLS",
    "AgentCard",
    "AgentStatus",
    "AutonomyLevel",
    "FORBIDDEN_MVP_TOOLS",
    "MVP_MAX_AUTONOMY",
    "clear_for_test",
    "get_agent",
    "is_tool_allowed",
    "kill_agent",
    "list_agents",
    "new_card",
    "register_agent",
    "requires_per_session_approval",
    "update_status",
]
