"""Delivery Factory v5 — per-service delivery plan."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.delivery_factory import (
    build_delivery_plan,
    list_available_services,
)

router = APIRouter(prefix="/api/v1/delivery-factory", tags=["delivery-factory"])


@router.get("/status")
async def status() -> dict:
    services = list_available_services()
    return {
        "module": "delivery_factory",
        "services_total": len(services),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/services")
async def services() -> dict:
    return {"services": list_available_services()}


@router.get("/plan/{service_id}")
async def plan(service_id: str) -> dict:
    """Build the delivery plan for one service from the YAML matrix."""
    try:
        return build_delivery_plan(service_id).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
