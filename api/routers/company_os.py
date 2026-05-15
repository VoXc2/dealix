"""Company OS router — read-only spine of the AI Company Operating System.

Surfaces the 7 internal systems, their maturity, the 4-phase roadmap,
the doctrine map, plus the agent-factory templates, eval taxonomy, and
transformation stages. All GET, all return ``governance_decision``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from auto_client_acquisition.agent_factory import (
    list_templates,
    validate_all,
)
from auto_client_acquisition.company_os import (
    doctrine_coverage,
    get_system,
    maturity_report,
    registry_digest,
    roadmap_digest,
)
from auto_client_acquisition.eval_os import EvalCategory, list_metrics
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.transformation_os import (
    ALLOWED_TRANSITIONS,
    STAGE_TO_OFFER,
    TransformationStage,
)

router = APIRouter(prefix="/api/v1/company-os", tags=["company-os"])

_ALLOW = GovernanceDecision.ALLOW.value


@router.get("/systems")
async def get_systems() -> dict[str, Any]:
    """The 7 internal systems Dealix runs on."""
    digest = registry_digest()
    return {**digest, "governance_decision": _ALLOW}


@router.get("/systems/{system_id}")
async def get_one_system(system_id: str) -> dict[str, Any]:
    """One internal system by id."""
    try:
        system = get_system(system_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"system": system.to_dict(), "governance_decision": _ALLOW}


@router.get("/maturity")
async def get_maturity() -> dict[str, Any]:
    """Maturity scores for all 7 systems."""
    return {**maturity_report(), "governance_decision": _ALLOW}


@router.get("/roadmap")
async def get_roadmap(
    paid_pilots: int = Query(0, ge=0, description="Paid pilots delivered to date"),
) -> dict[str, Any]:
    """The 4-phase roadmap; phases 3-4 stay deferred until 3 paid pilots."""
    return {**roadmap_digest(paid_pilots=paid_pilots), "governance_decision": _ALLOW}


@router.get("/doctrine")
async def get_doctrine() -> dict[str, Any]:
    """The 11 non-negotiables mapped to the systems that enforce them."""
    return {**doctrine_coverage(), "governance_decision": _ALLOW}


@router.get("/agent-factory/templates")
async def get_agent_templates() -> dict[str, Any]:
    """The agent-factory templates and their doctrine-validation status."""
    violations = validate_all()
    return {
        "templates": [t.to_dict() for t in list_templates()],
        "validation": violations,
        "all_valid": all(not v for v in violations.values()),
        "governance_decision": _ALLOW,
    }


@router.get("/eval/metrics")
async def get_eval_metrics() -> dict[str, Any]:
    """The 4-category evaluation taxonomy."""
    metrics = list_metrics()
    return {
        "categories": [str(c) for c in EvalCategory],
        "metric_count": len(metrics),
        "metrics": [m.to_dict() for m in metrics],
        "governance_decision": _ALLOW,
    }


@router.get("/transformation/stages")
async def get_transformation_stages() -> dict[str, Any]:
    """The 5 transformation stages and their offer-ladder mapping."""
    stages = [
        {
            "stage": stage.value,
            "offer": STAGE_TO_OFFER[stage],
            "next_stages": list(ALLOWED_TRANSITIONS.get(stage.value, ())),
        }
        for stage in TransformationStage
    ]
    return {"stages": stages, "governance_decision": _ALLOW}
