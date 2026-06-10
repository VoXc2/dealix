"""System 26: Enterprise Control Plane router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/control-plane", tags=["control-plane"])


@router.get("/health")
async def control_plane_health() -> dict[str, str]:
    return {"system": "26_control_plane", "status": "ok"}
