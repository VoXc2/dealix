"""System 29: Sandbox router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/sandbox", tags=["sandbox"])


@router.get("/health")
async def sandbox_health() -> dict[str, str]:
    return {"system": "29_sandbox", "status": "ok"}
