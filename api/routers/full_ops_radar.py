"""Full-Ops Radar HTTP surface (Phase 4).

  GET /api/v1/full-ops/status
  GET /api/v1/full-ops/score
  GET /api/v1/full-ops/weaknesses
  GET /api/v1/full-ops/evidence

Read-only. Read-safe.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.full_ops_radar import (
    SCORE_WEIGHTS,
    collect_evidence,
    compute_full_ops_score,
    detect_weaknesses,
    run_all_health_checks,
)

router = APIRouter(prefix="/api/v1/full-ops-radar", tags=["full-ops-radar"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_fake_proof": True,
    "no_fake_green": True,
    "read_only": True,
    "every_score_traceable_to_evidence": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "full_ops_radar",
        "version": "1.0.0",
        "weights_table": SCORE_WEIGHTS,
        "readiness_labels": [
            "Full Ops Ready (90-100)",
            "Customer Ready with Manual Ops (75-89)",
            "Diagnostic Only (60-74)",
            "Internal Only (<60)",
        ],
        "hard_gates": _HARD_GATES,
    }


@router.get("/score")
async def score() -> dict[str, Any]:
    s = compute_full_ops_score()
    return {**s, "hard_gates": _HARD_GATES}


@router.get("/weaknesses")
async def weaknesses(customer_handle: str | None = None) -> dict[str, Any]:
    weaknesses_list = detect_weaknesses(customer_handle=customer_handle)
    critical = [w for w in weaknesses_list if w["severity"] == "critical"]
    return {
        "count": len(weaknesses_list),
        "critical_count": len(critical),
        "weaknesses": weaknesses_list,
        "hard_gates": _HARD_GATES,
    }


@router.get("/evidence")
async def evidence() -> dict[str, Any]:
    e = collect_evidence()
    return {**e, "hard_gates": _HARD_GATES}
