"""Benchmark engine — Wave 14G."""
from __future__ import annotations

from auto_client_acquisition.benchmark_os import (
    aggregate_with_k_anonymity,
    generate_readiness_report,
    is_k_anonymous,
)


def test_k_anonymity_threshold():
    assert is_k_anonymous(contributor_count=5) is True
    assert is_k_anonymous(contributor_count=4) is False


def test_aggregate_suppresses_below_k():
    # Only 2 distinct contributors → suppressed.
    rows = [
        {"sector": "b2b", "score": 60, "customer_id": "a"},
        {"sector": "b2b", "score": 70, "customer_id": "b"},
    ]
    result = aggregate_with_k_anonymity(
        rows=rows, bucket_key="sector", value_key="score"
    )
    assert result["b2b"]["suppressed"] is True


def test_aggregate_passes_with_5_plus_contributors():
    rows = [
        {"sector": "b2b", "score": 60, "customer_id": f"c{i}"} for i in range(6)
    ]
    result = aggregate_with_k_anonymity(
        rows=rows, bucket_key="sector", value_key="score"
    )
    assert result["b2b"]["suppressed"] is False
    assert result["b2b"]["mean"] == 60.0
    assert result["b2b"]["contributors"] == 6


def test_generate_readiness_report_without_rows():
    report = generate_readiness_report()
    assert report.title == "Saudi AI Operations Readiness Report v1"
    assert report.k_anonymity_threshold == 5
    assert report.governance_decision == "allow_with_review"
    assert report.methodology
    assert len(report.limitations) >= 3


def test_generate_readiness_report_markdown_carries_disclaimer():
    report = generate_readiness_report()
    md = report.to_markdown()
    assert "SYNTHETIC + AGGREGATED" in md
    assert "Methodology" in md
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in md
