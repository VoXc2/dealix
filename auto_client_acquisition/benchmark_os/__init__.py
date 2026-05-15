"""Benchmark OS — safe market reports."""

from __future__ import annotations

from auto_client_acquisition.benchmark_os.benchmark_engine import (
    METHODOLOGY_VERSION,
    anonymize_label,
    benchmark_report_skeleton,
    methodology_footer,
)
from auto_client_acquisition.benchmark_os.k_anonymity import (
    aggregate_with_k_anonymity,
    is_k_anonymous,
)
from auto_client_acquisition.benchmark_os.readiness_report import (
    generate_readiness_report,
)

__all__ = [
    "METHODOLOGY_VERSION",
    "aggregate_with_k_anonymity",
    "anonymize_label",
    "benchmark_report_skeleton",
    "generate_readiness_report",
    "is_k_anonymous",
    "methodology_footer",
]
