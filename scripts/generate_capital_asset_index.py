#!/usr/bin/env python3
"""Generate an empty (or seed) capital_asset_index.json.

Idempotent: if the file already exists with valid entries, it does
nothing. If the file is missing, it creates a fresh empty index.

Use this:
  - On a fresh clone, before running the verifier.
  - When the index file is accidentally deleted.
  - Never to "reset" entries (those are append-only by discipline).

Usage:
    python scripts/generate_capital_asset_index.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "capital_asset_index.json"


def main() -> int:
    if INDEX_PATH.exists():
        try:
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            n = len(data.get("entries") or [])
            print(f"data/capital_asset_index.json already exists ({n} entries) — no-op.")
            return 0
        except json.JSONDecodeError:
            print(
                "existing index is invalid JSON; refusing to overwrite. "
                "Fix manually before regenerating.",
                file=sys.stderr,
            )
            return 1

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    fresh = {
        "index_id": "CAPITAL-ASSET-INDEX-001",
        "updated_at": datetime.now(timezone.utc).date().isoformat(),
        "entries": [],
    }
    INDEX_PATH.write_text(
        json.dumps(fresh, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"created empty index: {INDEX_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
