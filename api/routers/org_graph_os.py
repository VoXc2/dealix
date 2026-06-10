"""System 30: Org Graph router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/org-graph", tags=["org-graph"])


@router.get("/health")
async def org_graph_health() -> dict[str, str]:
    return {"system": "30_org_graph", "status": "ok"}
