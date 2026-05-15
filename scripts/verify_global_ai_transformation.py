#!/usr/bin/env python3
"""Verify global AI transformation program artifacts and core modules."""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path


TODO_IDS = (
    "doctrine-lock",
    "gap-closure",
    "enterprise-package",
    "governance-expansion",
    "data-flywheel",
    "reliability-program",
    "observability-contracts",
    "gtm-system",
    "unit-economics",
    "delivery-control-tower",
    "org-operating-system",
    "category-dominance",
)

DOC_FILES = (
    "docs/transformation/README.md",
    "docs/transformation/01_doctrine_lock.md",
    "docs/transformation/02_gap_closure_matrix.md",
    "docs/transformation/03_enterprise_package.md",
    "docs/transformation/04_governance_expansion.md",
    "docs/transformation/05_data_flywheel_operationalization.md",
    "docs/transformation/06_reliability_program.md",
    "docs/transformation/07_observability_contracts.md",
    "docs/transformation/08_gtm_system_playbook.md",
    "docs/transformation/09_unit_economics_governance.md",
    "docs/transformation/10_delivery_control_tower.md",
    "docs/transformation/11_org_operating_system.md",
    "docs/transformation/12_category_dominance.md",
)

ENTERPRISE_PACKAGE_FILES = (
    "docs/transformation/enterprise_package/pilot_scope_template.md",
    "docs/transformation/enterprise_package/trust_compliance_pack_template.md",
    "docs/transformation/enterprise_package/procurement_response_kit_template.md",
    "docs/transformation/enterprise_package/roi_realization_narrative_template.md",
)

CONTROL_ARTIFACTS = (
    "dealix/transformation/todo_registry.yaml",
    "dealix/transformation/kpi_registry.yaml",
    "dealix/transformation/ownership_matrix.yaml",
    "dealix/transformation/risk_register.yaml",
)

MODULE_IMPORTS = (
    "auto_client_acquisition.governance_os.workflow_control_registry",
    "auto_client_acquisition.revenue_os.data_flywheel",
    "auto_client_acquisition.reliability_os.mission_critical_program",
    "auto_client_acquisition.observability_v10.contract_registry",
    "auto_client_acquisition.operating_finance_os.lifecycle_unit_economics",
    "auto_client_acquisition.delivery_os.control_tower",
)


def _extract_todo_ids(text: str) -> tuple[str, ...]:
    ids = re.findall(r"^\\s*-\\s+id:\\s*([a-z0-9\\-]+)\\s*$", text, flags=re.MULTILINE)
    return tuple(ids)


def _require_paths(repo: Path, paths: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for rel in paths:
        if not (repo / rel).exists():
            missing.append(rel)
    return missing


def _check_todo_registry(repo: Path) -> list[str]:
    registry = repo / "dealix/transformation/todo_registry.yaml"
    if not registry.exists():
        return ["dealix/transformation/todo_registry.yaml"]
    text = registry.read_text(encoding="utf-8")
    found_ids = set(_extract_todo_ids(text))
    missing_ids = [todo_id for todo_id in TODO_IDS if todo_id not in found_ids]
    return [f"missing_todo_id:{todo_id}" for todo_id in missing_ids]


def _check_module_imports() -> list[str]:
    failures: list[str] = []
    for module_name in MODULE_IMPORTS:
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"import_failed:{module_name}:{type(exc).__name__}")
    return failures


def _check_jsonl_migration_policy(repo: Path) -> list[str]:
    report = repo / "docs/reports/enterprise_control_plane_hardening_report.md"
    if not report.exists():
        return ["missing_hardening_report"]
    text = report.read_text(encoding="utf-8")
    if "JSONL" not in text and "jsonl" not in text:
        return ["jsonl_policy_not_documented"]
    return []


def _check_observability_contracts(repo: Path) -> list[str]:
    path = repo / "docs/transformation/07_observability_contracts.md"
    if not path.exists():
        return ["missing_observability_contract_doc"]
    text = path.read_text(encoding="utf-8")
    required_tokens = ("tenant_id", "correlation_id", "run_id", "event_type")
    missing = [token for token in required_tokens if token not in text]
    return [f"missing_observability_token:{token}" for token in missing]


def _check_enterprise_package(repo: Path) -> list[str]:
    missing = _require_paths(repo, ENTERPRISE_PACKAGE_FILES)
    return [f"missing_enterprise_package_file:{path}" for path in missing]


def _check_reliability(repo: Path) -> list[str]:
    doc = repo / "docs/transformation/06_reliability_program.md"
    if not doc.exists():
        return ["missing_reliability_program_doc"]
    text = doc.read_text(encoding="utf-8")
    required = ("drill", "SLO", "rollback", "kill-switch")
    return [f"missing_reliability_token:{token}" for token in required if token not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", default="", help="Check one todo id only")
    parser.add_argument("--check-jsonl", action="store_true")
    parser.add_argument("--check-observability", action="store_true")
    parser.add_argument("--check-enterprise-package", action="store_true")
    parser.add_argument("--check-reliability", action="store_true")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    checks = {
        "doctrine-lock": lambda: _require_paths(repo, ("docs/transformation/01_doctrine_lock.md",)),
        "gap-closure": lambda: _require_paths(repo, ("docs/transformation/02_gap_closure_matrix.md",)),
        "enterprise-package": lambda: _check_enterprise_package(repo),
        "governance-expansion": lambda: _require_paths(repo, ("docs/transformation/04_governance_expansion.md",)),
        "data-flywheel": lambda: _require_paths(repo, ("docs/transformation/05_data_flywheel_operationalization.md",)),
        "reliability-program": lambda: _check_reliability(repo),
        "observability-contracts": lambda: _check_observability_contracts(repo),
        "gtm-system": lambda: _require_paths(repo, ("docs/transformation/08_gtm_system_playbook.md",)),
        "unit-economics": lambda: _require_paths(repo, ("docs/transformation/09_unit_economics_governance.md",)),
        "delivery-control-tower": lambda: _require_paths(repo, ("docs/transformation/10_delivery_control_tower.md",)),
        "org-operating-system": lambda: _require_paths(repo, ("docs/transformation/11_org_operating_system.md",)),
        "category-dominance": lambda: _require_paths(repo, ("docs/transformation/12_category_dominance.md",)),
    }

    if args.check:
        if args.check not in checks:
            print(f"Unknown check id: {args.check}", file=sys.stderr)
            return 2
        failures.extend(checks[args.check]())
    elif args.check_jsonl:
        failures.extend(_check_jsonl_migration_policy(repo))
    elif args.check_observability:
        failures.extend(_check_observability_contracts(repo))
    elif args.check_enterprise_package:
        failures.extend(_check_enterprise_package(repo))
    elif args.check_reliability:
        failures.extend(_check_reliability(repo))
    else:
        failures.extend(_require_paths(repo, DOC_FILES))
        failures.extend(_require_paths(repo, CONTROL_ARTIFACTS))
        failures.extend(_check_todo_registry(repo))
        failures.extend(_check_module_imports())

    if failures:
        print("GLOBAL AI TRANSFORMATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("GLOBAL AI TRANSFORMATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
