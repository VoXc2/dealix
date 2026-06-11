"""Post-deploy smoke test: hits a set of HTTP endpoints and reports status codes.

Usage:
    python3 scripts/post_deploy_smoke.py --base-url http://localhost:3100
"""
from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path


PATHS = [
    "/",
    "/sales-machine",
    "/lead-engine",
    "/offers",
    "/pricing",
    "/command-center",
    "/war-room",
    "/pipeline",
    "/delivery-os",
    "/kpi-finance",
    "/client-acquisition",
    "/automated-sales",
    "/persuasion-room",
    "/brand",
    "/cases",
    "/revenue-machine",
    "/sales-assets",
    "/partner-room",
    "/daily-draft",
    "/api/company-os/ceo-brief",
    "/api/company-os/founder-dashboard",
    "/api/sales-machine/ultimate-pack",
    "/api/sales-machine/daily-pack",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    print(f"Dealix post-deploy smoke test: {base}")
    print("=" * 50)

    failures: list[str] = []
    for path in PATHS:
        url = f"{base}{path}"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:  # noqa: BLE001
            print(f"  {path:40s}  ERROR: {e}")
            failures.append(path)
            continue
        flag = "OK" if 200 <= status < 400 else "FAIL"
        print(f"  {path:40s}  HTTP {status}  {flag}")
        if status >= 400:
            failures.append(path)

    if failures:
        print(f"\n{len(failures)} paths failed")
        return 1
    print(f"\nAll {len(PATHS)} paths OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
