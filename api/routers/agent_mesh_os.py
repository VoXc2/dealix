"""System 27: Agent Mesh router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/agent-mesh", tags=["agent-mesh"])


@router.get("/health")
async def agent_mesh_health() -> dict[str, str]:
    return {"system": "27_agent_mesh", "status": "ok"}
