"""Chain control — sub-agent chains must declare depth and owner."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentChainDeclaration:
    root_agent_id: str
    depth: int
    owner_principal: str


def chain_declaration_valid(d: AgentChainDeclaration) -> bool:
    if not (d.root_agent_id.strip() and d.owner_principal.strip()):
        return False
    return 0 < d.depth <= 5


__all__ = ["AgentChainDeclaration", "chain_declaration_valid"]
