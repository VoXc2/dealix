#!/usr/bin/env python3
"""Validate cross-layer catalog coherence for sellable services."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import (
    load_kpi_tree,
    load_playbook_catalog,
    load_pricing_model,
    load_risk_register,
)


def main() -> int:
    pricing = load_pricing_model()
    kpis = load_kpi_tree()
    playbooks = load_playbook_catalog()
    risks = load_risk_register()
    errors: list[str] = []

    for engine in pricing["service_matrix"].keys():
        if engine not in kpis:
            errors.append(f"{engine}: missing KPI definition")
        if engine not in playbooks:
            errors.append(f"{engine}: missing playbook definition")
        if engine not in risks:
            errors.append(f"{engine}: missing risk register")

    if errors:
        print("CATALOG_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("CATALOG_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
