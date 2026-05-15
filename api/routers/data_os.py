"""Data OS router — public CSV upload + DQ score for the 1,500 SAR Data Pack.

POST /api/v1/data-os/import-preview
  Upload a small CSV (multipart form OR JSON with raw_csv string) and get a
  preview + Data Quality Score back. Tenant-scoped via customer_handle in
  body. No PII retained beyond the response.

The Data Quality Score is a 0-100 composite derived from the deterministic
`import_preview_csv` metrics (completeness + duplicate-inverse) plus a small
source-clarity modifier driven by the Source Passport.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from auto_client_acquisition.data_os.import_preview import import_preview_csv
from auto_client_acquisition.data_os.source_passport import (
    SourcePassport,
    source_passport_valid_for_ai,
)
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    governance_decision_from_passport_ai_gate,
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
            allowed_use=frozenset(raw.get("allowed_use", ("internal_analysis",))),
            contains_pii=bool(raw.get("contains_pii", False)),
            sensitivity=str(raw.get("sensitivity", "medium")),
            retention_policy=str(raw.get("retention_policy", "project_duration")),
            ai_access_allowed=bool(raw.get("ai_access_allowed", True)),
            external_use_allowed=bool(raw.get("external_use_allowed", False)),
        )
    except Exception:  # noqa: BLE001
        return None


def _dq_score(quality: dict[str, Any], *, source_clarity: float) -> dict[str, float]:
    """Composite 0-100 DQ score: 60% completeness, 30% duplicate-inverse,
    5% format consistency, 5% source clarity."""
    completeness = round(float(quality.get("mean_completeness", 0.0)) * 100.0, 2)
    dup_ratio = float(quality.get("duplicate_ratio_company_name", 0.0))
    duplicate_inverse = round(max(0.0, 1.0 - dup_ratio) * 100.0, 2)
    format_consistency = 100.0  # neutral — deterministic parser already normalised
    overall = round(
        completeness * 0.60
        + duplicate_inverse * 0.30
        + format_consistency * 0.05
        + source_clarity * 0.05,
        2,
    )
    return {
        "overall": max(0.0, min(100.0, overall)),
        "completeness": completeness,
        "duplicate_inverse": duplicate_inverse,
        "format_consistency": format_consistency,
        "source_clarity": round(source_clarity, 2),
    }


def _governance(passport: SourcePassport | None) -> tuple[GovernanceDecision, list[str]]:
    if passport is None:
        return GovernanceDecision.BLOCK, ["no_source_passport_provided"]
    ok, errors = source_passport_valid_for_ai(passport)
    return governance_decision_from_passport_ai_gate(ok, errors), list(errors)


@router.post("/import-preview")
async def import_preview(body: _RawCSVBody) -> dict[str, Any]:
    """Inline CSV (JSON body). Easier to call from internal scripts."""
    if len(body.raw_csv.encode("utf-8")) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="csv exceeds 5MB cap")

    passport = _build_passport(body.passport)
    passport_ok, passport_errors = (
        source_passport_valid_for_ai(passport) if passport else (False, ())
    )

    preview = import_preview_csv(body.raw_csv)
    if isinstance(preview, dict) and preview.get("error"):
        raise HTTPException(status_code=400, detail=str(preview["error"]))

    quality = preview.get("data_quality", {})
    source_clarity = 100.0 if passport_ok else (50.0 if passport else 0.0)
    dq = _dq_score(quality, source_clarity=source_clarity)
    decision, reasons = _governance(passport)
    decision_value = decision.value.lower()  # machine-stable, lowercase vocabulary

    return {
        "customer_handle": body.customer_handle,
        "preview": {
            "columns": list(preview.get("detected_columns", [])),
            "row_count": int(preview.get("parsed_row_count", 0)),
            "preview_rows": preview.get("preview_rows", []),
        },
        "data_quality_score": dq,
        "source_passport": {
            "provided": passport is not None,
            "valid": bool(passport is not None and passport_ok),
            "reasons": list(passport_errors),
        },
        "governance_decision": decision_value,
        "governance": {"decision": decision_value, "reasons": reasons},
        "is_estimate": True,
        "next_step_recommendation": _next_step(dq["overall"], decision),
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


def _next_step(dq_overall: float, decision: GovernanceDecision) -> str:
    if decision == GovernanceDecision.BLOCK:
        return "block_until_source_passport_provided"
    if dq_overall < 50:
        return "data_cleanup_required_before_scoring"
    if dq_overall < 75:
        return "proceed_with_caveats_recommended_data_pack_1500_sar"
    return "data_is_score_ready_recommend_revenue_sprint_499_sar"
