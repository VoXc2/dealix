"""Benchmark report skeleton (deterministic)."""

from __future__ import annotations


def benchmark_report_skeleton(*, title: str) -> dict[str, str]:
    return {
        "title": title,
        "methodology": "aggregated_anonymized",
        "limitations": "not_individual_advice",
        "body": "",
    }


__all__ = ["benchmark_report_skeleton"]
