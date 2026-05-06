"""Delivery OS — thin alias over delivery_factory (read-only status + plan by id)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.delivery_factory import build_delivery_plan, list_available_services

router = APIRouter(prefix="/api/v1/delivery-os", tags=["delivery-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    services = list_available_services()
    return {
        "module": "delivery_os",
        "delegate": "delivery_factory",
        "services_total": len(services),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/session/{service_id}")
async def session_plan(service_id: str) -> dict[str, Any]:
    """Return delivery plan for a service id (same as GET /api/v1/delivery-factory/plan/{id})."""
    try:
        return build_delivery_plan(service_id).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
