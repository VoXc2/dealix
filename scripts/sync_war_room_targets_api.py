#!/usr/bin/env python3
"""POST default agency CSV → War Room via ops-autopilot API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", default=os.getenv("DEALIX_API_BASE", "http://localhost:8000"))
    p.add_argument("--admin-key", default=os.getenv("DEALIX_ADMIN_API_KEY", ""))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not args.admin_key:
        print("Set DEALIX_ADMIN_API_KEY", file=sys.stderr)
        return 2

    body = {"use_default_csv": True}
    if args.dry_run:
        print(json.dumps({"dry_run": True, "body": body}, ensure_ascii=False, indent=2))
        return 0

    url = f"{args.base.rstrip('/')}/api/v1/ops-autopilot/war-room/import-targets"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Admin-API-Key": args.admin_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            print(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"API unreachable: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
