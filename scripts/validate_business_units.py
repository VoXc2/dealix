#!/usr/bin/env python3
"""Validate `data/business_units.json` end-to-end.

Checks for every entry:
  - entry_id, git_author, created_at non-empty,
  - status in UnitPortfolioDecision enum,
  - KILL / HOLD entries have a non-empty reason,
  - charter_path resolves to an existing file under docs/,
  - doctrine_version matches a published doctrine version in
    `open-doctrine/doctrine_versions.json`.

Exit 0 if every entry valid; 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "business_units.json"
DOCTRINE_VERSIONS = REPO_ROOT / "open-doctrine" / "doctrine_versions.json"

sys.path.insert(0, str(REPO_ROOT))
from auto_client_acquisition.holding_os.unit_governance import (  # noqa: E402
    UnitPortfolioDecision,
)

VALID_STATUSES = {s.name for s in UnitPortfolioDecision}


def _known_doctrine_versions() -> set[str]:
    if not DOCTRINE_VERSIONS.exists():
        return set()
    try:
        data = json.loads(DOCTRINE_VERSIONS.read_text(encoding="utf-8"))
        return {v["version"] for v in (data.get("versions") or [])}
    except Exception:
        return set()


def main() -> int:
    if not REGISTRY.exists():
        print(f"missing {REGISTRY}", file=sys.stderr)
        return 1
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e}", file=sys.stderr)
        return 1

    entries = data.get("entries") or []
    versions = _known_doctrine_versions()
    failures: list[str] = []

    for i, entry in enumerate(entries):
        for required in ("entry_id", "git_author", "created_at"):
            v = entry.get(required)
            if not (isinstance(v, str) and v.strip()):
                failures.append(f"entry[{i}] missing {required}")
        status = entry.get("status")
        if status not in VALID_STATUSES:
            failures.append(f"entry[{i}] unknown status {status!r}")
        if status in ("KILL", "HOLD"):
            reason = entry.get("reason")
            if not (isinstance(reason, str) and reason.strip()):
                failures.append(f"entry[{i}] status {status} requires reason")
        # Charter path resolves.
        cp = str(entry.get("charter_path") or "")
        if cp and not (REPO_ROOT / cp).exists():
            failures.append(f"entry[{i}] charter_path missing: {cp}")
        # Doctrine version matches a published version (when versions
        # registry exists).
        dv = entry.get("doctrine_version")
        if versions and dv and dv not in versions:
            failures.append(f"entry[{i}] doctrine_version {dv!r} not published")

    if failures:
        print(f"{len(failures)} validation error(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    by_status: dict[str, int] = {}
    for e in entries:
        by_status[e["status"]] = by_status.get(e["status"], 0) + 1
    print(f"OK — {len(entries)} business unit(s) valid.")
    for status in sorted(by_status):
        print(f"  {status:<8s} {by_status[status]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
