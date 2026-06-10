"""LLM Gateway v10 router — routing + budget endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.llm_gateway_v10 import (
    BudgetPolicy,
    CostEstimate,
    RoutingPolicy,
    enforce_budget,
    estimate_cost,
    route,
)

router = APIRouter(prefix="/api/v1/llm-gateway-v10", tags=["llm-gateway-v10"])


class _EnforceBudgetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    estimates: list[CostEstimate]
    policy: BudgetPolicy


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "llm_gateway_v10",
        "guardrails": {
            "no_external_http": True,
            "no_llm_api_calls": True,
            "deterministic_routing": True,
            "bilingual_reason": True,
            "budget_enforced": True,
        },
    }


@router.post("/route")
async def route_endpoint(payload: RoutingPolicy) -> dict[str, Any]:
    try:
        decision = route(payload)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return decision.model_dump(mode="json")


@router.post("/estimate-cost")
async def estimate_cost_endpoint(payload: RoutingPolicy) -> dict[str, Any]:
    try:
        est = estimate_cost(payload)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return est.model_dump(mode="json")


@router.post("/enforce-budget")
async def enforce_budget_endpoint(payload: _EnforceBudgetRequest) -> dict[str, Any]:
    try:
        return enforce_budget(payload.estimates, payload.policy)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc)) from exc
