"""Anonymous benchmark catalog for market authority (no client data)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BenchmarkSpec:
    benchmark_id: str
    title_en: str
    safe_defaults: str = "anonymized_aggregated_permission_aware"


BENCHMARK_REGISTRY: tuple[BenchmarkSpec, ...] = (
    BenchmarkSpec("saudi_b2b_data_readiness", "Saudi B2B Services Data Readiness Benchmark"),
    BenchmarkSpec("saudi_sme_ai_ops_readiness", "Saudi SME AI Operations Readiness Report"),
    BenchmarkSpec("revenue_intelligence", "Revenue Intelligence Benchmark"),
    BenchmarkSpec("company_brain_readiness", "Company Brain Readiness Benchmark"),
    BenchmarkSpec("ai_governance_gap", "AI Governance Gap Report"),
)


def get_benchmark(benchmark_id: str) -> BenchmarkSpec | None:
    for b in BENCHMARK_REGISTRY:
        if b.benchmark_id == benchmark_id:
            return b
    return None


def list_benchmark_ids() -> tuple[str, ...]:
    return tuple(b.benchmark_id for b in BENCHMARK_REGISTRY)
