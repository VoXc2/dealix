"""Reports router — Reporting OS public API.

موجِّه التقارير — API نظام Reporting.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from dealix.reporting import (
    ExecutiveReport,
    ProofPack,
    WeeklySummary,
    build_executive_report,
    build_proof_pack,
    build_weekly_summary,
)
from dealix.reporting.executive_report import KPIRow
from dealix.reporting.proof_pack import ProofMetric


router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


class ExecutiveReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: str
    title_ar: str
    title_en: str
    summary_ar: str
    summary_en: str
    kpis: list[KPIRow]
    findings_ar: list[str] = []
    findings_en: list[str] = []
    recommendations_ar: list[str] = []
    recommendations_en: list[str] = []
    next_steps_ar: list[str] = []
    next_steps_en: list[str] = []
    quality_score: int | None = None
    proof_pack_ref: str | None = None


@router.post("/executive", response_model=None)
async def executive(req: ExecutiveReportRequest) -> dict[str, Any]:
    """Build an executive report. Caller is responsible for persistence/PDF render."""
    try:
        report: ExecutiveReport = build_executive_report(
            project_id=req.project_id,
            title_ar=req.title_ar,
            title_en=req.title_en,
            summary_ar=req.summary_ar,
            summary_en=req.summary_en,
            kpis=req.kpis,
            findings=(req.findings_ar, req.findings_en),
            recommendations=(req.recommendations_ar, req.recommendations_en),
            next_steps=(req.next_steps_ar, req.next_steps_en),
            quality_score=req.quality_score,
            proof_pack_ref=req.proof_pack_ref,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return report.to_dict()


class ProofPackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: str
    customer_codename: str
    vertical: str
    headline_ar: str
    headline_en: str
    metrics: list[ProofMetric]
    customer_quote_ar: str | None = None
    customer_quote_en: str | None = None
    artifacts_links: list[str] = []


@router.post("/proof-pack", response_model=None)
async def proof_pack(req: ProofPackRequest) -> dict[str, Any]:
    """Build a proof pack."""
    pack: ProofPack = build_proof_pack(
        project_id=req.project_id,
        customer_codename=req.customer_codename,
        vertical=req.vertical,
        headline_ar=req.headline_ar,
        headline_en=req.headline_en,
        metrics=req.metrics,
        customer_quote_ar=req.customer_quote_ar,
        customer_quote_en=req.customer_quote_en,
        artifacts_links=req.artifacts_links,
    )
    return pack.to_dict()


class WeeklySummaryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    week_starts: str | None = None
    pipeline_value_sar: float | None = None
    retainer_mrr_sar: float | None = None
    quality_score_avg: int | None = None
    risks_ar: list[str] = []
    risks_en: list[str] = []


@router.post("/weekly", response_model=None)
async def weekly(req: WeeklySummaryRequest) -> dict[str, Any]:
    """Build a weekly summary (Founder Command Center digest)."""
    summary: WeeklySummary = build_weekly_summary(
        pipeline_value_sar=req.pipeline_value_sar,
        retainer_mrr_sar=req.retainer_mrr_sar,
        quality_score_avg=req.quality_score_avg,
        risks=(req.risks_ar, req.risks_en),
    )
    return summary.to_dict()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"reporting_os": "ok"}
