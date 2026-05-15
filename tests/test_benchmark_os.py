"""Benchmark OS — anonymization, methodology tag, report skeleton."""
from __future__ import annotations

from auto_client_acquisition.benchmark_os import (
    METHODOLOGY_VERSION,
    anonymize_label,
    benchmark_report_skeleton,
    methodology_footer,
)


def test_methodology_version_is_stable():
    assert METHODOLOGY_VERSION == "dealix-benchmark-0.1"


def test_anonymize_label_is_deterministic_and_pii_free():
    a = anonymize_label("Real Saudi Corp")
    b = anonymize_label("Real Saudi Corp")
    assert a == b
    assert "real" not in a.lower()
    assert len(a) == 10


def test_anonymize_label_distinguishes_inputs():
    assert anonymize_label("Company A") != anonymize_label("Company B")


def test_anonymize_label_handles_empty():
    assert anonymize_label("   ") == "unknown"


def test_methodology_footer_mentions_version_and_limitations():
    footer = methodology_footer()
    assert METHODOLOGY_VERSION in footer
    assert "limitations" in footer.lower()


def test_benchmark_report_skeleton_shape():
    skeleton = benchmark_report_skeleton(title="Saudi B2B Readiness")
    assert skeleton["title"] == "Saudi B2B Readiness"
    assert skeleton["methodology"] == "aggregated_anonymized"
    assert "limitations" in skeleton
