#!/usr/bin/env python3
"""Production smoke — GET /health and optional ops-autopilot (admin key)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def _get(url: str, headers: dict[str, str] | None = None) -> tuple[int, dict]:
    req = Request(url, headers=headers or {}, method="GET")
    try:
        with urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            try:
                body = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                body = {"raw": raw[:500]}
            return resp.status, body
    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {"error": raw[:500]}
        return e.code, body
    except URLError as e:
        return 0, {"error": str(e.reason)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--base",
        default=os.environ.get("DEALIX_API_BASE")
        or os.environ.get("DEALIX_API_URL")
        or os.environ.get("NEXT_PUBLIC_API_URL")
        or "",
        help="API base URL (no trailing slash)",
    )
    p.add_argument(
        "--admin-key",
        default=os.environ.get("DEALIX_ADMIN_API_KEY") or "",
        help="X-Admin-API-Key for ops-autopilot smoke",
    )
    args = p.parse_args()
    base = (args.base or "").rstrip("/")
    if not base:
        print("PROD_SMOKE: SKIP — set DEALIX_API_BASE or pass --base")
        return 0

    fail = False
    code, body = _get(f"{base}/health")
    if code == 200:
        print(f"PROD_SMOKE: health OK ({base}/health)")
    else:
        print(f"PROD_SMOKE: health FAIL code={code} body={body}")
        fail = True

    if args.admin_key:
        headers = {"X-Admin-API-Key": args.admin_key}
        for path in (
            "/api/v1/ops-autopilot/war-room/summary",
            "/api/v1/ops-autopilot/targeting/pool",
        ):
            code, body = _get(f"{base}{path}", headers)
            if code == 200:
                print(f"PROD_SMOKE: {path} OK")
            else:
                print(f"PROD_SMOKE: {path} FAIL code={code}")
                fail = True
    else:
        print("PROD_SMOKE: ops-autopilot skipped (no DEALIX_ADMIN_API_KEY)")

    if fail:
        print("PROD_SMOKE_VERDICT: FAIL")
        return 1
    print("PROD_SMOKE_VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
