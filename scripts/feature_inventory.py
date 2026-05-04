#!/usr/bin/env python3
"""
feature_inventory.py — Layer-1 verification.

Reads docs/FEATURE_INVENTORY.md and asserts every claimed file path actually
exists. Doesn't validate semantic correctness — just that the inventory
isn't lying about what's in the repo.

Format the doc must follow (markdown table inside fenced ```inventory blocks):

```inventory
feature_id          | file_paths
public_website      | landing/index.html,landing/services.html,...
service_tower       | api/routers/services.py,auto_client_acquisition/service_tower/contracts.py
...
```

Multiple ```inventory blocks are merged. Lines starting with `#` inside
the block are comments. Header line is the first non-comment line.

Usage:
    python scripts/feature_inventory.py
Exit:
    0 — all referenced files exist
    1 — any missing
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOC = REPO / "docs" / "FEATURE_INVENTORY.md"


def parse(text: str) -> list[tuple[str, list[str]]]:
    """Extract feature → file-paths from all ```inventory blocks."""
    rows: list[tuple[str, list[str]]] = []
    blocks = re.findall(r"```inventory\s*\n(.*?)```", text, re.DOTALL)
    for blk in blocks:
        lines = [ln.strip() for ln in blk.splitlines()
                 if ln.strip() and not ln.strip().startswith("#")]
        if not lines:
            continue
        # Skip header row if it looks like one
        if "|" in lines[0] and ("file_paths" in lines[0].lower() or "feature_id" in lines[0].lower()):
            lines = lines[1:]
        for ln in lines:
            if "|" not in ln:
                continue
            parts = [p.strip() for p in ln.split("|", 1)]
            if len(parts) != 2:
                continue
            fid, paths_csv = parts
            paths = [p.strip() for p in paths_csv.split(",") if p.strip()]
            if fid and paths:
                rows.append((fid, paths))
    return rows


def main() -> int:
    if not DOC.exists():
        print(f"FAIL: {DOC} does not exist")
        return 1
    rows = parse(DOC.read_text(encoding="utf-8"))
    if not rows:
        print(f"FAIL: no ```inventory blocks parsed from {DOC.name}")
        return 1

    missing: list[tuple[str, str]] = []
    total_files = 0
    for feature_id, paths in rows:
        for p in paths:
            total_files += 1
            full = REPO / p
            if not full.exists():
                missing.append((feature_id, p))

    if missing:
        print(f"FAIL: {len(missing)}/{total_files} file(s) missing:")
        for feature_id, p in missing:
            print(f"  - [{feature_id}] {p}")
        return 1

    print(f"OK: {len(rows)} feature(s) · {total_files} file(s) all present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
