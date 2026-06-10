"""Tenant-scoped registry and routing for agent mesh control."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class AgentDescriptor:
    agent_id: str
    tenant_id: str
    name: str
    owner: str
    capabilities: tuple[str, ...]
    trust_tier: str
    status: str
    autonomy_level: int
    endpoint: str | None = None
    composite_score: float | None = None
    tool_permissions: tuple[str, ...] = ()
    registered_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class TrustBoundary:
    boundary_id: str
    tenant_id: str
    scope: str
    max_autonomy_level: int
    requires_human_for_external: bool = True


class InMemoryAgentMeshRepository:
    def __init__(self) -> None:
        self._agents: dict[str, dict[str, AgentDescriptor]] = {}
        self._boundaries: dict[str, TrustBoundary] = {}

    def register_agent(self, descriptor: AgentDescriptor) -> AgentDescriptor:
        tid = resolve_tenant_id(descriptor.tenant_id)
        self._agents.setdefault(tid, {})[descriptor.agent_id] = replace(descriptor, tenant_id=tid)
        return self._agents[tid][descriptor.agent_id]

    def set_trust_boundary(self, boundary: TrustBoundary) -> TrustBoundary:
        tid = resolve_tenant_id(boundary.tenant_id)
        self._boundaries[tid] = replace(boundary, tenant_id=tid)
        return self._boundaries[tid]

    def route_agent(self, *, tenant_id: str | None, capability: str) -> AgentDescriptor | None:
        tid = resolve_tenant_id(tenant_id)
        boundary = self._boundaries.get(tid)
        candidates = []
        for agent in self._agents.get(tid, {}).values():
            if agent.status != "active":
                continue
            if capability not in agent.capabilities:
                continue
            if boundary and agent.autonomy_level > boundary.max_autonomy_level:
                continue
            candidates.append(agent)
        if not candidates:
            return None
        return sorted(
            candidates,
            key=lambda item: (item.composite_score or 0.0, item.autonomy_level),
            reverse=True,
        )[0]

    def isolate_agent(self, *, tenant_id: str | None, agent_id: str) -> AgentDescriptor:
        tid = resolve_tenant_id(tenant_id)
        agent = self._agents[tid][agent_id]
        isolated = replace(agent, status="isolated")
        self._agents[tid][agent_id] = isolated
        return isolated

    def get_agent(self, *, tenant_id: str | None, agent_id: str) -> AgentDescriptor:
        tid = resolve_tenant_id(tenant_id)
        return self._agents[tid][agent_id]


__all__ = ["AgentDescriptor", "InMemoryAgentMeshRepository", "TrustBoundary"]
