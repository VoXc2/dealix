#!/usr/bin/env python3
"""
Dealix Truth Registry Validator
════════════════════════════════════════════════════════════════════
يفحص docs/registry/TRUTH.yaml ويتأكد من:
  - كل claim بـ status=live عنده telemetry_days >= 30
  - كل claim بـ status=pilot عنده evidence غير فارغة
  - كل claim عنده id و owner و last_verified

يُشغَّل في CI على كل push/PR.

Usage:
    python scripts/validate_truth_registry.py
Exit codes:
    0 = valid
    1 = invalid
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print("❌ PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "docs" / "registry" / "TRUTH.yaml"
REQUIRED_FIELDS = {"id", "claim", "status", "evidence", "telemetry_days", "last_verified", "owner"}
VALID_STATUSES = {"planned", "in_development", "in_testing", "staging", "pilot", "live", "deprecated"}


def validate() -> int:
    if not REGISTRY_PATH.exists():
        print(f"❌ Truth Registry not found: {REGISTRY_PATH}")
        return 1

    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ YAML parse error: {e}")
            return 1

    if not isinstance(data, dict):
        print("❌ Registry root must be a mapping")
        return 1

    claims = data.get("claims", [])
    if not isinstance(claims, list):
        print("❌ 'claims' must be a list")
        return 1

    errors: list[str] = []
    seen_ids: set[str] = set()

    for i, claim in enumerate(claims):
        prefix = f"claim[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix}: not a mapping")
            continue

        missing = REQUIRED_FIELDS - set(claim.keys())
        if missing:
            errors.append(f"{prefix}: missing fields: {sorted(missing)}")
            continue

        cid = claim["id"]
        if cid in seen_ids:
            errors.append(f"{prefix}: duplicate id '{cid}'")
        seen_ids.add(cid)

        status = claim["status"]
        if status not in VALID_STATUSES:
            errors.append(f"{cid}: invalid status '{status}' (valid: {sorted(VALID_STATUSES)})")

        telemetry = claim.get("telemetry_days", 0)
        if not isinstance(telemetry, int):
            errors.append(f"{cid}: telemetry_days must be int")
            telemetry = 0

        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{cid}: evidence must be a list")
            evidence = []

        # Core invariant: live REQUIRES 30+ days telemetry
        if status == "live" and telemetry < 30:
            errors.append(
                f"{cid}: status='live' but telemetry_days={telemetry} (must be >= 30). "
                f"Downgrade to 'staging' or 'pilot' until you have 30 days of production data."
            )

        # Pilot REQUIRES evidence
        if status == "pilot" and not evidence:
            errors.append(f"{cid}: status='pilot' but evidence is empty")

        # Validate date format
        try:
            last = claim["last_verified"]
            if isinstance(last, str):
                datetime.fromisoformat(last)
        except (ValueError, TypeError):
            errors.append(f"{cid}: last_verified must be ISO date (YYYY-MM-DD)")

    # Summary
    total = len(claims)
    by_status: dict[str, int] = {}
    for c in claims:
        if isinstance(c, dict) and "status" in c:
            by_status[c["status"]] = by_status.get(c["status"], 0) + 1

    print(f"📊 Truth Registry: {total} claims")
    for s in sorted(by_status.keys()):
        print(f"   {s}: {by_status[s]}")

    if errors:
        print(f"\n❌ {len(errors)} validation error(s):")
        for e in errors:
            print(f"   • {e}")
        return 1

    print(f"\n✅ Truth Registry valid (validated at {datetime.now(timezone.utc).isoformat()})")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
