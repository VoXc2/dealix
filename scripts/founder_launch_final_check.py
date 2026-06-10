#!/usr/bin/env python3
"""Founder final launch check for Dealix.

Runs local repository deployment checks and optional live health probes.
Dependency-free by design so it works in CI, Railway shells, and emergency sessions.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def run_step(name: str, command: list[str], *, timeout: int = 120) -> bool:
    print(f"\n=== {name} ===")
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"FAIL: timed out after {timeout}s")
        return False

    print(completed.stdout.strip())
    if completed.returncode != 0:
        print(f"FAIL: exit={completed.returncode}")
        return False
    print("OK")
    return True


def probe_url(url: str, *, timeout: int = 15) -> bool:
    request = Request(url, headers={"User-Agent": "dealix-founder-final-check/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - operator-supplied URL
            body = response.read(4096).decode("utf-8", errors="replace")
            print(f"{url} -> HTTP {response.status}")
            try:
                payload = json.loads(body)
                print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
            except json.JSONDecodeError:
                print(body[:500])
            return 200 <= response.status < 400
    except HTTPError as exc:
        print(f"{url} -> HTTP {exc.code}")
        return False
    except URLError as exc:
        print(f"{url} -> URL error: {exc.reason}")
        return False
    except TimeoutError:
        print(f"{url} -> timeout")
        return False


def normalize_base_url(value: str) -> str:
    return value.rstrip("/")


def add_health_probe(urls: list[str], base_url: str | None) -> None:
    if base_url:
        urls.append(f"{normalize_base_url(base_url)}/healthz")


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix founder final launch check")
    parser.add_argument("--live", action="store_true", help="Probe live deployment health URLs")
    parser.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    parser.add_argument("--frontend-base", default=os.getenv("DEALIX_FRONTEND_BASE") or os.getenv("DEALIX_FRONTEND_URL") or "https://dealix.me")
    parser.add_argument("--apps-web-base", default=os.getenv("DEALIX_APPS_WEB_BASE") or os.getenv("DEALIX_WEB_BASE") or os.getenv("DEALIX_WEB_URL"))
    parser.add_argument("--skip-openapi", action="store_true", help="Skip OpenAPI contract check")
    args = parser.parse_args()

    checks: list[tuple[str, list[str], int]] = [
        ("Railway deploy surfaces", [sys.executable, "scripts/verify_railway_surfaces.py"], 60),
        ("Environment contract", [sys.executable, "scripts/check_env_contract.py"], 60),
    ]
    if not args.skip_openapi:
        checks.append(("OpenAPI contract", [sys.executable, "scripts/check_openapi_contract.py"], 90))

    ok = True
    for name, command, timeout in checks:
        ok = run_step(name, command, timeout=timeout) and ok

    if args.live:
        print("\n=== Live health probes ===")
        api_base = normalize_base_url(args.api_base)
        live_urls = [
            f"{api_base}/healthz",
            f"{api_base}/ready",
        ]
        add_health_probe(live_urls, args.frontend_base)
        add_health_probe(live_urls, args.apps_web_base)
        for url in dict.fromkeys(live_urls):
            ok = probe_url(url) and ok

    if ok:
        print("\nFOUNDER_LAUNCH_FINAL_CHECK=ok")
        return 0
    print("\nFOUNDER_LAUNCH_FINAL_CHECK=fail")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
