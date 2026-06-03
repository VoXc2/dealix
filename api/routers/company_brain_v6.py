"""CompanyBrain v6 — per-customer brain endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.company_brain_v6 import (
    BuildRequest,
    build_company_brain_v6,
    next_best_action,
    recommend_service,
)

router = APIRouter(prefix="/api/v1/company-brain-v6", tags=["company-brain-v6"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "company_brain_v6",
        "guardrails": {
            "no_llm_calls": True,
            "no_external_http": True,
            "approval_required": True,
        },
    }


@router.post("/build")
async def build(payload: BuildRequest) -> dict[str, Any]:
    return build_company_brain_v6(payload).as_dict()


@router.post("/service-match")
async def service_match(payload: BuildRequest) -> dict[str, Any]:
    brain = build_company_brain_v6(payload)
    return {"recommended_service": recommend_service(brain)}


@router.post("/next-action")
async def next_action(payload: BuildRequest) -> dict[str, Any]:
    brain = build_company_brain_v6(payload)
    return {"next_best_action": next_best_action(brain)}
