"""System 27 — Agent Mesh Infrastructure router.

Register / discover / route / isolate agents and set trust boundaries.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.agent_mesh_os.core import MeshError, get_agent_mesh
from auto_client_acquisition.agent_mesh_os.schemas import (
    AgentDescriptor,
    AgentStatus,
    TrustBoundary,
    TrustTier,
)

router = APIRouter(prefix="/api/v1/agent-mesh", tags=["agent-mesh"])


class AgentBody(BaseModel):
    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    capabilities: list[str] = Field(default_factory=list)
    trust_tier: TrustTier = TrustTier.INTERNAL
    autonomy_level: int = Field(default=2, ge=0, le=4)
    endpoint: str = ""


class RouteBody(BaseModel):
    capability: str = Field(..., min_length=1)
    customer_id: str = ""


class IsolateBody(BaseModel):
    actor: str = "system"
    reason: str = ""


class TrustBoundaryBody(BaseModel):
    allowed_capabilities: list[str] = Field(default_factory=list)
    denied_capabilities: list[str] = Field(default_factory=list)
    max_autonomy_level: int = Field(default=4, ge=0, le=4)


class ScoreBody(BaseModel):
    reliability: float = Field(..., ge=0.0, le=1.0)
    safety: float = Field(..., ge=0.0, le=1.0)
    latency_ms: float = Field(..., ge=0.0)


@router.post("/agents", status_code=201)
async def register_agent(body: AgentBody) -> dict[str, Any]:
    descriptor = AgentDescriptor(status=AgentStatus.ACTIVE, **body.model_dump())
    try:
        stored = get_agent_mesh().register_agent(descriptor)
    except MeshError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return stored.model_dump(mode="json")


@router.get("/agents")
async def list_agents(capability: str | None = None) -> dict[str, Any]:
    mesh = get_agent_mesh()
    agents = mesh.discover(capability) if capability else mesh.list_agents()
    return {"count": len(agents), "agents": [a.model_dump(mode="json") for a in agents]}


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str) -> dict[str, Any]:
    try:
        return get_agent_mesh().monitor(agent_id)
    except MeshError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/route")
async def route(body: RouteBody) -> dict[str, Any]:
    decision = get_agent_mesh().route(
        capability=body.capability, customer_id=body.customer_id
    )
    return decision.model_dump(mode="json")


@router.post("/agents/{agent_id}/isolate")
async def isolate_agent(agent_id: str, body: IsolateBody) -> dict[str, Any]:
    try:
        agent = get_agent_mesh().isolate_agent(
            agent_id, actor=body.actor, reason=body.reason
        )
    except MeshError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return agent.model_dump(mode="json")


@router.put("/agents/{agent_id}/trust-boundary")
async def set_trust_boundary(agent_id: str, body: TrustBoundaryBody) -> dict[str, Any]:
    boundary = TrustBoundary(agent_id=agent_id, **body.model_dump())
    try:
        stored = get_agent_mesh().set_trust_boundary(boundary)
    except MeshError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return stored.model_dump(mode="json")


@router.get("/agents/{agent_id}/score")
async def score_agent(agent_id: str, reliability: float, safety: float, latency_ms: float) -> dict[str, Any]:
    try:
        score = get_agent_mesh().score_agent(
            agent_id, reliability=reliability, safety=safety, latency_ms=latency_ms
        )
    except MeshError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return score.model_dump(mode="json")
