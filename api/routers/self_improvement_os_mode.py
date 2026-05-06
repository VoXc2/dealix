"""Self-improvement OS — learning from shipped signals only (read-only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/self-improvement-os", tags=["self-improvement-os"])

REPO = Path(__file__).resolve().parents[2]
SCORECARD = REPO / "docs" / "snapshots" / "weekly_growth_scorecard.json"


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "self_improvement_os",
        "delegate": "self_growth",
        "weekly_learning": "/api/v1/self-improvement-os/weekly-learning",
        "guardrails": {
            "no_auto_pr": True,
            "no_fake_metrics": True,
        },
    }


@router.get("/weekly-learning")
async def weekly_learning() -> dict[str, Any]:
    """If scorecard snapshot exists, summarize gaps; else explicit insufficient_data."""
    if not SCORECARD.exists():
        return {
            "status": "insufficient_data",
            "message": "No weekly_growth_scorecard.json under docs/snapshots/.",
            "suggested_actions": [
                "Run internal weekly review and export a scorecard JSON (no PII).",
                "GET /api/v1/self-growth/scorecard/weekly for current in-process scorecard.",
            ],
        }
    try:
        raw = json.loads(SCORECARD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"invalid_json:{exc}") from exc
    return {
        "status": "ok",
        "source": str(SCORECARD.relative_to(REPO)),
        "keys": list(raw.keys())[:20],
        "note": "Human must interpret; no auto code changes.",
    }
