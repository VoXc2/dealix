"""Benchmark Engine — typed benchmark report shape with anonymization rules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkReport:
    benchmark_id: str
    title: str
    sector: str
    period: str
    sources_used: tuple[str, ...]
    methodology_appendix: str
    limitations: str
    anonymized: bool
    aggregated_only: bool
    contains_pii: bool

    def __post_init__(self) -> None:
        if self.contains_pii:
            raise ValueError("benchmarks_cannot_contain_pii")
        if not self.anonymized:
            raise ValueError("benchmarks_must_be_anonymized")
        if not self.aggregated_only:
            raise ValueError("benchmarks_must_be_aggregated_only")
        if not self.methodology_appendix:
            raise ValueError("benchmarks_require_methodology_appendix")
        if not self.limitations:
            raise ValueError("benchmarks_require_stated_limitations")
