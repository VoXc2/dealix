#!/usr/bin/env python3
"""Verify global AI transformation program artifacts and core modules."""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

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
    "docs/transformation/ENGINEERING_CUTOVER_RUNBOOK_AR.md",
    "docs/transformation/EXECUTIVE_OPERATING_CHECKLIST_AR.md",
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
    "dealix/transformation/kpi_baselines.yaml",
    "dealix/transformation/ownership_matrix.yaml",
    "dealix/transformation/risk_register.yaml",
    "dealix/transformation/jsonl_migration_catalog.yaml",
    "dealix/transformation/reliability_drills.yaml",
    "dealix/transformation/category_expansion_gates.yaml",
    "dealix/transformation/ceo_signal_os.yaml",
    "dealix/transformation/engineering_cutover_policy.yaml",
)

ENTERPRISE_RUNBOOK_FILES = (
    "docs/transformation/enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md",
    "docs/transformation/enterprise_package/PILOT_REPEAT_CHECKLIST_AR.md",
)

MODULE_IMPORTS = (
    "auto_client_acquisition.governance_os.workflow_control_registry",
    "auto_client_acquisition.revenue_os.data_flywheel",
    "auto_client_acquisition.reliability_os.mission_critical_program",
    "auto_client_acquisition.observability_v10.contract_registry",
    "auto_client_acquisition.observability_v10.contract_trace_hook",
    "auto_client_acquisition.operating_finance_os.lifecycle_unit_economics",
    "auto_client_acquisition.delivery_os.control_tower",
    "dealix.execution.weekly_cross_os_snapshot",
    "auto_client_acquisition.persistence.db_sync_url",
    "auto_client_acquisition.persistence.operational_stream_mirror",
    "auto_client_acquisition.value_os.value_ledger_postgres",
)


def _extract_todo_ids(text: str) -> tuple[str, ...]:
    ids = re.findall(r"^\s*-\s+id:\s*([a-z0-9\-]+)\s*$", text, flags=re.MULTILINE)
    return tuple(ids)


def _require_paths(repo: Path, paths: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for rel in paths:
        if not (repo / rel).exists():
            missing.append(rel)
    return missing


def _load_yaml(repo: Path, rel: str) -> dict[str, Any]:
    path = repo / rel
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


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
        except Exception as exc:
            failures.append(f"import_failed:{module_name}:{type(exc).__name__}")
    return failures


def _check_jsonl_migration_policy(repo: Path) -> list[str]:
    failures: list[str] = []
    report = repo / "docs/reports/enterprise_control_plane_hardening_report.md"
    if not report.exists():
        failures.append("missing_hardening_report")
    else:
        text = report.read_text(encoding="utf-8")
        if "JSONL" not in text and "jsonl" not in text:
            failures.append("jsonl_policy_not_documented")

    catalog = _load_yaml(repo, "dealix/transformation/jsonl_migration_catalog.yaml")
    if not catalog.get("entries"):
        failures.append("jsonl_migration_catalog_missing_entries")
        return failures
    for entry in catalog["entries"]:
        eid = entry.get("id", "?")
        if entry.get("tier") is None:
            failures.append(f"jsonl_catalog_missing_tier:{eid}")
        if not entry.get("target_cutoff_iso"):
            failures.append(f"jsonl_catalog_missing_cutoff:{eid}")
    return failures


def _check_observability_contracts(repo: Path) -> list[str]:
    path = repo / "docs/transformation/07_observability_contracts.md"
    if not path.exists():
        return ["missing_observability_contract_doc"]
    text = path.read_text(encoding="utf-8")
    required_tokens = ("tenant_id", "correlation_id", "run_id", "event_type")
    missing = [token for token in required_tokens if token not in text]
    return [f"missing_observability_token:{token}" for token in missing]


def _check_enterprise_package(repo: Path) -> list[str]:
    failures = [f"missing_enterprise_package_file:{path}" for path in _require_paths(repo, ENTERPRISE_PACKAGE_FILES)]
    failures.extend([f"missing_enterprise_runbook:{path}" for path in _require_paths(repo, ENTERPRISE_RUNBOOK_FILES)])
    return failures


def _check_reliability(repo: Path) -> list[str]:
    failures: list[str] = []
    doc = repo / "docs/transformation/06_reliability_program.md"
    if not doc.exists():
        failures.append("missing_reliability_program_doc")
        return failures
    text = doc.read_text(encoding="utf-8")
    required = ("drill", "SLO", "rollback", "kill-switch")
    failures.extend([f"missing_reliability_token:{token}" for token in required if token not in text])

    drills_file = _load_yaml(repo, "dealix/transformation/reliability_drills.yaml")
    drills = drills_file.get("drills") or []
    if len(drills) < 3:
        failures.append("reliability_drills_yaml_insufficient")
    return failures


def _check_kpi_registry_evidence(repo: Path) -> list[str]:
    data = _load_yaml(repo, "dealix/transformation/kpi_registry.yaml")
    if int(data.get("version", 0)) < 2:
        return ["kpi_registry_version_must_be_2"]
    failures: list[str] = []
    buckets = data.get("kpis") or {}
    for bucket_name in ("north_star", "leading", "guardrails"):
        for row in buckets.get(bucket_name, []):
            key = row.get("key", "?")
            ev = row.get("evidence")
            if not isinstance(ev, dict):
                failures.append(f"kpi_missing_evidence:{key}")
                continue
            if not str(ev.get("primary_source", "")).strip():
                failures.append(f"kpi_missing_primary_source:{key}")
            fields = ev.get("weekly_proof_fields")
            if not isinstance(fields, list) or not fields:
                failures.append(f"kpi_missing_weekly_proof_fields:{key}")
    return failures


def _check_ownership_matrix_human_fields(repo: Path) -> list[str]:
    data = _load_yaml(repo, "dealix/transformation/ownership_matrix.yaml")
    if int(data.get("version", 0)) < 2:
        return ["ownership_matrix_version_must_be_2"]
    failures: list[str] = []
    for os_key, row in (data.get("os_ownership") or {}).items():
        if not isinstance(row, dict):
            failures.append(f"ownership_invalid_os:{os_key}")
            continue
        if "human_assignee_name" not in row:
            failures.append(f"ownership_missing_human_assignee_key:{os_key}")
        if "human_assignee_notes_ar" not in row:
            failures.append(f"ownership_missing_human_notes_key:{os_key}")
    return failures


def _check_category_expansion_gates(repo: Path) -> list[str]:
    data = _load_yaml(repo, "dealix/transformation/category_expansion_gates.yaml")
    gates = data.get("gates") or []
    if len(gates) < 3:
        return ["category_expansion_gates_insufficient"]
    failures: list[str] = []
    for gate in gates:
        gid = gate.get("id", "?")
        if not gate.get("metric_key"):
            failures.append(f"category_gate_missing_metric:{gid}")
        ver = gate.get("verification_commands")
        if not isinstance(ver, list) or not ver:
            failures.append(f"category_gate_missing_verification:{gid}")
    return failures


def _collect_kpi_keys(repo: Path) -> tuple[str, ...]:
    data = _load_yaml(repo, "dealix/transformation/kpi_registry.yaml")
    keys: list[str] = []
    buckets = data.get("kpis") or {}
    for bucket_name in ("north_star", "leading", "guardrails"):
        for row in buckets.get(bucket_name, []):
            key = row.get("key")
            if key:
                keys.append(str(key))
    return tuple(keys)


def _check_kpi_baselines(repo: Path) -> list[str]:
    base = _load_yaml(repo, "dealix/transformation/kpi_baselines.yaml")
    if not base.get("version"):
        return ["kpi_baselines_missing_version"]
    snaps = base.get("snapshots") or {}
    expected = set(_collect_kpi_keys(repo))
    got = set(snaps.keys())
    missing = sorted(expected - got)
    extra = sorted(got - expected)
    failures = [f"kpi_baselines_missing_key:{k}" for k in missing]
    failures.extend([f"kpi_baselines_unknown_key:{k}" for k in extra])
    return failures


def _check_ceo_signal_os(repo: Path) -> list[str]:
    data = _load_yaml(repo, "dealix/transformation/ceo_signal_os.yaml")
    events = data.get("external_events") or []
    if len(events) < 10:
        return ["ceo_signal_os_external_events_insufficient"]
    monthly = data.get("monthly_targets") or {}
    if int(monthly.get("partner_attempts_minimum", 0) or 0) < 1:
        return ["ceo_signal_os_monthly_partner_target_missing"]
    return []


def _check_engineering_cutover_policy(repo: Path) -> list[str]:
    data = _load_yaml(repo, "dealix/transformation/engineering_cutover_policy.yaml")
    sigs = data.get("minimum_signals_any_one") or []
    if len(sigs) < 2:
        return ["engineering_cutover_policy_signals_insufficient"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", default="", help="Check one todo id only")
    parser.add_argument("--check-jsonl", action="store_true")
    parser.add_argument("--check-observability", action="store_true")
    parser.add_argument("--check-enterprise-package", action="store_true")
    parser.add_argument("--check-reliability", action="store_true")
    parser.add_argument("--check-category-expansion", action="store_true")
    args = parser.parse_args()

    repo = _REPO_ROOT
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
    elif args.check_category_expansion:
        failures.extend(_check_category_expansion_gates(repo))
    else:
        failures.extend(_require_paths(repo, DOC_FILES))
        failures.extend(_require_paths(repo, CONTROL_ARTIFACTS))
        failures.extend(_check_todo_registry(repo))
        failures.extend(_check_module_imports())
        failures.extend(_check_kpi_registry_evidence(repo))
        failures.extend(_check_ownership_matrix_human_fields(repo))
        failures.extend(_check_jsonl_migration_policy(repo))
        failures.extend(_check_category_expansion_gates(repo))
        failures.extend(_check_enterprise_package(repo))
        failures.extend(_check_observability_contracts(repo))
        failures.extend(_check_reliability(repo))
        failures.extend(_check_ceo_signal_os(repo))
        failures.extend(_check_engineering_cutover_policy(repo))
        failures.extend(_check_kpi_baselines(repo))

    if failures:
        print("GLOBAL AI TRANSFORMATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("GLOBAL AI TRANSFORMATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
