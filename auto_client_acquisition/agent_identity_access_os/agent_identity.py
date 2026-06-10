"""Agent identity record (IAM layer — separate from runtime card)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentIdentity:
    agent_id: str
    tenant_id: str
    owner_principal: str


def agent_identity_valid(i: AgentIdentity) -> bool:
    return all((i.agent_id.strip(), i.tenant_id.strip(), i.owner_principal.strip()))


__all__ = ["AgentIdentity", "agent_identity_valid"]
