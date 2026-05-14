#!/usr/bin/env python3
"""Render a public-safe holding portfolio snapshot into
`landing/assets/data/holding-portfolio.json`.

Byte-stable: sorted keys, no timestamps, no PII. Drift-gated in CI so
that the static landing page (`landing/group.html`) always reflects the
current registered BUs.

Public projection rules:
  - only entries whose status is BUILD / PILOT / SCALE / SPINOUT,
  - per-entry fields: slug, name, status, sector, doctrine_version,
    charter_path,
  - no owner, KPI, reason, git_author, entry_id, created_at.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = REPO_ROOT / "data" / "business_units.json"
OUTPUT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "holding-portfolio.json"

VISIBLE_STATUSES = {"BUILD", "PILOT", "SCALE", "SPINOUT"}
PUBLIC_FIELDS = ("slug", "name", "status", "sector", "doctrine_version", "charter_path")


def render() -> dict:
    if not INPUT_PATH.exists():
        data = {"entries": []}
    else:
        data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    visible = []
    for e in entries:
        if str(e.get("status") or "") not in VISIBLE_STATUSES:
            continue
        visible.append({k: str(e.get(k) or "") for k in PUBLIC_FIELDS})
    out = {
        "registry_id": "DEALIX-GROUP-PORTFOLIO-PUBLIC",
        "count": len(visible),
        "entries": visible,
        "doctrine": (
            "Public projection. Only BUs with status BUILD/PILOT/SCALE/"
            "SPINOUT. No owner, KPI, git provenance, or reason fields."
        ),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out


def main() -> int:
    out = render()
    try:
        display = OUTPUT_PATH.relative_to(REPO_ROOT)
    except ValueError:
        display = OUTPUT_PATH
    print(f"wrote {display}  ({out['count']} visible BUs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
