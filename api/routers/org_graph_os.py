"""System 30 — Operational Memory Graph router.

Add nodes / edges, traverse neighbours and dependencies, and compute the
blast radius of an incident.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.org_graph_os.core import GraphError, get_org_graph
from auto_client_acquisition.org_graph_os.schemas import (
    GraphEdge,
    GraphNode,
    NodeType,
    Relation,
)

router = APIRouter(prefix="/api/v1/org-graph", tags=["org-graph"])


class NodeBody(BaseModel):
    node_id: str = Field(..., min_length=1)
    node_type: NodeType
    label: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)


class EdgeBody(BaseModel):
    from_id: str = Field(..., min_length=1)
    to_id: str = Field(..., min_length=1)
    relation: Relation = Relation.RELATED_TO
    weight: float = 1.0


@router.post("/nodes", status_code=201)
async def add_node(body: NodeBody) -> dict[str, Any]:
    node = get_org_graph().add_node(GraphNode(**body.model_dump()))
    return node.model_dump(mode="json")


@router.post("/edges", status_code=201)
async def add_edge(body: EdgeBody) -> dict[str, Any]:
    try:
        edge = get_org_graph().add_edge(GraphEdge(**body.model_dump()))
    except GraphError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return edge.model_dump(mode="json")


@router.get("/nodes/{node_id}/neighbors")
async def neighbors(node_id: str, relation: str | None = None) -> dict[str, Any]:
    try:
        nodes = get_org_graph().neighbors(node_id, relation=relation)
    except GraphError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"count": len(nodes), "neighbors": [n.model_dump(mode="json") for n in nodes]}


@router.get("/nodes/{node_id}/dependencies")
async def dependencies(node_id: str) -> dict[str, Any]:
    try:
        nodes = get_org_graph().dependencies(node_id)
    except GraphError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "count": len(nodes),
        "dependencies": [n.model_dump(mode="json") for n in nodes],
    }


@router.get("/incidents/{incident_id}/impact")
async def incident_impact(incident_id: str) -> dict[str, Any]:
    try:
        impact = get_org_graph().incident_impact(incident_id)
    except GraphError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return impact.model_dump(mode="json")
