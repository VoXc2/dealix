"""Benchmark engine — safe, anonymized market intelligence outputs."""

from __future__ import annotations

BENCHMARK_ARTIFACT_SLUGS: tuple[str, ...] = (
    "saudi_b2b_revenue_readiness_benchmark",
    "saudi_sme_data_readiness_report",
    "ai_governance_gap_report",
    "company_brain_readiness_benchmark",
    "arabic_ai_output_quality_report",
)

BENCHMARK_SAFE_SOURCE_KINDS: tuple[str, ...] = (
    "anonymized_client_patterns",
    "aggregated_proof_metrics",
    "open_public_data",
    "survey_responses",
    "partner_insights",
)

BENCHMARK_PORTAL_SIGNALS: tuple[str, ...] = (
    "public_reports",
    "sector_readiness",
    "anonymous_insights",
    "downloadable_checklists",
)


def benchmark_portal_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not BENCHMARK_PORTAL_SIGNALS:
        return 0
    n = sum(1 for s in BENCHMARK_PORTAL_SIGNALS if s in signals_tracked)
    return (n * 100) // len(BENCHMARK_PORTAL_SIGNALS)


def benchmark_methodology_ok(
    *,
    no_client_identifiers: bool,
    no_pii: bool,
    methodology_disclosed: bool,
    limitations_stated: bool,
) -> tuple[bool, tuple[str, ...]]:
    errs: list[str] = []
    if not no_client_identifiers:
        errs.append("client_identifiers_forbidden")
    if not no_pii:
        errs.append("pii_forbidden")
    if not methodology_disclosed:
        errs.append("methodology_required")
    if not limitations_stated:
        errs.append("limitations_required")
    return not errs, tuple(errs)
