"""System 32: Simulation router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/simulation", tags=["simulation"])


@router.get("/health")
async def simulation_health() -> dict[str, str]:
    return {"system": "32_simulation", "status": "ok"}
