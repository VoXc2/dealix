"""Agent access bindings — tool sets scoped to tenant."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentAccessBinding:
    agent_id: str
    tenant_id: str
    allowed_tools: frozenset[str]


def access_binding_valid(b: AgentAccessBinding) -> bool:
    return bool(b.agent_id.strip() and b.tenant_id.strip() and b.allowed_tools)


__all__ = ["AgentAccessBinding", "access_binding_valid"]
