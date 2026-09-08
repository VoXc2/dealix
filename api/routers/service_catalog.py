"""Launch-safe public catalog and admin-only market-to-delivery preparation.

The existing public offering IDs and quote/Approval Center authority remain unchanged.
Research hypotheses never become approved offers, consent or delivery capacity.
"""
from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from api.security.api_key import founder_admin_keys, require_founder_admin_key
from auto_client_acquisition.service_catalog import (
    ServiceOffering,
    build_governed_revenue_ai_ops_blueprint,
    get_offering,
    list_offerings,
)
from auto_client_acquisition.service_catalog.market_to_delivery import load_catalog, prepare

router = APIRouter(prefix="/api/v1/services", tags=["Service Catalog"])
_LAUNCH_AUTHORIZED_SERVICE_IDS = ("free_mini_diagnostic", "revenue_command_pilot_30d")
_HARD_GATES = {
    "no_live_send": True, "no_live_charge": True, "no_fake_revenue": True,
    "no_fake_proof": True, "no_guaranteed_claims": True,
    "no_public_fixed_price_catalog": True, "no_public_checkout": True,
}


def _launch_offerings() -> list[ServiceOffering]:
    by_id = {offering.id: offering for offering in list_offerings()}
    missing = [service_id for service_id in _LAUNCH_AUTHORIZED_SERVICE_IDS if service_id not in by_id]
    if missing:
        raise RuntimeError(f"launch_authorized_service_missing:{','.join(missing)}")
    return [by_id[service_id] for service_id in _LAUNCH_AUTHORIZED_SERVICE_IDS]


def _serialize_launch_authority(offering: ServiceOffering) -> dict[str, Any]:
    data = offering.model_dump()
    for key in ("price_sar", "price_sar_max", "price_monthly_sar_min", "price_monthly_sar_max"):
        data.pop(key, None)
    data["price_model"] = "free" if offering.id == "free_mini_diagnostic" else "customer_specific_quote_only"
    data["public_fixed_price"] = False
    data["public_checkout"] = False
    data["price_authority"] = (
        "none_required_free_entry" if offering.id == "free_mini_diagnostic"
        else "customer_specific_quote_after_qualified_discovery"
    )
    return data


@router.get("/status")
async def service_catalog_status() -> dict[str, Any]:
    offerings = _launch_offerings()
    return {"status": "ok", "launch_authorized_offerings_count": len(offerings),
            "service_ids": [o.id for o in offerings], "hard_gates": _HARD_GATES,
            "authority": "launch_catalog_only", "public_fixed_pricing": False,
            "public_checkout": False, "is_estimate": False}


@router.get("/catalog")
async def service_catalog() -> dict[str, Any]:
    offerings = _launch_offerings()
    return {"offerings": [_serialize_launch_authority(o) for o in offerings],
            "count": len(offerings), "hard_gates": _HARD_GATES,
            "commercial_path": ["FREE_MINI_DIAGNOSTIC", "QUALIFIED_DISCOVERY",
                                "CUSTOMER_SPECIFIC_QUOTE", "REVENUE_COMMAND_PILOT_30D"]}


@router.get("/governed-operating-model")
async def governed_operating_model() -> dict[str, Any]:
    return {"operating_model": build_governed_revenue_ai_ops_blueprint(),
            "commercial_authority": {"public_fixed_pricing": False, "public_checkout": False,
                                     "primary_paid_offer": "revenue_command_pilot_30d",
                                     "price_authority": "customer_specific_quote_after_qualified_discovery"}}


def _require_mtd_admin_configured() -> None:
    # Unlike generic dev-mode routes, this preparation surface is never anonymous.
    if not founder_admin_keys():
        raise HTTPException(status_code=503, detail={"reason": "admin_authentication_not_configured"})


@router.get("/market-to-delivery/catalog", dependencies=[Depends(_require_mtd_admin_configured), Depends(require_founder_admin_key)])
async def market_to_delivery_catalog() -> dict[str, Any]:
    return {"catalog": load_catalog(), "authority": "INTERNAL_RESEARCH_ONLY", "live_effects": False}


@router.post("/market-to-delivery/prepare", dependencies=[Depends(_require_mtd_admin_configured), Depends(require_founder_admin_key)])
async def prepare_market_to_delivery(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Admin-only preparation. Does not fetch evidence, approve, persist or send.

    data_authorized is a submitter declaration, not independent verification.
    Actual approvals and tenant data authority stay with the canonical stores.
    """
    try:
        return prepare(payload)
    except ValueError as exc:
        reason = str(exc)
        if not reason.replace('_', '').isalnum():
            reason = 'invalid_preparation_request'
        raise HTTPException(status_code=422, detail={"reason": reason}) from exc


@router.get("/{service_id}")
async def service_offering_detail(service_id: str) -> dict[str, Any]:
    if service_id not in _LAUNCH_AUTHORIZED_SERVICE_IDS:
        raise HTTPException(status_code=404, detail={
            "reason": "service_not_publicly_launch_authorized",
            "public_service_ids": list(_LAUNCH_AUTHORIZED_SERVICE_IDS),
            "primary_paid_offer": "revenue_command_pilot_30d"})
    offering = get_offering(service_id)
    if offering is None:
        raise HTTPException(status_code=404, detail=f"unknown_service_id: {service_id}")
    return {"offering": _serialize_launch_authority(offering), "hard_gates": _HARD_GATES}
