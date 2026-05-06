"""Thin company-service router for compatibility checks."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from api.routers.customer_company_portal import customer_portal

router = APIRouter(prefix="/api/v1/company-service", tags=["company-service"])


@router.get("/status")
async def company_service_status() -> dict[str, Any]:
    return {
        "service": "company_service",
        "status": "operational",
        "mode": "compatibility_thin_wrapper",
        "next_action_ar": "استخدم /command-center لواجهة الشركة المختصرة",
        "next_action_en": "Use /command-center for the simplified company view.",
    }


@router.get("/command-center")
async def company_service_command_center(
    customer_handle: str = "Slot-A",
) -> dict[str, Any]:
    """Compatibility endpoint expected by older verification prompts.

    Delegates to customer-portal view and exposes only customer-facing sections.
    """
    portal = await customer_portal(customer_handle)
    return {
        "schema_version": 1,
        "experience_layer": "company_service",
        "customer_handle": portal.get("customer_handle", customer_handle),
        "sections": portal.get("sections", {}),
        "next_decision": portal.get("sections", {}).get("8_next_decision", {}),
    }
