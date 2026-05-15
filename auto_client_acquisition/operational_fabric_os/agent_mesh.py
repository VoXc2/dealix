"""System 27 — Agent mesh discovery, routing, and isolation."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class AgentDescriptor:
    agent_id: str
    capabilities: tuple[str, ...]
    trust_boundary: str
    governed: bool = True
    isolated: bool = False
    health_score: float = 1.0

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id_required")
        if not self.capabilities:
            raise ValueError("capabilities_required")
        if not self.trust_boundary.strip():
            raise ValueError("trust_boundary_required")
        if not 0.0 <= self.health_score <= 1.0:
            raise ValueError("health_score_out_of_range")


class AgentMesh:
    """Small in-memory mesh controller for deterministic policy checks."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentDescriptor] = {}

    def register(self, descriptor: AgentDescriptor) -> None:
        self._agents[descriptor.agent_id] = descriptor

    def discover(self, *, capability: str | None = None, include_isolated: bool = False) -> tuple[AgentDescriptor, ...]:
        cap = (capability or "").strip().lower()
        out: list[AgentDescriptor] = []
        for descriptor in self._agents.values():
            if descriptor.isolated and not include_isolated:
                continue
            if cap and cap not in {c.lower() for c in descriptor.capabilities}:
                continue
            out.append(descriptor)
        return tuple(sorted(out, key=lambda item: item.agent_id))

    def evaluate(self, agent_id: str, *, observability_score: float, policy_compliance: bool) -> float:
        descriptor = self._agents[agent_id]
        bounded_obs = max(0.0, min(1.0, observability_score))
        compliance_score = 1.0 if policy_compliance else 0.0
        health = round((bounded_obs * 0.7) + (compliance_score * 0.3), 3)
        self._agents[agent_id] = replace(descriptor, health_score=health)
        return health

    def isolate(self, agent_id: str) -> AgentDescriptor:
        descriptor = self._agents[agent_id]
        isolated = replace(descriptor, isolated=True)
        self._agents[agent_id] = isolated
        return isolated

    def route(self, capability: str) -> str | None:
        matches = [
            descriptor
            for descriptor in self._agents.values()
            if descriptor.governed
            and not descriptor.isolated
            and capability.lower() in {c.lower() for c in descriptor.capabilities}
        ]
        if not matches:
            return None
        best = sorted(matches, key=lambda item: (-item.health_score, item.agent_id))[0]
        return best.agent_id
