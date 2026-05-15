"""Evals OS router — run a quality suite, read run history.

Every response carries a ``governance_decision``.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.evals_os.eval_ledger import list_eval_runs
from auto_client_acquisition.evals_os.runner import SUITE_IDS, run_suite
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision

router = APIRouter(prefix="/api/v1/evals", tags=["Agents"])


class RunBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    suite_id: str = Field("all", min_length=1)


@router.post("/run")
async def run(body: RunBody) -> dict[str, Any]:
    if body.suite_id not in SUITE_IDS:
        raise HTTPException(
            status_code=422,
            detail=f"unknown suite_id {body.suite_id!r}; expected one of {list(SUITE_IDS)}",
        )
    summary = run_suite(body.suite_id, customer_id=body.customer_id)
    payload = summary.to_dict()
    payload["governance_decision"] = (
        GovernanceDecision.BLOCK.value
        if summary.regression_detected
        else GovernanceDecision.ALLOW.value
    )
    return payload


@router.get("/{customer_id}/history")
async def history(
    customer_id: str,
    suite_id: str | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
) -> dict[str, Any]:
    runs = list_eval_runs(customer_id=customer_id, suite_id=suite_id, limit=limit)
    return {
        "customer_id": customer_id,
        "count": len(runs),
        "runs": runs,
        "governance_decision": GovernanceDecision.ALLOW.value,
    }
