"""Company Service — customer-safe command surface (read-only)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.revenue_execution.company_portal_snapshot import build_company_command_center

router = APIRouter(prefix="/api/v1/company-service", tags=["company-service"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "company_service",
        "command_center": "/api/v1/company-service/command-center",
        "guardrails": {
            "no_internal_jargon_in_command_center": True,
            "approval_first_external": True,
        },
    }


@router.get("/command-center")
async def company_command_center() -> dict[str, Any]:
    """Single JSON for company-facing weekly rhythm (Arabic-first hints)."""
    return build_company_command_center()
