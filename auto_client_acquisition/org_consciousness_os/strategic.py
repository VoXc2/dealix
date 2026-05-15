"""System 44 — Strategic Organizational Engine.

Benchmarks one customer's execution health against a cohort. The cohort
is supplied by the caller (the router decides which customers it is
authorized to include) — this function never reads other tenants' stores.
"""

from __future__ import annotations

from auto_client_acquisition.org_consciousness_os.schemas import (
    ExecutionHealthSignal,
    StrategicBenchmark,
    StrategicIntelligenceReport,
)

# metric name -> (signal attribute, higher_is_better)
_METRICS: tuple[tuple[str, str, bool], ...] = (
    ("execution_health_score", "execution_health_score", True),
    ("friction_total", "friction_total", False),
    ("friction_cost_minutes", "friction_cost_minutes", False),
    ("avg_latency_ms", "avg_latency_ms", False),
)


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _percentile_rank(value: float, population: list[float]) -> int:
    """Percent of the population at or below ``value`` (0-100)."""
    if not population:
        return 0
    at_or_below = sum(1 for v in population if v <= value)
    return int((at_or_below / len(population)) * 100)


def benchmark_customer(
    *,
    customer_id: str,
    cohort_signals: dict[str, ExecutionHealthSignal],
) -> StrategicIntelligenceReport:
    """Benchmark ``customer_id`` against ``cohort_signals``.

    ``cohort_signals`` must include ``customer_id`` itself.
    """
    if customer_id not in cohort_signals:
        raise ValueError("cohort_signals must include the benchmarked customer_id")

    benchmarks: list[StrategicBenchmark] = []
    for metric_name, attr, higher_is_better in _METRICS:
        population = [float(getattr(sig, attr)) for sig in cohort_signals.values()]
        customer_value = float(getattr(cohort_signals[customer_id], attr))
        median = _median(population)
        percentile = _percentile_rank(customer_value, population)

        # direction is performance vs cohort: ahead / behind / at_median.
        if customer_value > median:
            direction = "ahead" if higher_is_better else "behind"
        elif customer_value < median:
            direction = "behind" if higher_is_better else "ahead"
        else:
            direction = "at_median"

        benchmarks.append(
            StrategicBenchmark(
                metric=metric_name,
                customer_value=round(customer_value, 3),
                cohort_median=round(median, 3),
                percentile=percentile,
                direction=direction,
            )
        )

    return StrategicIntelligenceReport(
        customer_id=customer_id,
        cohort_size=len(cohort_signals),
        benchmarks=tuple(benchmarks),
    )


__all__ = ["benchmark_customer"]
