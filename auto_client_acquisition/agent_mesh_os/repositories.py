"""In-memory agent mesh repository with tenant-aware routing rules."""

from __future__ import annotations

from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor
from auto_client_acquisition.control_plane_os.tenant_context import ensure_tenant_id


class AgentMeshRepository:
    """Tenant-scoped agent registry + deterministic routing."""

    def __init__(self, *, autonomy_ceiling: int = 3) -> None:
        self._autonomy_ceiling = autonomy_ceiling
        self._agents: dict[str, AgentDescriptor] = {}

    def register(self, descriptor: AgentDescriptor) -> AgentDescriptor:
        if descriptor.autonomy_level > self._autonomy_ceiling:
            raise ValueError("mvp_autonomy_ceiling_exceeded")
        self._agents[descriptor.agent_id] = descriptor
        return descriptor

    def get(self, *, tenant_id: str, agent_id: str) -> AgentDescriptor | None:
        tenant = ensure_tenant_id(tenant_id)
        row = self._agents.get(agent_id)
        if row is None or row.tenant_id != tenant:
            return None
        return row

    def isolate(self, *, tenant_id: str, agent_id: str) -> AgentDescriptor:
        row = self.get(tenant_id=tenant_id, agent_id=agent_id)
        if row is None:
            raise ValueError("agent_not_found")
        isolated = row.model_copy(update={"status": "isolated"})
        self._agents[agent_id] = isolated
        return isolated

    def list(self, *, tenant_id: str) -> list[AgentDescriptor]:
        tenant = ensure_tenant_id(tenant_id)
        return [row for row in self._agents.values() if row.tenant_id == tenant]

    def route(
        self,
        *,
        tenant_id: str,
        capability: str,
    ) -> AgentDescriptor:
        tenant = ensure_tenant_id(tenant_id)
        candidates = [
            row
            for row in self._agents.values()
            if row.tenant_id == tenant
            and row.status == "active"
            and row.autonomy_level <= self._autonomy_ceiling
            and capability in row.capabilities
        ]
        if not candidates:
            raise ValueError("no_routable_agent")
        # Highest composite score wins.
        candidates.sort(key=lambda row: row.composite_score, reverse=True)
        return candidates[0]

    def clear_for_test(self) -> None:
        self._agents.clear()


__all__ = ["AgentMeshRepository"]
