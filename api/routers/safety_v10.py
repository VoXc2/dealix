"""Safety v10 — red-team eval pack endpoints (read + run, no external send)."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.safety_v10 import (
    EVAL_CASES,
    policy_engine_check,
    run_safety_eval,
)

router = APIRouter(prefix="/api/v1/safety-v10", tags=["safety-v10"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "safety_v10",
        "cases_total": len(EVAL_CASES),
        "categories": sorted({c.category for c in EVAL_CASES}),
        "guardrails": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_linkedin_automation": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
            "no_llm_call_in_eval_pack": True,
        },
    }


@router.get("/cases")
async def list_cases() -> dict:
    return {
        "total": len(EVAL_CASES),
        "cases": [
            {"id": c.id, "category": c.category, "expected_action": c.expected_action}
            for c in EVAL_CASES
        ],
    }


@router.post("/run")
async def run(payload: dict | None = Body(default=None)) -> dict:
    """Run the eval pack. Optional body: {"case_ids": [...]} to subset."""
    payload = payload or {}
    case_ids = payload.get("case_ids")
    cases = list(EVAL_CASES)
    if case_ids:
        if not isinstance(case_ids, list) or not all(isinstance(x, str) for x in case_ids):
            raise HTTPException(
                status_code=400,
                detail="case_ids must be a list of strings",
            )
        wanted = set(case_ids)
        cases = [c for c in EVAL_CASES if c.id in wanted]
        if not cases:
            raise HTTPException(
                status_code=404,
                detail="no matching case_ids found",
            )
    report = run_safety_eval(cases)
    return report.to_dict()


@router.post("/check-text")
async def check_text(payload: dict = Body(...)) -> dict:
    text = payload.get("text", "")
    declared = payload.get("declared_action", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=400, detail="payload.text must be a string")
    if not isinstance(declared, str):
        raise HTTPException(
            status_code=400,
            detail="payload.declared_action must be a string",
        )
    result = policy_engine_check(text, declared_action=declared)
    return result.to_dict()
