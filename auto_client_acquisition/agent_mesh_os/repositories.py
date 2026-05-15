"""In-memory agent mesh repository with tenant-aware routing."""

from __future__ import annotations

from dataclasses import replace

from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor


class InMemoryAgentMeshRepository:
    def __init__(self) -> None:
        self._agents: dict[tuple[str, str], AgentDescriptor] = {}

    def register_agent(self, descriptor: AgentDescriptor) -> AgentDescriptor:
        self._agents[(descriptor.tenant_id, descriptor.agent_id)] = descriptor
        return descriptor

    def get_agent(self, *, tenant_id: str, agent_id: str) -> AgentDescriptor:
        try:
            return self._agents[(tenant_id, agent_id)]
        except KeyError as exc:
            raise ValueError("agent_not_found") from exc

    def isolate_agent(self, *, tenant_id: str, agent_id: str) -> AgentDescriptor:
        agent = self.get_agent(tenant_id=tenant_id, agent_id=agent_id)
        isolated = replace(agent, status="isolated")
        self._agents[(tenant_id, agent_id)] = isolated
        return isolated

    def list_agents(self, *, tenant_id: str) -> list[AgentDescriptor]:
        return [a for (tid, _), a in self._agents.items() if tid == tenant_id]

    def route_agent(
        self,
        *,
        tenant_id: str,
        capability: str,
        max_autonomy: int,
    ) -> AgentDescriptor:
        eligible = []
        for agent in self.list_agents(tenant_id=tenant_id):
            if agent.status != "active":
                continue
            if capability not in agent.capabilities:
                continue
            if agent.autonomy_level > max_autonomy:
                continue
            eligible.append(agent)
        if not eligible:
            raise ValueError("no_eligible_agent")
        eligible.sort(key=lambda a: (a.composite_score, -a.autonomy_level), reverse=True)
        return eligible[0]
