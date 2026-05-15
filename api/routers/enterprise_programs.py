"""Enterprise tier — HTTP surface for the 5 six-figure offerings.

Exposes the enterprise services, the 90-day Enterprise AI Transformation
Program structure, and per-service readiness scorecards:
- GET /api/v1/enterprise/status              — layer health + hard gates
- GET /api/v1/enterprise/services            — list the 5 enterprise offerings
- GET /api/v1/enterprise/services/{id}       — one offering + readiness
- GET /api/v1/enterprise/program             — 90-day program phase structure
- GET /api/v1/enterprise/readiness           — readiness scorecards

Read-only. Wraps ``service_catalog`` and ``enterprise_os``. The enterprise tier
is Planned (see dealix/registers/no_overclaim.yaml): every response carries
``sellable`` so no surface can present a service as buyable before its
readiness gates pass.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.enterprise_os.enterprise_program import (
    EnterpriseProgram,
    ProgramPhase,
    get_program,
)
from auto_client_acquisition.enterprise_os.enterprise_readiness import (
    ReadinessReport,
    get_readiness,
    list_readiness,
)
from auto_client_acquisition.service_catalog import (
    ServiceOffering,
    get_offering,
    list_enterprise_offerings,
)

router = APIRouter(prefix="/api/v1/enterprise", tags=["Enterprise Programs"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "no_guaranteed_claims": True,  # Article 8 forbids "guaranteed"/"نضمن"
}


def _phase(phase: ProgramPhase) -> dict[str, Any]:
    return {
        "key": phase.key,
        "name_ar": phase.name_ar,
        "name_en": phase.name_en,
        "week_start": phase.week_start,
        "week_end": phase.week_end,
        "deliverables": list(phase.deliverables),
        "gate_checkpoint": phase.gate_checkpoint,
    }


def _program(program: EnterpriseProgram) -> dict[str, Any]:
    return {
        "service_id": program.service_id,
        "name_ar": program.name_ar,
        "name_en": program.name_en,
        "duration_days": program.duration_days,
        "phases": [_phase(p) for p in program.phases],
    }


def _readiness(report: ReadinessReport) -> dict[str, Any]:
    return {
        "service_id": report.service_id,
        "scores": report.scores._asdict(),
        "total": round(report.total, 1),
        "band": report.band.value,
        "sellable": report.sellable,
    }


def _offering(offering: ServiceOffering) -> dict[str, Any]:
    data = offering.model_dump()
    report = get_readiness(offering.id)
    data["readiness"] = _readiness(report) if report is not None else None
    data["sellable"] = bool(report and report.sellable)
    return data


@router.get("/status")
async def enterprise_status() -> dict[str, Any]:
    """Layer health, enterprise offering count, hard gates."""
    offerings = list_enterprise_offerings()
    return {
        "status": "ok",
        "governance_decision": "allow",
        "tier": "enterprise",
        "offerings_count": len(offerings),
        "service_ids": [o.id for o in offerings],
        "hard_gates": _HARD_GATES,
        "note": "Enterprise tier is Planned; not sellable until readiness gates pass.",
        "is_estimate": True,
    }


@router.get("/services")
async def enterprise_services() -> dict[str, Any]:
    """The 5 enterprise offerings in catalog display order."""
    offerings = list_enterprise_offerings()
    return {
        "governance_decision": "allow",
        "offerings": [_offering(o) for o in offerings],
        "count": len(offerings),
        "hard_gates": _HARD_GATES,
    }


@router.get("/program")
async def enterprise_program() -> dict[str, Any]:
    """The 90-day Enterprise AI Transformation Program phase structure."""
    return {
        "governance_decision": "allow",
        "program": _program(get_program()),
        "hard_gates": _HARD_GATES,
    }


@router.get("/readiness")
async def enterprise_readiness() -> dict[str, Any]:
    """Readiness scorecards for every enterprise service."""
    reports = list_readiness()
    return {
        "governance_decision": "allow",
        "readiness": [_readiness(r) for r in reports],
        "count": len(reports),
    }


@router.get("/services/{service_id}")
async def enterprise_service_detail(service_id: str) -> dict[str, Any]:
    """One enterprise offering by id, with its readiness scorecard."""
    offering = get_offering(service_id)
    if offering is None or offering.customer_journey_stage != "enterprise":
        raise HTTPException(
            status_code=404, detail=f"unknown_enterprise_service_id: {service_id}"
        )
    return {
        "governance_decision": "allow",
        "offering": _offering(offering),
        "hard_gates": _HARD_GATES,
    }
