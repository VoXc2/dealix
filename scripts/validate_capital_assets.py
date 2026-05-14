#!/usr/bin/env python3
"""Validate every entry in data/capital_asset_index.json.

Exits 0 if every entry passes capital_ledger_event_valid(), 1 if any
entry fails. Used by:
  - CI (PR4 adds it to the doctrine-gate job)
  - The verifier matrix (it references this script name)
  - Local pre-flight before registering more assets

Usage:
    python scripts/validate_capital_assets.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "capital_asset_index.json"

sys.path.insert(0, str(REPO_ROOT))
from auto_client_acquisition.capital_os.asset_types import CapitalAssetType  # noqa: E402
from auto_client_acquisition.capital_os.capital_ledger import (  # noqa: E402
    CapitalLedgerEvent,
    capital_ledger_event_valid,
)


def main() -> int:
    if not INDEX_PATH.exists():
        print("data/capital_asset_index.json missing — nothing to validate.")
        print("(Empty index is valid. Register first asset via scripts/register_capital_asset.py.)")
        return 0

    try:
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e}", file=sys.stderr)
        return 1

    entries = data.get("entries") or []
    failures: list[str] = []
    valid_types = {t.value for t in CapitalAssetType}

    for i, entry in enumerate(entries):
        # Required fields for honest provenance:
        for required in ("entry_id", "created_at", "git_author"):
            if not entry.get(required):
                failures.append(f"entry[{i}]: missing {required}")
        # asset_type must be a known CapitalAssetType.
        atype = str(entry.get("asset_type") or "")
        if atype not in valid_types:
            failures.append(f"entry[{i}]: unknown asset_type {atype!r}")
            continue
        # CapitalLedgerEvent contract.
        ev = CapitalLedgerEvent(
            capital_event_id=str(entry.get("entry_id") or ""),
            project_id=str(entry.get("project_id") or ""),
            client_id=str(entry.get("client_id") or ""),
            asset_type=atype,
            title=str(entry.get("title") or ""),
            description=str(entry.get("description") or ""),
            evidence=str(entry.get("evidence") or ""),
        )
        if not capital_ledger_event_valid(ev):
            failures.append(f"entry[{i}]: fields fail capital_ledger_event_valid")

    if failures:
        print(f"{len(failures)} validation error(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"OK — {len(entries)} entries valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
