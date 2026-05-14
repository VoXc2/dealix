"""Benchmark OS — safe market reports."""

from __future__ import annotations

from auto_client_acquisition.benchmark_os.benchmark_engine import (
    METHODOLOGY_VERSION,
    anonymize_label,
    benchmark_report_skeleton,
    methodology_footer,
)

__all__ = [
    "METHODOLOGY_VERSION",
    "anonymize_label",
    "benchmark_report_skeleton",
    "methodology_footer",
]
