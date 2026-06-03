"""
Agent registry helpers.

The canonical agent data lives in ``core.safety.permissions.AGENT_REGISTRY``.
This module exposes convenience accessors and the schema (required fields)
that governance docs and tests rely on.
"""

from __future__ import annotations

from typing import Dict, List

from core.safety.permissions import AGENT_REGISTRY, PERMISSION_LEVELS, get_agent

# Fields every agent definition MUST carry (enforced by tests).
REQUIRED_AGENT_FIELDS = [
    "name",
    "mission",
    "input_files",
    "output_files",
    "allowed_actions",
    "forbidden_actions",
    "risk_level",
    "permission_level",
    "required_approval",
    "required_verification",
    "handoff_targets",
    "collision_rules",
]


def list_agents() -> List[Dict]:
    """All agent definitions, in registry order."""
    return list(AGENT_REGISTRY.values())


def agents_by_permission_level() -> Dict[str, List[str]]:
    """Map permission level -> agent names."""
    out: Dict[str, List[str]] = {lvl: [] for lvl in PERMISSION_LEVELS}
    for agent in AGENT_REGISTRY.values():
        out.setdefault(agent["permission_level"], []).append(agent["name"])
    return out


__all__ = [
    "AGENT_REGISTRY",
    "REQUIRED_AGENT_FIELDS",
    "PERMISSION_LEVELS",
    "list_agents",
    "get_agent",
    "agents_by_permission_level",
]
