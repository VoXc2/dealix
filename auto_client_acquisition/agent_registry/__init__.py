"""Agent Registry — doctrine #9: no AI agent without owner + scope + audit.

Public API:
    from auto_client_acquisition.agent_registry import (
        AgentSpec,
        register, get, list_agents, verify,
        seed_default_agents, get_default_registry,
    )
"""
from __future__ import annotations

from auto_client_acquisition.agent_registry.registry import (
    SEED_AGENT_NAMES,
    AgentRegistryError,
    get,
    get_default_registry,
    list_agents,
    register,
    reset_default_registry,
    seed_default_agents,
    verify,
)
from auto_client_acquisition.agent_registry.registry_postgres import (
    PostgresAgentRegistry,
)
from auto_client_acquisition.agent_registry.schemas import AgentSpec, RiskClass

__all__ = [
    "AgentRegistryError",
    "AgentSpec",
    "PostgresAgentRegistry",
    "RiskClass",
    "SEED_AGENT_NAMES",
    "get",
    "get_default_registry",
    "list_agents",
    "register",
    "reset_default_registry",
    "seed_default_agents",
    "verify",
]
