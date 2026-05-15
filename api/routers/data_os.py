"""Data OS router — public CSV upload + DQ score for the 1,500 SAR Data Pack.

POST /api/v1/data-os/import-preview
  Upload a small CSV (multipart form OR JSON with raw_csv string) and get a
  preview + Data Quality Score back. Tenant-scoped via X-Tenant header /
  customer_handle in body. No PII retained beyond the response.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from auto_client_acquisition.data_os.data_quality_score import compute_dq
from auto_client_acquisition.data_os.import_preview import preview as preview_csv
from auto_client_acquisition.data_os.source_passport import (
    SourcePassport,
    validate as validate_passport,
)
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)

router = APIRouter(prefix="/api/v1/data-os", tags=["data-os"])


_MAX_BYTES = 5 * 1024 * 1024  # 5 MB hard cap on uploads (anti-abuse)


class _RawCSVBody(BaseModel):
    customer_handle: str = Field(..., min_length=1)
    raw_csv: str = Field(..., min_length=1)
    passport: dict[str, Any] | None = None  # optional inline Source Passport


def _build_passport(raw: dict[str, Any] | None) -> SourcePassport | None:
    if not raw:
        return None
    try:
        return SourcePassport(
            source_id=str(raw.get("source_id", "")),
            source_type=str(raw.get("source_type", "client_upload")),
            owner=str(raw.get("owner", "client")),
            allowed_use=tuple(raw.get("allowed_use", ("internal_analysis",))),
            contains_pii=bool(raw.get("contains_pii", False)),
            sensitivity=str(raw.get("sensitivity", "medium")),
            ai_access_allowed=bool(raw.get("ai_access_allowed", True)),
            external_use_allowed=bool(raw.get("external_use_allowed", False)),
            retention_policy=str(raw.get("retention_policy", "project_duration")),
        )
    except Exception:  # noqa: BLE001
        return None


def _governance_envelope(*, passport: SourcePassport | None) -> dict[str, Any]:
    result = decide(
        action="run_scoring",
        context={
            "source_passport": passport,
            "contains_pii": passport.contains_pii if passport else False,
            "external_use": passport.external_use_allowed if passport else False,
        },
    )
    return {
        "decision": result.decision.value,
        "reasons": list(result.reasons),
        "safe_alternative": result.safe_alternative,
    }


@router.post("/import-preview")
async def import_preview(body: _RawCSVBody) -> dict[str, Any]:
    """Inline CSV (JSON body). Easier to call from internal scripts."""
    if len(body.raw_csv.encode("utf-8")) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="csv exceeds 5MB cap")

    passport = _build_passport(body.passport)
    passport_validation = validate_passport(passport) if passport else None

    preview = preview_csv(body.raw_csv.encode("utf-8"))
    dq = compute_dq(
        preview=preview,
        duplicates_found=0,
        source_passport=passport,
    )
    envelope = _governance_envelope(passport=passport)
    return {
        "customer_handle": body.customer_handle,
        "preview": {
            "columns": list(preview.columns),
            "row_count": preview.row_count,
            "missing_pct": dict(preview.missing_pct),
            "pii_columns": list(preview.pii_columns),
            "suggested_cleanup": list(preview.suggested_cleanup),
        },
        "data_quality_score": {
            "overall": dq.overall,
            "completeness": dq.completeness,
            "duplicate_inverse": dq.duplicate_inverse,
            "format_consistency": dq.format_consistency,
            "source_clarity": dq.source_clarity,
        },
        "source_passport": {
            "provided": passport is not None,
            "valid": bool(passport_validation and passport_validation.is_valid),
            "reasons": list(passport_validation.reasons) if passport_validation else [],
        },
        "governance_decision": envelope["decision"],
        "governance": envelope,
        "is_estimate": True,
        "next_step_recommendation": _next_step(dq.overall, envelope["decision"]),
    }


@router.post("/import-preview/upload")
async def import_preview_upload(
    customer_handle: str = Form(...),
    file: UploadFile = File(...),
) -> dict[str, Any]:
    """Multipart CSV upload — used by `landing/services.html` form widget."""
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty file")
    if len(raw) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="csv exceeds 5MB cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="file must be UTF-8 CSV")

    body = _RawCSVBody(customer_handle=customer_handle, raw_csv=text)
    return await import_preview(body)


def _next_step(dq_overall: float, decision: str) -> str:
    normalized = decision.strip().lower()
    if normalized in {GovernanceDecision.BLOCK.value.lower(), "deny", "block"}:
        return "block_until_source_passport_provided"
    if dq_overall < 50:
        return "data_cleanup_required_before_scoring"
    if dq_overall < 75:
        return "proceed_with_caveats_recommended_data_pack_1500_sar"
    return "data_is_score_ready_recommend_revenue_sprint_499_sar"
