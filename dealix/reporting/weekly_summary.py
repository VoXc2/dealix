"""Weekly Summary — Founder Command Center weekly digest.

ملخّص أسبوعي لمركز قيادة المؤسس — أولوية واحدة كل يوم لمدة 5 أيام.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class FocusItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    day_iso: str
    headline_ar: str
    headline_en: str
    action_ar: str
    action_en: str
    expected_outcome_ar: str
    expected_outcome_en: str


class WeeklySummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary_id: str = Field(default_factory=lambda: f"week_{uuid4().hex[:12]}")
    week_starts: str
    focuses: list[FocusItem]
    pipeline_value_sar: float | None = None
    retainer_mrr_sar: float | None = None
    quality_score_avg: int | None = None
    risks_ar: list[str] = Field(default_factory=list)
    risks_en: list[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def build_weekly_summary(
    week_start: datetime | None = None,
    *,
    focuses: list[FocusItem] | None = None,
    pipeline_value_sar: float | None = None,
    retainer_mrr_sar: float | None = None,
    quality_score_avg: int | None = None,
    risks: tuple[list[str], list[str]] | None = None,
) -> WeeklySummary:
    start = (week_start or datetime.now(UTC)).date()
    if focuses is None:
        focuses = []
    if risks is None:
        risks_ar: list[str] = []
        risks_en: list[str] = []
    else:
        risks_ar, risks_en = risks
    if not focuses:
        focuses = [
            FocusItem(
                day_iso=(start + timedelta(days=i)).isoformat(),
                headline_ar="—",
                headline_en="—",
                action_ar="—",
                action_en="—",
                expected_outcome_ar="—",
                expected_outcome_en="—",
            )
            for i in range(5)
        ]
    return WeeklySummary(
        week_starts=start.isoformat(),
        focuses=list(focuses),
        pipeline_value_sar=pipeline_value_sar,
        retainer_mrr_sar=retainer_mrr_sar,
        quality_score_avg=quality_score_avg,
        risks_ar=list(risks_ar),
        risks_en=list(risks_en),
    )
