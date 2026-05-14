"""Deterministic validation rules for account-style rows."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.data_os.schemas import RowValidationResult


def validate_account_row(row: dict[str, Any], row_index: int) -> RowValidationResult:
    issues: list[str] = []
    if not str(row.get("company_name", "")).strip():
        issues.append("missing_company_name")
    src = str(row.get("source", "")).strip()
    if not src:
        issues.append("missing_source")
    return RowValidationResult(row_index=row_index, ok=not issues, issues=issues)


def validate_rows(rows: list[dict[str, Any]]) -> list[RowValidationResult]:
    return [validate_account_row(r, i) for i, r in enumerate(rows)]
