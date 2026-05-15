#!/usr/bin/env python3
"""Validate KPI tree coverage for all sellable services."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import (
    load_benchmark_targets,
    load_executive_metrics,
    load_guardrail_metrics,
    load_kpi_tree,
    load_north_star_metrics,
    load_operational_metrics,
    load_pricing_model,
)


def main() -> int:
    tree = load_kpi_tree()
    north = load_north_star_metrics()
    operational = load_operational_metrics()
    executive = load_executive_metrics()
    guardrails = load_guardrail_metrics()
    benchmarks = load_benchmark_targets()
    pricing = load_pricing_model()
    errors: list[str] = []

    for engine in pricing["service_matrix"].keys():
        cfg = tree.get(engine)
        if not cfg:
            errors.append(f"missing kpi engine: {engine}")
            continue
        for key in (
            "north_star",
            "business_kpis",
            "operational_kpis",
            "guardrail_kpis",
            "target_benchmarks",
        ):
            if key not in cfg:
                errors.append(f"{engine}: missing key {key}")
        if engine not in north:
            errors.append(f"{engine}: missing north_star_metrics entry")
        if engine not in operational:
            errors.append(f"{engine}: missing operational_metrics entry")
        if engine not in executive:
            errors.append(f"{engine}: missing executive_metrics entry")
        if engine not in guardrails:
            errors.append(f"{engine}: missing guardrails entry")
        if engine not in benchmarks:
            errors.append(f"{engine}: missing benchmark_targets entry")

    if errors:
        print("KPI_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("KPI_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
