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
    compute_enterprise_nervous_system,
    default_system_scores,
    executive_scorecard_template,
    systems_blueprint,
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


@router.post("/assess")
async def assess(request: AssessRequest) -> dict[str, Any]:
    score_map = {item.system_id: item.score for item in request.system_scores}
    assessment = compute_enterprise_nervous_system(score_map)
    return {
        "module": "enterprise_nervous_system",
        "assessment": assessment,
    }
