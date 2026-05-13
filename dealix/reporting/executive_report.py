"""Executive Report — bilingual PDF-shaped report consumed by every sprint.

تقرير تنفيذي ثنائي اللغة (هيكل JSON قابل للتحويل إلى PDF).
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class KPIRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label_ar: str
    label_en: str
    baseline: str
    after: str
    delta: str


class ExecutiveReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_id: str = Field(default_factory=lambda: f"rep_{uuid4().hex[:12]}")
    project_id: str
    title_ar: str
    title_en: str
    summary_ar: str
    summary_en: str
    kpis: list[KPIRow]
    findings_ar: list[str]
    findings_en: list[str]
    recommendations_ar: list[str]
    recommendations_en: list[str]
    next_steps_ar: list[str]
    next_steps_en: list[str]
    quality_score: int | None = None
    proof_pack_ref: str | None = None
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def build_executive_report(
    project_id: str,
    title_ar: str,
    title_en: str,
    summary_ar: str,
    summary_en: str,
    kpis: list[KPIRow],
    findings: tuple[list[str], list[str]],
    recommendations: tuple[list[str], list[str]],
    next_steps: tuple[list[str], list[str]],
    *,
    quality_score: int | None = None,
    proof_pack_ref: str | None = None,
) -> ExecutiveReport:
    f_ar, f_en = findings
    r_ar, r_en = recommendations
    n_ar, n_en = next_steps
    return ExecutiveReport(
        project_id=project_id,
        title_ar=title_ar,
        title_en=title_en,
        summary_ar=summary_ar,
        summary_en=summary_en,
        kpis=list(kpis),
        findings_ar=list(f_ar),
        findings_en=list(f_en),
        recommendations_ar=list(r_ar),
        recommendations_en=list(r_en),
        next_steps_ar=list(n_ar),
        next_steps_en=list(n_en),
        quality_score=quality_score,
        proof_pack_ref=proof_pack_ref,
    )
