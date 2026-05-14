#!/usr/bin/env python3
"""Validate the Capital Asset Registry — Wave 19.

Schema integrity check. Run before any commit that touches the
registry. Exit 0 = clean. Exit 1 = at least one violation.

Doctrine:
- Every asset MUST cite real file paths (the validator checks each path exists).
- Every asset MUST link to at least one non-negotiable id.
- Every asset MUST carry a recent `last_reviewed` (ISO date) within 12 months.
- Public assets MUST NOT reference commercial-sensitive paths (anchor_partner_pipeline.json,
  any admin-only path, internal investor materials).

Usage:
    python scripts/validate_capital_assets.py
    python scripts/validate_capital_assets.py --strict   # also fail on warnings
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


_COMMERCIAL_SENSITIVE_TOKENS = (
    "anchor_partner_pipeline",
    "admin_key",
    "client_data",
    "private_pricing",
    "investor_confidential",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    from auto_client_acquisition.capital_os.capital_asset_registry import (
        CAPITAL_ASSETS,
    )
    from auto_client_acquisition.governance_os.non_negotiables import (
        NON_NEGOTIABLES,
    )

    valid_nn_ids = {n.id for n in NON_NEGOTIABLES}
    errors: list[str] = []
    warnings: list[str] = []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=365)).date().isoformat()

    seen_ids: set[str] = set()
    for a in CAPITAL_ASSETS:
        if a.asset_id in seen_ids:
            errors.append(f"{a.asset_id}: duplicate asset_id")
        seen_ids.add(a.asset_id)

        if not a.file_paths:
            errors.append(f"{a.asset_id}: file_paths is empty")
        for path in a.file_paths:
            full = REPO_ROOT / path
            if not full.exists():
                errors.append(f"{a.asset_id}: file_paths references missing path: {path}")

        if not a.linked_non_negotiables:
            errors.append(f"{a.asset_id}: linked_non_negotiables is empty (must link >= 1)")
        for nn in a.linked_non_negotiables:
            if nn not in valid_nn_ids:
                errors.append(f"{a.asset_id}: invalid non-negotiable id {nn!r}")

        if a.last_reviewed < cutoff:
            warnings.append(
                f"{a.asset_id}: last_reviewed={a.last_reviewed} is older than 1 year"
            )

        if a.public:
            for path in a.file_paths:
                for tok in _COMMERCIAL_SENSITIVE_TOKENS:
                    if tok in path:
                        errors.append(
                            f"{a.asset_id} (public=True): file_paths includes "
                            f"commercial-sensitive token {tok!r} in {path!r}"
                        )

    print("━━ Capital Asset Registry Validation ━━")
    print(f"Assets: {len(CAPITAL_ASSETS)}")
    print(f"Public-safe: {sum(1 for a in CAPITAL_ASSETS if a.public)}")
    print(f"Internal: {sum(1 for a in CAPITAL_ASSETS if not a.public)}")
    print()

    if errors:
        print("❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        print()
    if warnings:
        print("⚠ WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors or (args.strict and warnings):
        return 1
    print("✅ Registry valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
