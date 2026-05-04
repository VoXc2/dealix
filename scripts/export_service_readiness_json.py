#!/usr/bin/env python3
"""Export the service readiness matrix to JSON for the static landing site.

Reads docs/registry/SERVICE_READINESS_MATRIX.yaml and writes
landing/assets/data/service-readiness.json. The renderer
(landing/assets/js/service-console.js) consumes this file at runtime.

Run as part of the deploy step BEFORE publishing landing/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = REPO_ROOT / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"
OUT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "service-readiness.json"

ALLOWED_STATUSES = ["live", "pilot", "partial", "target", "blocked", "backlog"]


def main() -> int:
    if not MATRIX_PATH.exists():
        print(f"FAIL: missing {MATRIX_PATH}", file=sys.stderr)
        return 1

    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    services = data.get("services") or []
    bundles = data.get("bundles") or []

    counts = {s: 0 for s in ALLOWED_STATUSES}
    counts["total"] = 0
    for svc in services:
        s = svc.get("status")
        if s in counts:
            counts[s] += 1
        counts["total"] += 1

    payload = {
        "version": data.get("version", 1),
        "owner": data.get("owner"),
        "last_updated": data.get("last_updated"),
        "source_file": "docs/registry/SERVICE_READINESS_MATRIX.yaml",
        "counts": counts,
        "bundles": bundles,
        "services": services,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")

    print(
        f"OK: wrote {OUT_PATH.relative_to(REPO_ROOT)} "
        f"(services={counts['total']} live={counts['live']} "
        f"pilot={counts['pilot']} partial={counts['partial']} "
        f"target={counts['target']} blocked={counts['blocked']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
