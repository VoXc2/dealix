#!/usr/bin/env python3
"""Staging technical gate: /health, smoke paths, optional launch-readiness JSON.

Usage:
  export STAGING_BASE_URL=https://your-app.example.com
  python scripts/launch_readiness_check.py

Or:
  python scripts/launch_readiness_check.py --base-url https://your-app.example.com

Exit code 0 only if /health is 200 and all smoke paths return 200.

Terminal markers (grep-friendly):
  STAGING_HEALTH_OK
  DEPLOY_PARITY_OK
  SMOKE_STAGING_OK
  LAUNCH_READINESS_JSON_OK
  STAGING_LEVEL_1_TECH_OK

These markers mean **HTTP smoke passed** against the given base URL. They do NOT mean
commercial "paid beta ready" — see docs/ops/full_ops_pack/LEVEL_1_ACCEPTANCE_CHECKLIST_AR.md
for the distinction vs GET /api/v1/personal-operator/launch-readiness (internal score/stage).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import httpx  # noqa: E402

# Keep aligned with scripts/smoke_staging.py (GET only).
SMOKE_PATHS = [
    "/",
    "/health",
    "/api/v1/personal-operator/daily-brief",
    "/api/v1/personal-operator/launch-report",
    "/api/v1/v3/command-center/snapshot",
    "/api/v1/business/pricing",
]

LAUNCH_READINESS_PATH = "/api/v1/personal-operator/launch-readiness"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is optional (e.g. some environments); default stream is fine.
        pass

    parser = argparse.ArgumentParser(description="Health + smoke + optional launch-readiness for staging")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("STAGING_BASE_URL", "").strip().rstrip("/"),
        help="Staging origin (or set STAGING_BASE_URL)",
    )
    parser.add_argument(
        "--skip-readiness-json",
        action="store_true",
        help="Do not GET /api/v1/personal-operator/launch-readiness",
    )
    parser.add_argument(
        "--expect-git-sha",
        default=os.environ.get("EXPECT_GIT_SHA", "").strip(),
        help=(
            "Optional: assert /health git_sha matches this commit "
            "(full SHA or short prefix)."
        ),
    )
    args = parser.parse_args()
    base = args.base_url
    if not base:
        print("ERROR: set STAGING_BASE_URL or pass --base-url", file=sys.stderr)
        return 2

    timeout = float(os.environ.get("STAGING_SMOKE_TIMEOUT", "30"))
    failed = 0

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        health_url = f"{base}/health"
        try:
            hr = client.get(health_url)
        except httpx.RequestError as exc:
            print(f"STAGING_HEALTH_FAIL error={exc}", file=sys.stderr)
            return 1
        if hr.status_code != 200:
            print(f"STAGING_HEALTH_FAIL status={hr.status_code}", file=sys.stderr)
            return 1
        print("STAGING_HEALTH_OK")
        expected_sha = args.expect_git_sha.strip()
        if expected_sha:
            try:
                health_payload = hr.json()
            except Exception:
                print("DEPLOY_PARITY_FAIL health_not_json", file=sys.stderr)
                return 1
            remote_sha = str(health_payload.get("git_sha", "")).strip()
            if not remote_sha:
                print("DEPLOY_PARITY_FAIL missing_git_sha", file=sys.stderr)
                return 1
            if not remote_sha.startswith(expected_sha):
                print(
                    f"DEPLOY_PARITY_FAIL expected={expected_sha} actual={remote_sha}",
                    file=sys.stderr,
                )
                return 1
            print(f"DEPLOY_PARITY_OK git_sha={remote_sha}")

        for path in SMOKE_PATHS:
            url = f"{base}{path}"
            try:
                r = client.get(url)
            except httpx.RequestError as exc:
                print(f"FAIL {path} error={exc}", file=sys.stderr)
                failed += 1
                continue
            print(f"{r.status_code} {path}")
            if r.status_code != 200:
                failed += 1
                print(r.text[:400], file=sys.stderr)
            else:
                try:
                    print(json.dumps(r.json(), ensure_ascii=False)[:300])
                except Exception:
                    print(r.text[:120])

        if failed:
            print(f"SMOKE_STAGING_FAIL {failed} endpoints", file=sys.stderr)
            return 1
        print("SMOKE_STAGING_OK")

        if not args.skip_readiness_json:
            lr_url = f"{base}{LAUNCH_READINESS_PATH}"
            try:
                lr = client.get(lr_url)
            except httpx.RequestError as exc:
                print(f"LAUNCH_READINESS_JSON_FAIL error={exc}", file=sys.stderr)
                return 1
            if lr.status_code != 200:
                print(f"LAUNCH_READINESS_JSON_FAIL status={lr.status_code}", file=sys.stderr)
                return 1
            try:
                body = lr.json()
            except Exception:
                print("LAUNCH_READINESS_JSON_FAIL not json", file=sys.stderr)
                return 1
            print("LAUNCH_READINESS_JSON_OK")
            print(json.dumps(body, ensure_ascii=False, indent=2)[:2000])

    print("STAGING_LEVEL_1_TECH_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
