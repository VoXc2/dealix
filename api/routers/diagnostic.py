"""
Diagnostic Router — bilingual diagnostic brief generator.
موجِّه التشخيص — مُولِّد موجز ثنائي اللغة.

Endpoints under /api/v1/diagnostic/:
    GET  /status     — module health + supported sectors + guardrails
    GET  /sectors    — list of supported sector keys
    POST /generate   — build a diagnostic brief from a request body

Pure local composition: no LLM calls, no live sends, no external HTTP.
Every generated brief is tagged ``approval_status="approval_required"``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    generate_diagnostic,
    list_supported_sectors,
)

router = APIRouter(prefix="/api/v1/diagnostic", tags=["diagnostic"])


@router.get("/status")
async def diagnostic_status() -> dict[str, Any]:
    """Module health, supported sectors, and active guardrails."""
    sectors = list_supported_sectors()
    return {
        "module": "diagnostic_engine",
        "status": "operational",
        "supported_sectors": sectors,
        "n_sectors": len(sectors),
        "guardrails": {
            "no_llm_calls": True,
            "no_live_sends": True,
            "no_external_http": True,
            "approval_required_on_every_brief": True,
            "pdpl_aware": True,
        },
    }


@router.get("/sectors")
async def diagnostic_sectors() -> dict[str, Any]:
    """List the sector keys backed by the Service Readiness Matrix."""
    return {"sectors": list_supported_sectors()}


@router.post("/generate")
async def diagnostic_generate(payload: DiagnosticRequest) -> dict[str, Any]:
    """Render a bilingual diagnostic brief — never auto-sent."""
    result = generate_diagnostic(payload)
    return result.model_dump(mode="json")
