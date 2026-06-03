"""Benchmark engine safety checklist."""

from __future__ import annotations

BENCHMARK_SAFE_RULES: tuple[str, ...] = (
    "anonymized",
    "aggregated",
    "no_pii",
    "no_client_confidential",
    "permission_aware",
)


def benchmark_publish_ok(checklist: dict[str, bool]) -> bool:
    """Return True only when every required rule is explicitly True."""
    unknown = set(checklist) - set(BENCHMARK_SAFE_RULES)
    if unknown:
        raise ValueError(f"Unknown benchmark rules: {sorted(unknown)}")
    return all(checklist.get(rule, False) for rule in BENCHMARK_SAFE_RULES)
