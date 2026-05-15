"""Institutional Dependency Index — Layer 46 measurement endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.institutional_dependency_os import (
    InstitutionalDependencyDimensions,
    dependency_band,
    dependency_blockers,
    institutional_dependency_index,
)

router = APIRouter(
    prefix="/api/v1/institutional-dependency",
    tags=["institutional-dependency"],
)

_DIMENSION_FIELDS: tuple[str, ...] = (
    "control_plane_coverage",
    "agent_society_governed",
    "assurance_contract_coverage",
    "memory_fabric_traceability",
    "org_reasoning_depth",
    "resilience_recovery",
    "meta_governance_improvement",
    "value_measurability",
    "learning_loop_active",
    "operating_core_reliance",
)


@router.get("/status")
async def status() -> dict:
    return {
        "module": "institutional_dependency_os",
        "layer": "46_institutional_operating_core",
        "measures": "institutional dependency, not agent count",
        "dimensions": list(_DIMENSION_FIELDS),
        "bands": ["tool", "platform", "infrastructure", "institutional_operating_core"],
    }


@router.post("/index")
async def compute_index(payload: dict = Body(...)) -> dict:
    """Compute the dependency index from ten 0–100 system signals."""
    try:
        values = {field: int(payload[field]) for field in _DIMENSION_FIELDS}
    except KeyError as exc:
        raise HTTPException(status_code=422, detail=f"missing dimension: {exc.args[0]}") from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422, detail=f"dimension values must be integers: {exc}"
        ) from exc

    dimensions = InstitutionalDependencyDimensions(**values)
    score = institutional_dependency_index(dimensions)
    blockers = dependency_blockers(dimensions)
    return {
        "score": score,
        "band": dependency_band(score),
        "blockers": list(blockers),
        "operating_core": not blockers and dependency_band(score) == "institutional_operating_core",
    }
