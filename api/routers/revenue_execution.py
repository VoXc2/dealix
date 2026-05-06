"""Revenue execution — daily command center facade (read-only)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.revenue_execution import build_daily_command_center

router = APIRouter(prefix="/api/v1/full-ops", tags=["full-ops-revenue-execution"])


@router.get("/daily-command-center")
async def daily_command_center() -> dict[str, Any]:
    """Single founder-facing snapshot. Always 200; check ``degraded_sections`` if partial."""
    return build_daily_command_center()


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "revenue_execution",
        "endpoints": ["/daily-command-center"],
        "aliases": {"revenue_execution_prefix": "/api/v1/full-ops"},
    }
