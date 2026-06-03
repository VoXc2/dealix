"""Delivery Factory v5 — per-service delivery plan.

V11 hardening: ``/status`` and ``/services`` return 200 + ``degraded=true``
when the underlying YAML registry is unavailable instead of 500.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.delivery_factory import (
    build_delivery_plan,
    list_available_services,
)
from auto_client_acquisition.runtime_paths import (
    registry_dir_exists,
    resolve_registry_dir,
)

router = APIRouter(prefix="/api/v1/delivery-factory", tags=["delivery-factory"])


_HARD_GATES = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def status() -> dict:
    """Return delivery-factory readiness — 200 always, degraded when
    the YAML registry is missing or fails to load.
    """
    if not registry_dir_exists():
        return {
            "service": "delivery_factory",
            "module": "delivery_factory",
            "status": "degraded",
            "version": "v5",
            "degraded": True,
            "blocker": "registry_missing",
            "registry_dir": str(resolve_registry_dir()),
            "services_total": 0,
            "checks": {"registry_dir_exists": False},
            "hard_gates": _HARD_GATES,
            "guardrails": _HARD_GATES,
            "next_action_ar": "تأكد أن docs/registry مضمنة في Docker image",
            "next_action_en": (
                "Ensure docs/registry/ is included in the Docker image."
            ),
        }
    try:
        services = list_available_services()
    except BaseException as exc:
        return {
            "service": "delivery_factory",
            "module": "delivery_factory",
            "status": "degraded",
            "version": "v5",
            "degraded": True,
            "blocker": "registry_load_failed",
            "error_type": type(exc).__name__,
            "services_total": 0,
            "checks": {"registry_dir_exists": True, "registry_loaded": False},
            "hard_gates": _HARD_GATES,
            "guardrails": _HARD_GATES,
            "next_action_ar": "افحص YAML الخاص بـ SERVICE_READINESS_MATRIX",
            "next_action_en": "Inspect SERVICE_READINESS_MATRIX YAML.",
        }
    return {
        "service": "delivery_factory",
        "module": "delivery_factory",
        "status": "operational",
        "version": "v5",
        "degraded": False,
        "services_total": len(services),
        "checks": {"registry_dir_exists": True, "registry_loaded": True},
        "hard_gates": _HARD_GATES,
        "guardrails": _HARD_GATES,
        "next_action_ar": "كل الخدمات جاهزة للقراءة",
        "next_action_en": "All services ready to read.",
    }


@router.get("/services")
async def services() -> dict:
    """List services. If registry missing, return empty + degraded marker."""
    if not registry_dir_exists():
        return {"services": [], "degraded": True, "blocker": "registry_missing"}
    try:
        return {"services": list_available_services()}
    except BaseException as exc:
        return {
            "services": [],
            "degraded": True,
            "blocker": "registry_load_failed",
            "error_type": type(exc).__name__,
        }


@router.get("/plan/{service_id}")
async def plan(service_id: str) -> dict:
    """Build the delivery plan for one service from the YAML matrix."""
    try:
        return build_delivery_plan(service_id).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
