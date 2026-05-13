"""Data Quality Score — Data OS aggregate 0–100 score for a record batch.

درجة جودة البيانات (0–100) لمجموعة سجلات.

Inputs are weighted across:
  completeness · validity · uniqueness · freshness · pii_risk · source_attribution
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.customer_data_plane.validation_rules import (
    validate_record,
)


class QualityBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")
    completeness: int = Field(ge=0, le=25)
    validity: int = Field(ge=0, le=25)
    uniqueness: int = Field(ge=0, le=15)
    freshness: int = Field(ge=0, le=15)
    pii_safety: int = Field(ge=0, le=10)
    source_attribution: int = Field(ge=0, le=10)

    @property
    def total(self) -> int:
        return (
            self.completeness
            + self.validity
            + self.uniqueness
            + self.freshness
            + self.pii_safety
            + self.source_attribution
        )


class QualityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: int
    breakdown: QualityBreakdown
    record_count: int
    invalid_count: int
    duplicate_count: int
    missing_field_counts: dict[str, int]
    has_pii: bool
    sources_attributed: bool
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


_EXPECTED_FIELDS: tuple[str, ...] = (
    "company_name_ar",
    "commercial_registration",
    "vertical",
    "region",
    "email",
    "phone",
    "contact_name",
)


def _completeness(records: list[dict[str, Any]]) -> tuple[int, dict[str, int]]:
    if not records:
        return 0, {f: 0 for f in _EXPECTED_FIELDS}
    counts = {f: 0 for f in _EXPECTED_FIELDS}
    for r in records:
        for f in _EXPECTED_FIELDS:
            if r.get(f) in (None, ""):
                counts[f] += 1
    total_slots = len(records) * len(_EXPECTED_FIELDS)
    missing_slots = sum(counts.values())
    pct = 1.0 - (missing_slots / total_slots) if total_slots else 0.0
    return int(round(pct * 25)), counts


def _validity(records: list[dict[str, Any]]) -> tuple[int, int]:
    if not records:
        return 0, 0
    invalid = sum(1 for r in records if not validate_record(r).valid)
    pct = 1.0 - (invalid / len(records))
    return int(round(pct * 25)), invalid


def _uniqueness(records: list[dict[str, Any]]) -> tuple[int, int]:
    if not records:
        return 0, 0
    seen: set[str] = set()
    dupes = 0
    for r in records:
        key = (
            str(r.get("commercial_registration") or "")
            or str(r.get("vat_number") or "")
            or str(r.get("domain") or "")
            or str(r.get("email") or "")
        )
        if not key:
            continue
        if key in seen:
            dupes += 1
        else:
            seen.add(key)
    pct = 1.0 - (dupes / max(len(records), 1))
    return int(round(pct * 15)), dupes


def _freshness(records: list[dict[str, Any]]) -> int:
    if not records:
        return 0
    now = datetime.now(UTC)
    fresh_pct_sum = 0.0
    counted = 0
    for r in records:
        stamp = r.get("updated_at") or r.get("created_at")
        if not stamp:
            continue
        try:
            d = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        except ValueError:
            continue
        age_days = (now - d).days
        fresh_pct_sum += max(0.0, 1.0 - (age_days / 180.0))
        counted += 1
    if counted == 0:
        return 8  # neutral score when timestamps are absent
    avg = fresh_pct_sum / counted
    return int(round(avg * 15))


def _pii_safety(has_pii: bool, redacted: bool) -> int:
    if not has_pii:
        return 10
    return 10 if redacted else 4


def _source_attribution(records: list[dict[str, Any]]) -> tuple[int, bool]:
    if not records:
        return 0, False
    attributed = sum(1 for r in records if r.get("source"))
    pct = attributed / len(records)
    return int(round(pct * 10)), pct >= 0.9


def score_batch(
    records: Iterable[dict[str, Any]],
    *,
    has_pii: bool = False,
    redacted: bool = False,
) -> QualityReport:
    """Compute a 0–100 data quality score for a batch."""
    records = list(records)
    comp, missing = _completeness(records)
    val, invalid = _validity(records)
    uni, dupes = _uniqueness(records)
    fresh = _freshness(records)
    pii = _pii_safety(has_pii, redacted)
    src, src_ok = _source_attribution(records)

    breakdown = QualityBreakdown(
        completeness=comp,
        validity=val,
        uniqueness=uni,
        freshness=fresh,
        pii_safety=pii,
        source_attribution=src,
    )
    return QualityReport(
        score=breakdown.total,
        breakdown=breakdown,
        record_count=len(records),
        invalid_count=invalid,
        duplicate_count=dupes,
        missing_field_counts=missing,
        has_pii=has_pii,
        sources_attributed=src_ok,
    )
