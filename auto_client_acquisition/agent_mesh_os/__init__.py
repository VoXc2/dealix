"""Agent Mesh OS (tenant-aware routing + isolation + autonomy ceiling)."""

from auto_client_acquisition.agent_mesh_os.repositories import AgentMeshRepository
from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor

__all__ = ["AgentDescriptor", "AgentMeshRepository"]
