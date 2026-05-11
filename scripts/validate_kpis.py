#!/usr/bin/env python3
"""Validate KPI tree coverage for all sellable services."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_kpi_tree, load_pricing_model


def main() -> int:
    tree = load_kpi_tree()
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

    if errors:
        print("KPI_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("KPI_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
