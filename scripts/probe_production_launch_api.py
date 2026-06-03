#!/usr/bin/env python3
"""Probe api.dealix.me for launch verify (health + optional admin routes)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _get(url: str, headers: dict | None = None) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(512).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(512).decode("utf-8", errors="replace")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--admin-key", default=os.getenv("DEALIX_ADMIN_API_KEY", ""))
    args = p.parse_args()
    base = args.base.rstrip("/")
    checks: list[dict] = []

    code, _ = _get(f"{base}/health")
    checks.append({"path": "/health", "status": code, "ok": code == 200})

    admin_paths = [
        "/api/v1/ops-autopilot/marketing/social-today",
        "/api/v1/ops-autopilot/war-room/today-pack",
        "/api/v1/ops-autopilot/founder/daily-pack",
    ]
    if args.admin_key:
        hdr = {"X-Admin-API-Key": args.admin_key}
        for path in admin_paths:
            code, _ = _get(f"{base}{path}", hdr)
            checks.append({"path": path, "status": code, "ok": code == 200})
    else:
        for path in admin_paths:
            checks.append({"path": path, "status": None, "ok": None, "skipped": "no admin key"})

    print(json.dumps({"base": base, "checks": checks}, indent=2))
    required_ok = [c for c in checks if c.get("ok") is not None]
    if all(c["ok"] for c in required_ok):
        print("PRODUCTION_LAUNCH_PROBE=PASS")
        return 0
    print("PRODUCTION_LAUNCH_PROBE=PARTIAL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
