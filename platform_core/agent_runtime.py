"""Agent runtime facade — identity card, registry, and lifecycle.

No agent enters the registry without a valid card (identity + owner +
autonomy_level). The registry is an in-memory module-global; tests reset
it via ``clear_agent_registry_for_tests``.
"""

from __future__ import annotations

from auto_client_acquisition.agent_os.agent_card import AgentCard, agent_card_valid
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    lifecycle_allows_production_tools,
)
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    get_agent,
    list_agents,
    register_agent,
)

__all__ = [
    "AgentCard",
    "AgentLifecycleState",
    "agent_card_valid",
    "clear_agent_registry_for_tests",
    "get_agent",
    "lifecycle_allows_production_tools",
    "list_agents",
    "register_agent",
]
