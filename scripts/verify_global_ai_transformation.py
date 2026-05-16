#!/usr/bin/env python3
"""Global AI transformation verifier.

A thin aggregator — it does not introduce new verification logic. It asserts:

  1. Governance modules import cleanly (proof / value / governance /
     board-decision / decision-passport).
  2. `dealix/registers/kpi_baselines.yaml` is honest: every KPI with a
     non-null `value` MUST also have a non-null `source_ref`. A measured
     number without a source is a fabricated KPI and fails the gate.

Exit 0 = transformation surface verified. Exit 1 = at least one failure.

Usage:
    python3 scripts/verify_global_ai_transformation.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

GOVERNANCE_MODULES = [
    "auto_client_acquisition.proof_os",
    "auto_client_acquisition.value_os",
    "auto_client_acquisition.governance_os",
    "auto_client_acquisition.board_decision_os",
    "auto_client_acquisition.decision_passport",
]

KPI_REGISTER = _REPO / "dealix" / "registers" / "kpi_baselines.yaml"


def check_governance_modules() -> list[str]:
    failures: list[str] = []
    for module in GOVERNANCE_MODULES:
        try:
            importlib.import_module(module)
            print(f"  ok   import {module}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"import {module}: {exc!r}")
            print(f"  FAIL import {module}: {exc!r}")
    return failures


def check_kpi_honesty() -> list[str]:
    failures: list[str] = []
    if not KPI_REGISTER.exists():
        return [f"missing register: {KPI_REGISTER}"]
    try:
        import yaml
    except Exception as exc:  # noqa: BLE001
        return [f"pyyaml unavailable: {exc!r}"]

    data = yaml.safe_load(KPI_REGISTER.read_text(encoding="utf-8")) or {}
    kpis = data.get("kpis") or []
    for kpi in kpis:
        kid = kpi.get("id", "<unknown>")
        if kpi.get("value") is not None and not kpi.get("source_ref"):
            failures.append(f"KPI {kid}: has a value but no source_ref (fabricated)")
            print(f"  FAIL KPI {kid}: value set without source_ref")
        else:
            print(f"  ok   KPI {kid}")
    return failures


def main() -> int:
    print("== Governance modules ==")
    failures = check_governance_modules()
    print("== KPI baseline honesty ==")
    failures += check_kpi_honesty()

    if failures:
        print(f"\nFAIL — {len(failures)} issue(s):")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print("\nOK — global AI transformation surface verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
