"""Answer grounding score API (initiative 175)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/v1/intelligence", tags=["intelligence"])


class GroundingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str
    source_refs: list[str] = Field(default_factory=list)


@router.post("/grounding-score")
def post_grounding_score(body: GroundingRequest) -> dict:
    refs = [r.strip() for r in body.source_refs if r.strip()]
    ratio = min(1.0, len(refs) / 3.0) if refs else 0.0
    has_citation = "[" in body.answer or "source:" in body.answer.lower()
    score = min(100.0, ratio * 70 + (30.0 if has_citation else 0.0))
    return {
        "grounding_score": round(score, 1),
        "source_ref_count": len(refs),
        "recommendation_ar": "أضف مراجع مصدر" if score < 60 else "مقبول للمراجعة",
    }
