"""Benchmark candidates — safe publication gates (delegates methodology checks)."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.benchmark_engine import benchmark_methodology_ok

BENCHMARK_CANDIDATE_SLUGS: tuple[str, ...] = (
    "saudi_b2b_revenue_readiness_benchmark",
    "saudi_sme_data_readiness_report",
    "ai_governance_gap_report",
    "arabic_ai_output_quality_report",
    "company_brain_readiness_benchmark",
)


def benchmark_candidate_eligible(
    *,
    occurrences: int,
    no_client_identifiers: bool,
    no_pii: bool,
    methodology_disclosed: bool,
    limitations_stated: bool,
) -> tuple[bool, tuple[str, ...]]:
    ok, errs = benchmark_methodology_ok(
        no_client_identifiers=no_client_identifiers,
        no_pii=no_pii,
        methodology_disclosed=methodology_disclosed,
        limitations_stated=limitations_stated,
    )
    if occurrences < 6:
        return False, errs + ("pattern_confidence_below_high",)
    return ok, errs
