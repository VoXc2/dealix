"""Executive OS — founder brief delegate (read-only weekly pack)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.executive_reporting import build_weekly_report

router = APIRouter(prefix="/api/v1/executive-os", tags=["executive-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "executive_os",
        "delegate": "executive_reporting",
        "weekly": "/api/v1/executive-report/weekly",
        "guardrails": {
            "no_llm_call": True,
            "no_external_http": True,
            "no_marketing_claims": True,
        },
    }


@router.get("/weekly-pack")
async def weekly_pack() -> dict[str, Any]:
    """Same payload as GET /api/v1/executive-report/weekly (bilingual)."""
    return build_weekly_report().model_dump(mode="json")
