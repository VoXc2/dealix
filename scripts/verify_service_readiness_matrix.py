#!/usr/bin/env python3
"""Validate docs/registry/SERVICE_READINESS_MATRIX.yaml.

Refuses fake "Live" status and forbidden marketing claims. Run in CI on every
push; the landing exporter depends on a clean validation.

Exits 0 on success, 1 on any violation.
Emits a one-line summary on stdout suitable for GitHub Actions step output.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = REPO_ROOT / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"

ALLOWED_STATUSES = {"live", "pilot", "partial", "target", "blocked", "backlog"}
ALLOWED_BUNDLES = {
    "growth_starter",
    "data_to_revenue",
    "executive_growth_os",
    "partnership_growth",
    "full_control_tower",
    "internal",
}

REQUIRED_SERVICE_FIELDS = [
    "service_id",
    "name_ar",
    "name_en",
    "bundle",
    "capability_group",
    "status",
    "customer_value_ar",
    "customer_value_en",
    "target_customer_ar",
    "target_customer_en",
    "what_it_does_ar",
    "what_it_does_en",
    "required_inputs",
    "workflow_steps",
    "channels",
    "safe_action_policy",
    "approval_required",
    "blocked_actions",
    "deliverables",
    "proof_metrics",
    "api_endpoints",
    "frontend_surfaces",
    "data_dependencies",
    "integration_dependencies",
    "owner",
    "next_activation_step_ar",
    "next_activation_step_en",
    "definition_of_live",
    "tests_required",
    "risks",
    "sla",
    "last_verified_at",
    "evidence",
]

# Forbidden marketing claims. Allowed-context entries permit narrow uses
# (e.g. blocked_actions documenting that we *don't* do these things).
FORBIDDEN_PATTERNS_AR = [
    r"نضمن",
    r"مضمون",
    r"بدون أي مخاطرة",
]
FORBIDDEN_PATTERNS_EN = [
    r"\bguaranteed?\b",
    r"\bblast\b",
    r"\bscrape\b",
    r"\bscraping\b",
    r"\bcold\s+(whatsapp|outreach|email|messaging)\b",
]
# Fields whose role is to *document* what is blocked. These may legitimately
# mention forbidden patterns (e.g. blocked_actions: cold_whatsapp).
ALLOWED_CONTEXT_FIELDS = {
    "blocked_actions",
    "safe_action_policy",
    "risks",
    "next_activation_step_ar",
    "next_activation_step_en",
}

# 8 quality gates required for a service to be marked `live`.
LIVE_GATES = [
    "inputs",
    "workflow",
    "agent_role",
    "human_approval",
    "safe_tool_gateway",
    "deliverable",
    "proof_metric",
    "test_or_evidence",
]


def load_matrix() -> dict:
    if not MATRIX_PATH.exists():
        raise SystemExit(f"FAIL: matrix not found at {MATRIX_PATH}")
    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise SystemExit("FAIL: matrix root must be a mapping")
    return data


def _contains_forbidden(text: str, patterns: Iterable[str]) -> list[str]:
    hits: list[str] = []
    for pat in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            hits.append(pat)
    return hits


def _scan_for_forbidden(field: str, value, errors: list[str], svc_id: str) -> None:
    if field in ALLOWED_CONTEXT_FIELDS:
        return
    if isinstance(value, str):
        ar = _contains_forbidden(value, FORBIDDEN_PATTERNS_AR)
        en = _contains_forbidden(value, FORBIDDEN_PATTERNS_EN)
        for hit in ar + en:
            errors.append(
                f"{svc_id}.{field}: forbidden phrase {hit!r} found"
            )
    elif isinstance(value, list):
        for item in value:
            _scan_for_forbidden(field, item, errors, svc_id)


def _check_evidence_paths(svc: dict, errors: list[str]) -> None:
    for ev in svc.get("evidence", []) or []:
        if not isinstance(ev, str):
            continue
        # Allow workflow refs like .github/workflows/ci.yml; check on disk.
        if not (REPO_ROOT / ev).exists():
            errors.append(
                f"{svc['service_id']}.evidence: missing path {ev!r}"
            )


def _check_live_gates(svc: dict, errors: list[str]) -> None:
    """Live status requires explicit gates: block to be present and all true."""
    status = svc.get("status")
    if status != "live":
        return
    gates = svc.get("gates") or {}
    if not isinstance(gates, dict):
        errors.append(f"{svc['service_id']}: status=live requires a gates: mapping")
        return
    for g in LIVE_GATES:
        if not gates.get(g):
            errors.append(
                f"{svc['service_id']}: status=live requires gates.{g}=true"
            )
    # Live also requires every tests_required path to exist.
    for tp in svc.get("tests_required", []) or []:
        if not (REPO_ROOT / tp).exists():
            errors.append(
                f"{svc['service_id']}: status=live requires test file {tp!r} to exist"
            )


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    services = data.get("services") or []
    if not isinstance(services, list) or not services:
        errors.append("matrix.services must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for svc in services:
        if not isinstance(svc, dict):
            errors.append("a service entry is not a mapping")
            continue
        sid = svc.get("service_id", "<unknown>")
        for field in REQUIRED_SERVICE_FIELDS:
            if field not in svc:
                errors.append(f"{sid}: missing required field {field!r}")
        if sid in seen_ids:
            errors.append(f"{sid}: duplicate service_id")
        seen_ids.add(sid)

        status = svc.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(
                f"{sid}: status={status!r} not in {sorted(ALLOWED_STATUSES)}"
            )

        bundle = svc.get("bundle")
        if bundle not in ALLOWED_BUNDLES:
            errors.append(
                f"{sid}: bundle={bundle!r} not in {sorted(ALLOWED_BUNDLES)}"
            )

        for field, val in svc.items():
            _scan_for_forbidden(field, val, errors, sid)

        _check_evidence_paths(svc, errors)
        _check_live_gates(svc, errors)

    bundles = data.get("bundles") or []
    bundle_ids = {b.get("id") for b in bundles if isinstance(b, dict)}
    missing_bundles = ALLOWED_BUNDLES - bundle_ids
    if missing_bundles:
        errors.append(
            f"matrix.bundles missing required ids: {sorted(missing_bundles)}"
        )

    return errors


def counts(data: dict) -> dict[str, int]:
    out = {s: 0 for s in ALLOWED_STATUSES}
    out["total"] = 0
    for svc in data.get("services", []) or []:
        s = svc.get("status")
        if s in out:
            out[s] += 1
        out["total"] += 1
    return out


def main() -> int:
    data = load_matrix()
    errors = validate(data)
    c = counts(data)
    summary = (
        f"SERVICES_TOTAL={c['total']} "
        f"LIVE={c['live']} PILOT={c['pilot']} "
        f"PARTIAL={c['partial']} TARGET={c['target']} "
        f"BLOCKED={c['blocked']} BACKLOG={c['backlog']}"
    )
    if errors:
        print("FAIL: service readiness matrix has violations:")
        for e in errors:
            print(f"  - {e}")
        print(summary)
        return 1
    print(f"OK: {MATRIX_PATH.relative_to(REPO_ROOT)}")
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
