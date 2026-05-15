"""System 27 — Agent Mesh Infrastructure.

Discovery, capability registry, routing, trust boundaries and inter-agent
governance for an ecosystem of agents (internal, partner, vendor, third-party).

Autonomy is capped at the MVP ceiling (`AutonomyLevel.QUEUE_FOR_APPROVAL`) —
no mesh agent may be registered above "queue for approval", so nothing in the
mesh auto-executes (`no_unbounded_agents`). Routing skips isolated agents.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.agent_mesh_os.schemas import (
    AgentDescriptor,
    AgentScore,
    AgentStatus,
    RoutingDecision,
    TrustBoundary,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit

_MODULE = "agent_mesh_os"

# No mesh agent may exceed "queue for approval" — nothing auto-executes.
AUTONOMY_CEILING: int = int(AutonomyLevel.QUEUE_FOR_APPROVAL)


class MeshError(ValueError):
    """Raised on an invalid mesh operation — never swallowed."""


class AgentMesh:
    """Registry + router for an ecosystem of agents."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentDescriptor] = {}
        self._boundaries: dict[str, TrustBoundary] = {}

    def register_agent(self, descriptor: AgentDescriptor) -> AgentDescriptor:
        """Register an agent. Rejects autonomy above the MVP ceiling."""
        if descriptor.autonomy_level > AUTONOMY_CEILING:
            raise MeshError(
                f"agent {descriptor.agent_id} autonomy {descriptor.autonomy_level} "
                f"exceeds ceiling {AUTONOMY_CEILING}"
            )
        self._agents[descriptor.agent_id] = descriptor
        emit(
            event_type=ControlEventType.AGENT_REGISTERED,
            source_module=_MODULE,
            subject_type="agent",
            subject_id=descriptor.agent_id,
            payload={
                "capabilities": descriptor.capabilities,
                "trust_tier": str(descriptor.trust_tier),
            },
        )
        return descriptor

    def get_agent(self, agent_id: str) -> AgentDescriptor | None:
        return self._agents.get(agent_id)

    def list_agents(self, *, capability: str | None = None) -> list[AgentDescriptor]:
        agents = list(self._agents.values())
        if capability:
            agents = [a for a in agents if capability in a.capabilities]
        return agents

    def discover(self, capability: str) -> list[AgentDescriptor]:
        """Discoverable agents for a capability — excludes isolated/retired."""
        return [
            a
            for a in self._agents.values()
            if capability in a.capabilities
            and a.status not in (AgentStatus.ISOLATED, AgentStatus.RETIRED)
        ]

    def route(self, *, capability: str, customer_id: str = "") -> RoutingDecision:
        """Route a capability request to the highest-scoring eligible agent."""
        candidates = self.discover(capability)
        if not candidates:
            return RoutingDecision(
                requested_capability=capability,
                chosen_agent_id=None,
                trust_tier=None,
                reason="no eligible (non-isolated) agent offers this capability",
            )
        chosen = max(candidates, key=lambda a: a.composite_score or 0.0)
        emit(
            event_type=ControlEventType.AGENT_ROUTED,
            source_module=_MODULE,
            subject_type="agent",
            subject_id=chosen.agent_id,
            payload={"capability": capability, "customer_id": customer_id},
        )
        return RoutingDecision(
            requested_capability=capability,
            chosen_agent_id=chosen.agent_id,
            trust_tier=str(chosen.trust_tier),
            reason=f"highest composite score among {len(candidates)} candidate(s)",
        )

    def set_trust_boundary(self, boundary: TrustBoundary) -> TrustBoundary:
        if boundary.agent_id not in self._agents:
            raise MeshError(f"unknown agent: {boundary.agent_id}")
        self._boundaries[boundary.agent_id] = boundary
        emit(
            event_type=ControlEventType.AGENT_TRUST_BOUNDARY_SET,
            source_module=_MODULE,
            subject_type="agent",
            subject_id=boundary.agent_id,
            payload={"max_autonomy_level": boundary.max_autonomy_level},
        )
        return boundary

    def get_trust_boundary(self, agent_id: str) -> TrustBoundary | None:
        return self._boundaries.get(agent_id)

    def isolate_agent(
        self, agent_id: str, *, actor: str = "system", reason: str = ""
    ) -> AgentDescriptor:
        """Isolate an agent — it stops being routable immediately."""
        agent = self._require(agent_id)
        agent.status = AgentStatus.ISOLATED
        emit(
            event_type=ControlEventType.AGENT_ISOLATED,
            source_module=_MODULE,
            actor=actor,
            subject_type="agent",
            subject_id=agent_id,
            decision="deny",
            payload={"reason": reason},
        )
        return agent

    def score_agent(
        self,
        agent_id: str,
        *,
        reliability: float,
        safety: float,
        latency_ms: float,
    ) -> AgentScore:
        """Score an agent. Composite weights safety highest, then reliability."""
        agent = self._require(agent_id)
        latency_factor = max(0.0, 1.0 - min(latency_ms, 5000.0) / 5000.0)
        composite = round(
            0.5 * safety + 0.35 * reliability + 0.15 * latency_factor, 4
        )
        agent.composite_score = composite
        return AgentScore(
            agent_id=agent_id,
            reliability=reliability,
            safety=safety,
            latency_ms=latency_ms,
            composite=composite,
        )

    def monitor(self, agent_id: str) -> dict[str, Any]:
        agent = self._require(agent_id)
        boundary = self._boundaries.get(agent_id)
        return {
            "agent": agent.model_dump(mode="json"),
            "trust_boundary": boundary.model_dump(mode="json") if boundary else None,
            "routable": agent.status not in (AgentStatus.ISOLATED, AgentStatus.RETIRED),
        }

    def _require(self, agent_id: str) -> AgentDescriptor:
        agent = self._agents.get(agent_id)
        if agent is None:
            raise MeshError(f"unknown agent: {agent_id}")
        return agent


_MESH: AgentMesh | None = None


def get_agent_mesh() -> AgentMesh:
    """Return the process-scoped agent mesh singleton."""
    global _MESH
    if _MESH is None:
        _MESH = AgentMesh()
    return _MESH


def reset_agent_mesh() -> None:
    """Test helper: drop the cached mesh."""
    global _MESH
    _MESH = None


__all__ = [
    "AUTONOMY_CEILING",
    "AgentMesh",
    "MeshError",
    "get_agent_mesh",
    "reset_agent_mesh",
]
