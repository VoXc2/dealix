"""Enterprise Nervous System router.

API surface for operating blueprint, phased roadmap, and capability scoring
for Dealix as agentic-enterprise infrastructure.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.enterprise_os import (
    capability_roadmap,
    compute_cross_plane_health,
    compute_enterprise_nervous_system,
    compute_full_enterprise_assessment,
    default_health_signals,
    default_system_scores,
    dependency_graph_payload,
    executive_scorecard_template,
    layer_contracts_payload,
    systems_blueprint,
    validate_layer_stack,
)

router = APIRouter(
    prefix="/api/v1/enterprise-nervous-system",
    tags=["enterprise-nervous-system"],
)


class SystemScoreInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_id: str = Field(..., min_length=3)
    score: float = Field(..., ge=0, le=100)


class AssessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_scores: list[SystemScoreInput] = Field(..., min_length=1)


class StackValidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    implemented_system_ids: list[str] = Field(..., min_length=1)


class CrossPlaneHealthRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_compliance_rate: float = Field(70, ge=0, le=100)
    trace_coverage_rate: float = Field(70, ge=0, le=100)
    evaluation_coverage_rate: float = Field(65, ge=0, le=100)
    workflow_success_rate: float = Field(70, ge=0, le=100)
    exception_escalation_precision: float = Field(70, ge=0, le=100)
    memory_grounding_score: float = Field(70, ge=0, le=100)
    memory_freshness_hours: float = Field(48, ge=0, le=9999)
    incident_mtta_minutes: float = Field(120, ge=0, le=99999)


class FullAssessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_scores: list[SystemScoreInput] = Field(..., min_length=1)
    implemented_system_ids: list[str] = Field(..., min_length=1)
    health_signals: CrossPlaneHealthRequest = Field(
        default_factory=CrossPlaneHealthRequest
    )


@router.get("/blueprint")
async def blueprint() -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "blueprint": systems_blueprint(),
        "note_ar": "المحور: قياس القدرة المؤسسية وليس عدد الميزات.",
    }


@router.get("/roadmap")
async def roadmap() -> dict[str, Any]:
    baseline = default_system_scores()
    return {
        "module": "enterprise_nervous_system",
        "baseline_score": 50,
        "roadmap": capability_roadmap(baseline),
        "note_ar": "الطريق الافتراضي: تحكم ثم ذكاء ثم تنفيذ وتوسّع.",
    }


@router.get("/scorecard")
async def scorecard() -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "metrics": executive_scorecard_template(),
    }


@router.get("/layers/contracts")
async def layers_contracts() -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "contracts_total": len(layer_contracts_payload()),
        "contracts": layer_contracts_payload(),
    }


@router.get("/layers/dependencies")
async def layers_dependencies() -> dict[str, Any]:
    graph = dependency_graph_payload()
    return {
        "module": "enterprise_nervous_system",
        "graph": graph,
        "nodes_total": len(graph["nodes"]),
        "edges_total": len(graph["edges"]),
    }


@router.post("/layers/validate")
async def layers_validate(request: StackValidateRequest) -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "validation": validate_layer_stack(request.implemented_system_ids),
    }


@router.get("/health/defaults")
async def health_defaults() -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "defaults": default_health_signals(),
    }


@router.post("/health/cross-plane")
async def health_cross_plane(request: CrossPlaneHealthRequest) -> dict[str, Any]:
    return {
        "module": "enterprise_nervous_system",
        "health": compute_cross_plane_health(request.model_dump()),
    }


@router.post("/assess")
async def assess(request: AssessRequest) -> dict[str, Any]:
    score_map = {item.system_id: item.score for item in request.system_scores}
    assessment = compute_enterprise_nervous_system(score_map)
    return {
        "module": "enterprise_nervous_system",
        "assessment": assessment,
    }


@router.post("/assess/full")
async def assess_full(request: FullAssessRequest) -> dict[str, Any]:
    score_map = {item.system_id: item.score for item in request.system_scores}
    full = compute_full_enterprise_assessment(
        system_scores=score_map,
        implemented_system_ids=request.implemented_system_ids,
        health_signals=request.health_signals.model_dump(),
    )
    return {
        "module": "enterprise_nervous_system",
        "assessment": full,
    }
