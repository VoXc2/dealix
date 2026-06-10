"""Thin facade over ecosystem benchmark hooks."""

from __future__ import annotations

from auto_client_acquisition.benchmark_os.anonymization import anonymize_label
from auto_client_acquisition.benchmark_os.methodology import METHODOLOGY_VERSION, methodology_footer
from auto_client_acquisition.benchmark_os.report_generator import benchmark_report_skeleton

__all__ = [
    "METHODOLOGY_VERSION",
    "anonymize_label",
    "benchmark_report_skeleton",
    "methodology_footer",
]
