"""KPI tree accessors."""

from __future__ import annotations

from typing import Any

from .catalog import (
    load_benchmark_targets,
    load_executive_metrics,
    load_guardrail_metrics,
    load_kpi_tree,
    load_north_star_metrics,
    load_operational_metrics,
)
from .pricing import parse_service_id


def kpis_for_service(service_id: str) -> dict[str, Any]:
    engine, _tier = parse_service_id(service_id)
    tree = load_kpi_tree()
    if engine in tree:
        return tree[engine]

    # Fallback composition using split KPI files.
    north_star = load_north_star_metrics().get(engine)
    executive = load_executive_metrics().get(engine)
    operational = load_operational_metrics().get(engine)
    guardrails = load_guardrail_metrics().get(engine)
    targets = load_benchmark_targets().get(engine)

    if not all([north_star, executive, operational, guardrails, targets]):
        raise ValueError(f"KPI definitions missing for engine: {engine}")

    return {
        "north_star": north_star,
        "business_kpis": executive,
        "operational_kpis": operational,
        "guardrail_kpis": guardrails,
        "target_benchmarks": targets,
    }
