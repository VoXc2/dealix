"""System 28: Assurance Contracts router."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/assurance-contracts", tags=["assurance-contracts"])


@router.get("/health")
async def assurance_contracts_health() -> dict[str, str]:
    return {"system": "28_assurance_contracts", "status": "ok"}
