"""Reliability OS v5 — health matrix endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from auto_client_acquisition.reliability_os import (
    build_health_matrix,
    summary,
)

router = APIRouter(prefix="/api/v1/reliability", tags=["reliability"])


@router.get("/status")
async def status() -> dict:
    return {"module": "reliability_os", **summary()}


@router.get("/health-matrix")
async def health_matrix() -> dict:
    """Aggregated health probe over local subsystems.

    NEVER opens network connections (other than what individual probes
    already do). NEVER writes to DB.
    """
    return build_health_matrix()
