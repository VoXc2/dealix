"""Data OS — table quality metrics."""

from __future__ import annotations

from auto_client_acquisition.data_os import (
    duplicate_ratio_by_field,
    mean_completeness,
    summarize_table_quality,
)


def test_mean_completeness() -> None:
    rows = [
        {"company_name": "A", "sector": "x", "city": "y"},
        {"company_name": "", "sector": "x", "city": ""},
    ]
    mc = mean_completeness(rows, ("company_name", "sector", "city"))
    assert 0.4 < mc < 0.9


def test_duplicate_ratio() -> None:
    rows = [
        {"company_name": "Acme"},
        {"company_name": "acme"},
        {"company_name": "Other"},
    ]
    assert duplicate_ratio_by_field(rows, "company_name") > 0.0


def test_summarize_table_quality_keys() -> None:
    s = summarize_table_quality([{"company_name": "Z", "sector": "s", "city": "c"}])
    assert set(s.keys()) == {"row_count", "mean_completeness", "duplicate_ratio_company_name"}
