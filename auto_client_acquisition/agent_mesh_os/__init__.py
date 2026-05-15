"""System 27 — Agent Mesh Infrastructure.

Discovery, capability registry, routing, trust boundaries for an agent ecosystem.
"""

from auto_client_acquisition.agent_mesh_os.core import (
    AUTONOMY_CEILING,
    AgentMesh,
    MeshError,
    get_agent_mesh,
    reset_agent_mesh,
)
from auto_client_acquisition.agent_mesh_os.schemas import (
    AgentDescriptor,
    AgentScore,
    AgentStatus,
    RoutingDecision,
    TrustBoundary,
    TrustTier,
)

__all__ = [
    "AUTONOMY_CEILING",
    "AgentDescriptor",
    "AgentMesh",
    "AgentScore",
    "AgentStatus",
    "MeshError",
    "RoutingDecision",
    "TrustBoundary",
    "TrustTier",
    "get_agent_mesh",
    "reset_agent_mesh",
]
