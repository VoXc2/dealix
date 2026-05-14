"""Canonical Benchmark OS — Wave 5 seed (14G).

Aggregation + anonymization + report generation for Saudi-AI-Operations-
Readiness benchmarks. SYNTHETIC + AGGREGATED data only — no real client
metrics. K-anonymity ≥ 5. Methodology disclosed.
"""
from auto_client_acquisition.benchmark_os.anonymization import (
    aggregate_with_k_anonymity,
    is_k_anonymous,
)
from auto_client_acquisition.benchmark_os.report_generator import (
    BenchmarkReport,
    generate_readiness_report,
)

__all__ = [
    "BenchmarkReport",
    "aggregate_with_k_anonymity",
    "generate_readiness_report",
    "is_k_anonymous",
]
