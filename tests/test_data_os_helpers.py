"""Data OS — import preview and validation helpers."""

from __future__ import annotations

from auto_client_acquisition.data_os import (
    import_preview_csv,
    pii_flags_for_row,
    source_coverage_ratio,
    validate_rows,
)


def test_import_preview_csv() -> None:
    csv_text = "company_name,sector,city,source\nAcme,logistics,Riyadh,crm_export\n"
    out = import_preview_csv(csv_text)
    assert out.get("parsed_row_count") == 1
    assert "data_quality" in out


def test_validate_rows_flags_missing_source() -> None:
    rows = [{"company_name": "X", "sector": "s", "city": "c", "source": ""}]
    res = validate_rows(rows)
    assert res[0].ok is False
    assert "missing_source" in res[0].issues


def test_source_coverage_ratio() -> None:
    rows = [
        {"company_name": "A", "source": "crm"},
        {"company_name": "B", "source": ""},
    ]
    assert source_coverage_ratio(rows) == 0.5


def test_pii_flags_email() -> None:
    flags = pii_flags_for_row({"contact_email": "a@b.co", "company_name": "Z"})
    kinds = {f.reason for f in flags}
    assert "email_pattern" in kinds
