"""Lightweight typed shapes for Data OS (import paths, previews, flags)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PIIFlag:
    """Heuristic PII flag on a row or column."""

    field: str
    reason: str


@dataclass
class RowValidationResult:
    row_index: int
    ok: bool
    issues: list[str] = field(default_factory=list)


@dataclass
class DataQualityReport:
    row_count: int
    mean_completeness: float
    duplicate_ratio: float
    source_coverage: float | None = None


@dataclass
class UploadedDataset:
    """Logical dataset after preview (not necessarily persisted)."""

    detected_columns: list[str]
    preview_rows: list[dict[str, Any]]
    quality: dict[str, Any]
