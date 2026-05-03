#!/usr/bin/env python3
"""
Cross-check the delivery workflow doc against the live route inventory.

Reads `docs/SERVICE_DELIVERY_WORKFLOWS.md` for `/api/...` mentions, then
fetches `${BASE_URL}/openapi.json` and prints which referenced routes
are present, missing, or 500. Read-only. No writes.

Exit code 0 if every referenced route exists.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOC = REPO / "docs" / "SERVICE_DELIVERY_WORKFLOWS.md"
BASE_URL = os.getenv("BASE_URL", "https://api.dealix.me").rstrip("/")
TIMEOUT = float(os.getenv("VERIFY_TIMEOUT_S", "10"))


_ROUTE_RE = re.compile(r"`(GET|POST|PATCH|PUT|DELETE)\s+(/api/v1[^\s`]+)`")


def referenced_routes() -> set[tuple[str, str]]:
    if not DOC.exists():
        return set()
    txt = DOC.read_text(encoding="utf-8")
    found: set[tuple[str, str]] = set()
    for m in _ROUTE_RE.finditer(txt):
        method = m.group(1).upper()
        path = m.group(2).strip()
        # Normalize {id} placeholders
        path = re.sub(r"\{[^}]+\}", "{id}", path)
        # Strip query string and trailing punctuation
        path = path.split("?", 1)[0]
        path = path.rstrip(".,)`')")
        found.add((method, path))
    return found


def live_routes() -> set[tuple[str, str]]:
    try:
        with urllib.request.urlopen(f"{BASE_URL}/openapi.json", timeout=TIMEOUT) as r:  # noqa: S310
            spec = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"WORKFLOWS_VERIFY_FAIL  cannot reach openapi.json: {e}")
        return set()
    out: set[tuple[str, str]] = set()
    for path, ops in (spec.get("paths") or {}).items():
        norm = re.sub(r"\{[^}]+\}", "{id}", path)
        for method in ops.keys():
            out.add((method.upper(), norm))
    return out


def main() -> int:
    refs = referenced_routes()
    if not refs:
        print("WORKFLOWS_VERIFY_FAIL  no routes referenced in doc")
        return 1
    live = live_routes()
    missing = sorted(refs - live)
    present = sorted(refs & live)
    print(f"referenced={len(refs)}  live_present={len(present)}  missing={len(missing)}")
    if missing:
        print("MISSING ROUTES:")
        for m, p in missing:
            print(f"  {m} {p}")
    else:
        print("WORKFLOWS_VERIFY_OK  all referenced routes are live")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
