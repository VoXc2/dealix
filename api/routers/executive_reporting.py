"""Executive Reporting v6 — weekly report endpoints.

Pure read-only composition. NEVER calls an LLM, NEVER persists,
NEVER opens external HTTP.
"""
from __future__ import annotations

from fastapi import APIRouter

from auto_client_acquisition.executive_reporting import build_weekly_report

router = APIRouter(prefix="/api/v1/executive-report", tags=["executive-reporting"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "executive_reporting",
        "version": 1,
        "guardrails": {
            "no_llm_call": True,
            "no_external_http": True,
            "no_marketing_claims": True,
            "no_pii_in_report": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/weekly")
async def weekly() -> dict:
    """Compose the bilingual weekly executive report.

    Wraps ``executive_reporting.build_weekly_report``. Pure read-only
    aggregation over service_activation_matrix, weekly_growth_scorecard,
    daily_growth_loop, reliability_os, and proof_ledger.
    """
    report = build_weekly_report()
    return report.model_dump(mode="json")
