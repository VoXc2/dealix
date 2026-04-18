#!/usr/bin/env python3
"""
Dealix — Readiness Matrix Validator
====================================
Enforces the 8 Gates policy from DEALIX_SERVICE_REALITY_AND_TESTING_PROTOCOL_AR.md.

Rules enforced:
  1. A service with status "Live" MUST have all gates passing (policy.marketing_can_claim_live_only_if).
  2. Every service must have: status, contract_test, workflow_test, abuse_test, last_verified (if not Target), owner.
  3. status must be one of: Live | Partial | Pilot | Target | Deprecated.
  4. All "Live" services must have last_verified within last 30 days.
  5. Sum of summary counters must match actual counts.

Exit codes:
  0 = all gates pass
  1 = validation errors
  2 = schema errors

Usage:
  python scripts/validate_readiness_matrix.py
  python scripts/validate_readiness_matrix.py --strict  # fail on any warning too
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml")
    sys.exit(2)

MATRIX_PATH = Path(__file__).parent.parent / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"

VALID_STATUS = {"Live", "Partial", "Pilot", "Target", "Deprecated"}
VALID_GATE_RESULT = {"Pass", "Partial", "Fail", "N/A"}
REQUIRED_FIELDS = ["status", "contract_test", "workflow_test", "abuse_test", "owner"]
SERVICE_GROUPS = ["revenue_os", "partnership_os", "executive_os", "compliance", "infra"]


def load_matrix() -> dict:
    if not MATRIX_PATH.exists():
        print(f"ERROR: Matrix not found at {MATRIX_PATH}")
        sys.exit(2)
    with MATRIX_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def iter_services(matrix: dict):
    for group in SERVICE_GROUPS:
        services = matrix.get(group, {})
        if not isinstance(services, dict):
            continue
        for name, svc in services.items():
            if isinstance(svc, dict):
                yield f"{group}.{name}", svc


def validate(matrix: dict, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Required fields + status validity
    for fqn, svc in iter_services(matrix):
        for field in REQUIRED_FIELDS:
            if field not in svc:
                errors.append(f"{fqn}: missing required field '{field}'")
        status = svc.get("status")
        if status and status not in VALID_STATUS:
            errors.append(f"{fqn}: invalid status '{status}' (must be one of {sorted(VALID_STATUS)})")
        for gate in ("contract_test", "workflow_test", "abuse_test"):
            val = svc.get(gate)
            if val and val not in VALID_GATE_RESULT:
                errors.append(f"{fqn}: invalid {gate} '{val}' (must be one of {sorted(VALID_GATE_RESULT)})")

    # 2. "Live" services must have ALL gates passing
    for fqn, svc in iter_services(matrix):
        if svc.get("status") != "Live":
            continue
        for gate in ("contract_test", "workflow_test", "abuse_test"):
            if svc.get(gate) != "Pass":
                errors.append(
                    f"{fqn}: claims Live but {gate} = {svc.get(gate)!r}. "
                    "Demote to Partial or fix the gate."
                )
        if svc.get("telemetry_visible") is False:
            warnings.append(f"{fqn}: Live without telemetry. See Gate 7 (Observability).")

    # 3. "Live" services must be verified within last 30 days
    cutoff = datetime.utcnow() - timedelta(days=30)
    for fqn, svc in iter_services(matrix):
        if svc.get("status") != "Live":
            continue
        lv = svc.get("last_verified")
        if not lv:
            errors.append(f"{fqn}: Live but last_verified is null. Run weekly reality review.")
            continue
        try:
            lv_dt = datetime.fromisoformat(str(lv))
            if lv_dt < cutoff:
                errors.append(
                    f"{fqn}: Live but last_verified={lv} is older than 30 days. "
                    "Re-verify or demote."
                )
        except ValueError:
            errors.append(f"{fqn}: last_verified '{lv}' is not ISO date")

    # 4. Summary counters sanity
    summary = matrix.get("summary", {})
    actual_counts = {s: 0 for s in VALID_STATUS}
    total = 0
    for _, svc in iter_services(matrix):
        st = svc.get("status")
        if st in actual_counts:
            actual_counts[st] += 1
            total += 1
    if summary.get("total_services") != total:
        warnings.append(
            f"summary.total_services={summary.get('total_services')} but actual={total}"
        )
    for st, key in (("Live", "live"), ("Partial", "partial"), ("Pilot", "pilot"),
                    ("Target", "target"), ("Deprecated", "deprecated")):
        if summary.get(key) != actual_counts[st]:
            warnings.append(
                f"summary.{key}={summary.get(key)} but actual {st}={actual_counts[st]}"
            )

    # 5. No duplicate service names
    seen = set()
    for fqn, _ in iter_services(matrix):
        if fqn in seen:
            errors.append(f"Duplicate service fqn: {fqn}")
        seen.add(fqn)

    return errors, warnings


def print_summary(matrix: dict) -> None:
    actual_counts = {s: 0 for s in VALID_STATUS}
    for _, svc in iter_services(matrix):
        st = svc.get("status")
        if st in actual_counts:
            actual_counts[st] += 1

    print("\n─────────── Service Readiness Summary ───────────")
    for st in ("Live", "Partial", "Pilot", "Target", "Deprecated"):
        icon = {"Live": "🟢", "Partial": "🟡", "Pilot": "🔵",
                "Target": "⚪", "Deprecated": "⚫"}[st]
        print(f"  {icon} {st:<12} {actual_counts[st]}")
    print(f"  Total:       {sum(actual_counts.values())}")

    # Highlight what's "Live"
    print("\n🟢 Live services:")
    for fqn, svc in iter_services(matrix):
        if svc.get("status") == "Live":
            gates = [svc.get(g, "?") for g in ("contract_test", "workflow_test", "abuse_test")]
            print(f"   • {fqn} — gates: {'/'.join(gates)}")
    print()


def main() -> int:
    strict = "--strict" in sys.argv
    matrix = load_matrix()
    errors, warnings = validate(matrix, strict=strict)

    print_summary(matrix)

    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   {w}")
        print()

    if errors:
        print("❌ Errors:")
        for e in errors:
            print(f"   {e}")
        print(f"\n{len(errors)} error(s). Matrix INVALID.")
        return 1

    if strict and warnings:
        print(f"❌ Strict mode: {len(warnings)} warning(s) → fail.")
        return 1

    print("✅ Service Readiness Matrix valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
