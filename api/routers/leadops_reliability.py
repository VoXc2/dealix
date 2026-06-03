"""LeadOps Reliability HTTP surface (Phase 4 Wave 5).

Read-only diagnostic surface OVER existing leadops_spine. Uses NEW
distinct paths (`/reliability`, `/debug-trace`, `/next-fix`) to avoid
shadowing the existing leadops_spine endpoints (`/status`, `/run`,
`/brief`, `/draft`, `/debug`).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.leadops_reliability import (
    diagnose,
    overall_status,
    queue_health,
    source_health,
    suggest_next_fix,
)

# Distinct prefix to avoid shadowing existing leadops endpoints
router = APIRouter(prefix="/api/v1/leadops", tags=["leadops-reliability"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "read_only": True,
    "approval_required_for_external_actions": True,
}


@router.get("/reliability")
async def reliability() -> dict[str, Any]:
    return {
        "status": overall_status(),
        "queue_health": queue_health(),
        "source_health": source_health(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/debug-trace")
async def debug_trace() -> dict[str, Any]:
    return {
        "diagnostic": diagnose(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/next-fix")
async def next_fix() -> dict[str, Any]:
    return {
        "next_fix": suggest_next_fix(),
        "hard_gates": _HARD_GATES,
    }
