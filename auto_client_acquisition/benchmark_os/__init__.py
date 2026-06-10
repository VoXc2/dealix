"""Benchmark OS — safe market reports."""

from __future__ import annotations

from auto_client_acquisition.benchmark_os.anonymization import (
    K_ANONYMITY_THRESHOLD,
    aggregate_with_k_anonymity,
    is_k_anonymous,
)
from auto_client_acquisition.benchmark_os.benchmark_engine import (
    METHODOLOGY_VERSION,
    anonymize_label,
    benchmark_report_skeleton,
    methodology_footer,
)
from auto_client_acquisition.benchmark_os.report_generator import (
    ReadinessReport,
    generate_readiness_report,
)

__all__ = [
    "K_ANONYMITY_THRESHOLD",
    "METHODOLOGY_VERSION",
    "ReadinessReport",
    "aggregate_with_k_anonymity",
    "anonymize_label",
    "benchmark_report_skeleton",
    "generate_readiness_report",
    "is_k_anonymous",
    "methodology_footer",
]
