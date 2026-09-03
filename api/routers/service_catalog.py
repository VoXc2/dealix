"""Dealix launch-authorized service catalog HTTP surface.

The full service registry remains an internal product/delivery planning source.
The public HTTP catalog deliberately exposes only the current buying path:
Free Mini Diagnostic -> Qualified Discovery -> customer-specific quote ->
30-Day Revenue Command Pilot.

No fixed-price expansion catalogue is published during launch.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.service_catalog import (
    ServiceOffering,
    build_governed_revenue_ai_ops_blueprint,
    get_offering,
    list_offerings,
)

router = APIRouter(prefix="/api/v1/services", tags=["Service Catalog"])

_LAUNCH_AUTHORIZED_SERVICE_IDS = (
    "free_mini_diagnostic",
    "revenue_command_pilot_30d",
)

_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "no_guaranteed_claims": True,
    "no_public_fixed_price_catalog": True,
    "no_public_checkout": True,
}


def _launch_offerings() -> list[ServiceOffering]:
    by_id = {offering.id: offering for offering in list_offerings()}
    missing = [service_id for service_id in _LAUNCH_AUTHORIZED_SERVICE_IDS if service_id not in by_id]
    if missing:
        raise RuntimeError(f"launch_authorized_service_missing:{','.join(missing)}")
    return [by_id[service_id] for service_id in _LAUNCH_AUTHORIZED_SERVICE_IDS]


def _serialize_launch_authority(offering: ServiceOffering) -> dict[str, Any]:
    """Serialize launch-safe product truth without publishing a fixed price catalogue."""
    data = offering.model_dump()
    for key in (
        "price_sar",
        "price_sar_max",
        "price_monthly_sar_min",
        "price_monthly_sar_max",
    ):
        data.pop(key, None)

    if offering.id == "free_mini_diagnostic":
        price_model = "free"
    else:
        price_model = "customer_specific_quote_only"

    data["price_model"] = price_model
    data["public_fixed_price"] = False
    data["public_checkout"] = False
    data["price_authority"] = (
        "none_required_free_entry"
        if offering.id == "free_mini_diagnostic"
        else "customer_specific_quote_after_qualified_discovery"
    )
    return data


@router.get("/status")
async def service_catalog_status() -> dict[str, Any]:
    """Launch catalog health and hard gates; does not publish internal catalogue entries."""
    offerings = _launch_offerings()
    return {
        "status": "ok",
        "launch_authorized_offerings_count": len(offerings),
        "service_ids": [o.id for o in offerings],
        "hard_gates": _HARD_GATES,
        "authority": "launch_catalog_only",
        "public_fixed_pricing": False,
        "public_checkout": False,
        "is_estimate": False,
    }


@router.get("/catalog")
async def service_catalog() -> dict[str, Any]:
    """Only the launch-authorized entry + primary paid motion, with no fixed prices."""
    offerings = _launch_offerings()
    return {
        "offerings": [_serialize_launch_authority(o) for o in offerings],
        "count": len(offerings),
        "hard_gates": _HARD_GATES,
        "commercial_path": [
            "FREE_MINI_DIAGNOSTIC",
            "QUALIFIED_DISCOVERY",
            "CUSTOMER_SPECIFIC_QUOTE",
            "REVENUE_COMMAND_PILOT_30D",
        ],
    }


@router.get("/governed-operating-model")
async def governed_operating_model() -> dict[str, Any]:
    """Founder-facing strategy payload; not pricing or checkout authority."""
    payload = build_governed_revenue_ai_ops_blueprint()
    return {
        "operating_model": payload,
        "commercial_authority": {
            "public_fixed_pricing": False,
            "public_checkout": False,
            "primary_paid_offer": "revenue_command_pilot_30d",
            "price_authority": "customer_specific_quote_after_qualified_discovery",
        },
    }


@router.get("/{service_id}")
async def service_offering_detail(service_id: str) -> dict[str, Any]:
    """Return details only for launch-authorized offers; expansion catalogue stays internal."""
    if service_id not in _LAUNCH_AUTHORIZED_SERVICE_IDS:
        raise HTTPException(
            status_code=404,
            detail={
                "reason": "service_not_publicly_launch_authorized",
                "public_service_ids": list(_LAUNCH_AUTHORIZED_SERVICE_IDS),
                "primary_paid_offer": "revenue_command_pilot_30d",
            },
        )
    offering = get_offering(service_id)
    if offering is None:
        raise HTTPException(status_code=404, detail=f"unknown_service_id: {service_id}")
    return {
        "offering": _serialize_launch_authority(offering),
        "hard_gates": _HARD_GATES,
    }
