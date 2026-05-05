"""CompanyBrain v5 — read-only snapshot endpoint."""
from __future__ import annotations

from fastapi import APIRouter

from auto_client_acquisition.company_brain import build_company_brain

router = APIRouter(prefix="/api/v1/company-brain", tags=["company-brain"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "company_brain",
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
            "no_llm_calls": True,
        },
    }


@router.get("/")
async def get_brain() -> dict:
    return build_company_brain().as_dict()
