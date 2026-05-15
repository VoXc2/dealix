#!/usr/bin/env python3
"""Validate governance, deployment, compliance, and escalation rules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import (
    load_audit_rules,
    load_compliance_rules,
    load_deployment_rules,
    load_escalation_matrix,
)


def main() -> int:
    errors: list[str] = []
    deployment = load_deployment_rules()
    compliance = load_compliance_rules()
    audit = load_audit_rules()
    escalation = load_escalation_matrix()

    if "required_artifacts" not in deployment:
        errors.append("deployment_rules: missing required_artifacts")
    if "blocking_conditions" not in deployment:
        errors.append("deployment_rules: missing blocking_conditions")

    if not compliance.get("frameworks"):
        errors.append("compliance_rules: frameworks empty")
    if not compliance.get("controls_required_for_data_services"):
        errors.append("compliance_rules: controls_required_for_data_services empty")
    if not compliance.get("compliance_profiles"):
        errors.append("compliance_rules: compliance_profiles missing")

    if not audit.get("required_audit_fields"):
        errors.append("audit_rules: required_audit_fields missing")
    if "evidence_export_required" not in audit:
        errors.append("audit_rules: evidence_export_required missing")

    if not escalation.get("severity_levels"):
        errors.append("escalation_matrix: severity_levels missing")
    if not escalation.get("service_routes"):
        errors.append("escalation_matrix: service_routes missing")

    if errors:
        print("GOVERNANCE_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("GOVERNANCE_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
