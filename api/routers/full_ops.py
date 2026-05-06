"""V12 — Full-Ops umbrella router.

Single ``GET /api/v1/full-ops/daily-command-center`` returning all 5
active OS queues + top-3 decisions + blocked actions + hard gates.

Read-only. No external calls. Returns 200 always; degraded sections
are reported in ``degraded_sections`` rather than raising 5xx.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.full_ops.daily_cc_builder import (
    compose_daily_command_center,
    hard_gates_dict,
)

router = APIRouter(prefix="/api/v1/full-ops", tags=["full-ops"])


@router.get("/status")
async def full_ops_status() -> dict[str, Any]:
    return {
        "service": "full_ops",
        "module": "full_ops",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"work_queue": "ok"},
        "hard_gates": hard_gates_dict(),
        "next_action_ar": "افتح /daily-command-center للحصول على القرارات اليومية",
        "next_action_en": "Open /daily-command-center for today's decisions.",
    }


@router.get("/daily-command-center")
async def daily_command_center() -> dict[str, Any]:
    """Single bilingual snapshot across all 9 OSes.

    Read-only. 200 always. Degraded sections reported in
    ``degraded_sections`` rather than 5xx.
    """
    return compose_daily_command_center()
