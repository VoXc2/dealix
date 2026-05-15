"""Enterprise Maturity router — score Dealix itself against the maturity model.

Read-only platform self-assessment: the 5 maturity stages, 10 readiness gates,
5 verification systems, and an honest current-state assessment.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.enterprise_maturity_os.maturity_assessment import (
    assess_current_platform,
    assess_platform_maturity,
)
from auto_client_acquisition.enterprise_maturity_os.readiness_gates import (
    GATE_CRITERIA,
    readiness_band,
)
from auto_client_acquisition.enterprise_maturity_os.stages import STAGES
from auto_client_acquisition.enterprise_maturity_os.verification_systems import (
    VERIFICATION_SYSTEMS,
)

router = APIRouter(prefix="/api/v1/maturity", tags=["enterprise-maturity"])

_BANDS: list[dict[str, Any]] = [
    {"band": "prototype", "min": 0, "max": 59},
    {"band": "internal_beta", "min": 60, "max": 74},
    {"band": "client_pilot", "min": 75, "max": 84},
    {"band": "enterprise_ready", "min": 85, "max": 94},
    {"band": "mission_critical", "min": 95, "max": 100},
]


class AssessBody(BaseModel):
    gate_evidence: dict[str, dict[str, bool]] = Field(default_factory=dict)
    verification_evidence: dict[str, dict[str, bool]] = Field(default_factory=dict)


@router.get("/stages")
async def get_stages() -> dict[str, Any]:
    return {
        "stages": [
            {
                "stage_id": s.stage_id,
                "level": s.level,
                "name_en": s.name_en,
                "name_ar": s.name_ar,
                "description_ar": s.description_ar,
                "entry_signals": list(s.entry_signals),
            }
            for s in STAGES
        ]
    }


@router.get("/gates")
async def get_gates() -> dict[str, Any]:
    return {
        "bands": _BANDS,
        "gates": [
            {"gate_id": gate_id, "criteria": criteria}
            for gate_id, criteria in GATE_CRITERIA.items()
        ],
    }


@router.get("/verification-systems")
async def get_verification_systems() -> dict[str, Any]:
    return {
        "verification_systems": [
            {
                "system_id": v.system_id,
                "name_en": v.name_en,
                "name_ar": v.name_ar,
                "checks": list(v.checks),
            }
            for v in VERIFICATION_SYSTEMS
        ]
    }


@router.post("/assess")
async def post_assess(body: AssessBody) -> dict[str, Any]:
    assessment = assess_platform_maturity(
        gate_evidence=body.gate_evidence,
        verification_evidence=body.verification_evidence,
    )
    return assessment.to_dict()


@router.get("/current")
async def get_current() -> dict[str, Any]:
    """Dealix's maturity today, scored against the packaged honest baseline."""
    assessment = assess_current_platform()
    result = assessment.to_dict()
    result["gate_bands"] = {
        gate_id: readiness_band(score) for gate_id, score in assessment.gate_scores.items()
    }
    return result
