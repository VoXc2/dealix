"""Enterprise Nervous System router.

Turns strategic transformation into measurable organizational capability.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.agentic_operations_os import (
    ASSESSMENT_SYSTEMS_COUNT,
    CORE_SYSTEM_IDS,
    CORE_SYSTEMS,
    CRITICAL_GOVERNANCE_SYSTEMS,
    DEFAULT_TARGET_SCORE,
    TARGET_SYSTEMS_COUNT_DEFAULT,
    assess_enterprise_nervous_system,
    unknown_system_ids,
)

router = APIRouter(prefix="/api/v1/agentic-enterprise", tags=["agentic-enterprise"])

_HARD_GATES = {
    "external_actions_are_draft_or_approval_first": True,
    "no_cold_whatsapp_automation": True,
    "no_linkedin_dm_automation": True,
    "auditability_required": True,
    "policy_compliance_required": True,
}


class MaturityAssessmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_scores: dict[str, float] = Field(
        ...,
        description="Map of system_id -> score(0..100). Missing systems default to 0.",
    )
    target_score: float = Field(default=DEFAULT_TARGET_SCORE, ge=50.0, le=100.0)
    target_systems_count: int = Field(
        default=TARGET_SYSTEMS_COUNT_DEFAULT,
        ge=ASSESSMENT_SYSTEMS_COUNT,
        le=50,
        description="Program target count. Dealix strategic target is 20.",
    )


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "agentic_enterprise",
        "model": "enterprise_nervous_system",
        "systems_assessed": ASSESSMENT_SYSTEMS_COUNT,
        "systems_target_default": TARGET_SYSTEMS_COUNT_DEFAULT,
        "critical_governance_systems": sorted(CRITICAL_GOVERNANCE_SYSTEMS),
        "hard_gates": _HARD_GATES,
    }


@router.get("/framework")
async def framework() -> dict[str, Any]:
    return {
        "model": "enterprise_nervous_system",
        "phase": "phase_1_of_20_systems",
        "systems_assessed": ASSESSMENT_SYSTEMS_COUNT,
        "systems_target_default": TARGET_SYSTEMS_COUNT_DEFAULT,
        "core_system_ids": sorted(CORE_SYSTEM_IDS),
        "critical_governance_systems": sorted(CRITICAL_GOVERNANCE_SYSTEMS),
        "systems": [
            {
                "system_id": item.system_id,
                "name_en": item.name_en,
                "name_ar": item.name_ar,
                "intent_en": item.intent_en,
                "weight": item.weight,
            }
            for item in CORE_SYSTEMS
        ],
        "hard_gates": _HARD_GATES,
    }


@router.post("/maturity-assessment")
async def maturity_assessment(body: MaturityAssessmentRequest) -> dict[str, Any]:
    bad_ids = unknown_system_ids(body.system_scores)
    if bad_ids:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "unknown_system_ids",
                "unknown_system_ids": list(bad_ids),
                "allowed_system_ids": sorted(CORE_SYSTEM_IDS),
            },
        )

    assessment = assess_enterprise_nervous_system(
        system_scores=body.system_scores,
        target_score=body.target_score,
        target_systems_count=body.target_systems_count,
    )

    return {
        "overall_score": assessment.overall_score,
        "maturity_band": assessment.maturity_band,
        "governed_autonomy_ready": assessment.governed_autonomy_ready,
        "target_score": assessment.target_score,
        "assessed_systems_count": assessment.assessed_systems_count,
        "target_systems_count": assessment.target_systems_count,
        "architecture_coverage_percent": assessment.architecture_coverage_percent,
        "weakest_systems": list(assessment.weakest_systems),
        "prioritized_next_moves_ar": list(assessment.prioritized_next_moves_ar),
        "systems": [
            {
                "system_id": row.system_id,
                "name_en": row.name_en,
                "name_ar": row.name_ar,
                "score": row.score,
                "weight": row.weight,
                "weighted_score": row.weighted_score,
                "level": row.level,
                "gap_to_target": row.gap_to_target,
                "next_move_ar": row.next_move_ar,
            }
            for row in assessment.systems
        ],
        "hard_gates": _HARD_GATES,
    }
