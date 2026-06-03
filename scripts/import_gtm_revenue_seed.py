#!/usr/bin/env python3
"""Import GTM revenue-machine seed via Data OS API or direct DB seed.

Usage:
  python scripts/import_gtm_revenue_seed.py --dry-run
  python scripts/import_gtm_revenue_seed.py --db
  python scripts/import_gtm_revenue_seed.py --api --base http://localhost:8000
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = REPO_ROOT / "docs/commercial/operations/targeting/gtm_revenue_machine_import.json"


def _load_payload() -> dict:
    if not PAYLOAD.is_file():
        raise SystemExit(f"missing payload: {PAYLOAD}")
    return json.loads(PAYLOAD.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Print row count only")
    p.add_argument("--db", action="store_true", help="Run seed_revenue_machine_candidates.py")
    p.add_argument("--api", action="store_true", help="POST /api/v1/data/import")
    p.add_argument("--base", default="http://localhost:8000")
    args = p.parse_args()

    body = _load_payload()
    rows = body.get("rows") or []
    print(f"payload rows: {len(rows)} · source={body.get('source_name')}")

    if args.dry_run:
        return 0

    if args.db or (not args.api):
        seed = REPO_ROOT / "scripts" / "seed_revenue_machine_candidates.py"
        return subprocess.call([sys.executable, str(seed)])

    import urllib.error
    import urllib.request

    url = f"{args.base.rstrip('/')}/api/v1/data/import"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            print(resp.read().decode("utf-8")[:2000])
    except urllib.error.URLError as exc:
        print(f"API import failed: {exc}", file=sys.stderr)
        print("Fallback: python scripts/seed_revenue_machine_candidates.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
