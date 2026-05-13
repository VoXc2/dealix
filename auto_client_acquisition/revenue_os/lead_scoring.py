"""Lead Scoring — explainable A/B/C/D banding for Saudi B2B accounts.

تقييم العملاء المحتملين بشكل قابل للتفسير (A/B/C/D) للسوق السعودي.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ScoreBand(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ScoreFeature(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    weight: float
    raw: float
    contribution: float
    rationale_ar: str
    rationale_en: str


class LeadScore(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    score: float = Field(ge=0.0, le=100.0)
    band: ScoreBand
    features: list[ScoreFeature]
    why_now_ar: str
    why_now_en: str

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _band_from_score(score: float) -> ScoreBand:
    if score >= 80:
        return ScoreBand.A
    if score >= 60:
        return ScoreBand.B
    if score >= 40:
        return ScoreBand.C
    return ScoreBand.D


def _trigger_score(triggers: list[str]) -> tuple[float, str, str]:
    weight_map = {
        "tender": 30,
        "funding": 25,
        "hire": 20,
        "cr_amendment": 15,
        "vision2030": 15,
        "dpo_appointment": 10,
        "expansion": 12,
    }
    score = sum(weight_map.get(t, 0) for t in triggers)
    return (
        min(score, 30),
        f"محفّزات شراء عالية ({', '.join(triggers)})." if triggers else "لا محفّزات نشطة.",
        f"High-intent buying triggers ({', '.join(triggers)})." if triggers else "No active triggers.",
    )


def _vertical_fit(vertical: str | None) -> tuple[float, str, str]:
    high_fit = {"bfsi", "retail_ecomm", "healthcare", "logistics"}
    if vertical in high_fit:
        return 20, "قطاع ضمن الأولويات الثلاث.", "Vertical is in top-3 priority list."
    return 10, "قطاع غير أولوية في المرحلة الحالية.", "Vertical is outside the current priority list."


def _size_fit(headcount: int | None, revenue: float | None) -> tuple[float, str, str]:
    if headcount is None and revenue is None:
        return 8, "حجم غير معروف — تقدير محايد.", "Size unknown — neutral estimate."
    if (headcount or 0) >= 200 or (revenue or 0) >= 200_000_000:
        return 25, "مؤسسة كبرى (Tier 1).", "Tier-1 enterprise."
    if (headcount or 0) >= 50 or (revenue or 0) >= 30_000_000:
        return 18, "سوق متوسط.", "Mid-market."
    return 10, "منشأة صغيرة.", "SME tier."


def _data_quality_fit(quality_score: int | None) -> tuple[float, str, str]:
    if quality_score is None:
        return 6, "جودة بيانات غير محسوبة.", "Data quality not computed."
    if quality_score >= 80:
        return 15, "بيانات نظيفة وموثوقة.", "Clean, trusted data."
    if quality_score >= 60:
        return 10, "بيانات مقبولة، تحتاج تحسين طفيف.", "Acceptable data, minor cleanup needed."
    return 5, "بيانات ضعيفة، تحتاج تنظيف قبل الاستهداف.", "Poor data; cleanup required before targeting."


def score_account(record: dict[str, Any]) -> LeadScore:
    """Score one account dict; produces an explainable A/B/C/D banding."""
    triggers = record.get("triggers") or []
    if isinstance(triggers, str):
        triggers = [triggers]
    trig_pts, trig_ar, trig_en = _trigger_score(list(triggers))
    vert_pts, vert_ar, vert_en = _vertical_fit(record.get("vertical"))
    size_pts, size_ar, size_en = _size_fit(record.get("headcount"), record.get("annual_revenue_sar"))
    dq_pts, dq_ar, dq_en = _data_quality_fit(record.get("data_quality_score"))

    features = [
        ScoreFeature(
            name="trigger",
            weight=0.30,
            raw=trig_pts,
            contribution=trig_pts,
            rationale_ar=trig_ar,
            rationale_en=trig_en,
        ),
        ScoreFeature(
            name="vertical_fit",
            weight=0.20,
            raw=vert_pts,
            contribution=vert_pts,
            rationale_ar=vert_ar,
            rationale_en=vert_en,
        ),
        ScoreFeature(
            name="size_fit",
            weight=0.25,
            raw=size_pts,
            contribution=size_pts,
            rationale_ar=size_ar,
            rationale_en=size_en,
        ),
        ScoreFeature(
            name="data_quality_fit",
            weight=0.15,
            raw=dq_pts,
            contribution=dq_pts,
            rationale_ar=dq_ar,
            rationale_en=dq_en,
        ),
    ]
    total = sum(f.contribution for f in features) + 10  # base 10
    total = min(100.0, max(0.0, total))

    primary_trigger = (triggers or ["—"])[0]
    why_now_ar = (
        f"محفّز '{primary_trigger}' نشط الآن مع توافق قطاعي وحجمي." if triggers
        else "لا محفّز قوي حاليًا — انتظر إشارة شراء قبل الاستهداف."
    )
    why_now_en = (
        f"Trigger '{primary_trigger}' active alongside vertical and size fit." if triggers
        else "No strong trigger now — wait for a buying signal before targeting."
    )

    return LeadScore(
        score=total,
        band=_band_from_score(total),
        features=features,
        why_now_ar=why_now_ar,
        why_now_en=why_now_en,
    )


def rank_top_k(records: list[dict[str, Any]], k: int = 50) -> list[tuple[dict[str, Any], LeadScore]]:
    """Rank accounts by score and return top-k as (record, score) tuples."""
    scored = [(r, score_account(r)) for r in records]
    scored.sort(key=lambda x: x[1].score, reverse=True)
    return scored[:k]
