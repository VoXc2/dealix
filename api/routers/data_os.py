"""Data OS router — public CSV upload + Data Quality Score for the Data Pack offer.

POST /api/v1/data-os/import-preview
  Upload a small CSV (multipart form OR JSON with a raw_csv string) and get
  a structural preview + a 0–100 Data Quality Score back. An optional inline
  Source Passport drives the governance decision. No PII is retained beyond
  the response.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.data_os.data_quality_score import compute_dq
from auto_client_acquisition.data_os.import_preview import import_preview_csv
from auto_client_acquisition.data_os.pii_detection import column_name_suggests_pii
from auto_client_acquisition.data_os.source_passport import SourcePassport
from auto_client_acquisition.governance_os.runtime_decision import (
    governance_decision_from_passport_ai_gate,
)
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    source_passport_valid_for_ai,
)

router = APIRouter(prefix="/api/v1/data-os", tags=["data-os"])

_MAX_BYTES = 5 * 1024 * 1024  # 5 MB hard cap on uploads (anti-abuse)
_REQUIRED_KEYS: tuple[str, ...] = ("company_name", "sector", "city")


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
    except Exception:  # noqa: BLE001 — malformed inline passport is non-fatal
        return None


def _passport_block(
    passport: SourcePassport | None,
) -> tuple[dict[str, Any], GovernanceDecision]:
    """Validate the passport and derive the governance decision.

    With no passport the preview is still allowed, but flagged for review.
    """
    if passport is None:
        return (
            {"provided": False, "valid": False, "reasons": []},
            GovernanceDecision.ALLOW_WITH_REVIEW,
        )
    ok, errors = source_passport_valid_for_ai(passport)
    decision = governance_decision_from_passport_ai_gate(ok, errors)
    return (
        {"provided": True, "valid": ok, "reasons": list(errors)},
        decision,
    )


def _missing_pct(rows: list[dict[str, Any]], columns: list[str]) -> dict[str, float]:
    if not rows:
        return {c: 0.0 for c in columns}
    out: dict[str, float] = {}
    for c in columns:
        missing = sum(1 for r in rows if not str(r.get(c, "")).strip())
        out[c] = round(missing / len(rows) * 100, 1)
    return out


def _suggested_cleanup(
    rows: list[dict[str, Any]],
    columns: list[str],
    missing_pct: dict[str, float],
) -> list[str]:
    hints: list[str] = []
    for col, pct in missing_pct.items():
        if pct > 0:
            hints.append(f"fill_missing:{col}")
    if "company_name" in columns and "source" not in columns:
        hints.append("add_source_column_for_provenance")
    return hints


def _next_step(dq_overall: float, decision: GovernanceDecision) -> str:
    if decision == GovernanceDecision.BLOCK:
        return "block_until_source_passport_provided"
    if dq_overall < 50:
        return "data_cleanup_required_before_scoring"
    if dq_overall < 75:
        return "proceed_with_caveats_recommended_data_pack_1500_sar"
    return "data_is_score_ready_recommend_revenue_sprint_499_sar"


@router.post("/import-preview")
async def import_preview(body: _RawCSVBody) -> dict[str, Any]:
    """Inline CSV (JSON body) — preview + Data Quality Score + governance."""
    if len(body.raw_csv.encode("utf-8")) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="csv exceeds 5MB cap")

    parsed = import_preview_csv(body.raw_csv)
    if "error" in parsed:
        raise HTTPException(status_code=400, detail=str(parsed["error"]))

    columns = list(parsed.get("detected_columns", []))
    rows = list(parsed.get("preview_rows", []))
    row_count = int(parsed.get("parsed_row_count", len(rows)))

    passport = _build_passport(body.passport)
    passport_block, decision = _passport_block(passport)

    dq = compute_dq(
        rows,
        columns=columns,
        has_valid_passport=passport_block["valid"],
        required_keys=_REQUIRED_KEYS,
    )
    missing_pct = _missing_pct(rows, columns)

    return {
        "customer_handle": body.customer_handle,
        "preview": {
            "columns": columns,
            "row_count": row_count,
            "missing_pct": missing_pct,
            "pii_columns": [c for c in columns if column_name_suggests_pii(c)],
            "suggested_cleanup": _suggested_cleanup(rows, columns, missing_pct),
        },
        "data_quality_score": {
            "overall": dq.overall,
            "completeness": dq.completeness,
            "duplicate_inverse": dq.duplicate_inverse,
            "format_consistency": dq.format_consistency,
            "source_clarity": dq.source_clarity,
        },
        "source_passport": passport_block,
        "governance_decision": decision.value.lower(),
        "is_estimate": True,
        "next_step_recommendation": _next_step(dq.overall, decision),
    }


@router.post("/import-preview/upload")
async def import_preview_upload(
    customer_handle: str = Form(...),
    file: UploadFile = File(...),
) -> dict[str, Any]:
    """Multipart CSV upload — used by the `landing/services.html` form widget."""
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty file")
    if len(raw) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="csv exceeds 5MB cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400, detail="file must be UTF-8 CSV",
        ) from exc

    return await import_preview(_RawCSVBody(customer_handle=customer_handle, raw_csv=text))
