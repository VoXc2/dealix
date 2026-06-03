#!/usr/bin/env python3
"""Print Railway + GitHub env readiness (reads os.environ only)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from dealix.commercial_ops.railway_launch import (  # noqa: E402
    check_railway_api_env,
    check_railway_frontend_env,
)


def _stdout_utf8() -> None:
    out = getattr(sys.stdout, "reconfigure", None)
    if callable(out):
        try:
            out(encoding="utf-8")
        except Exception:
            pass


def main() -> int:
    _stdout_utf8()
    api = check_railway_api_env()
    fe = check_railway_frontend_env()
    payload = {"api": api, "frontend": fe}
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    print("\n== Railway API ==")
    for k, ok in api["api_required"].items():
        print(f"  {'OK' if ok else 'MISSING'}: {k}")
    print("\n== Payments ==")
    for k, ok in api["payments"].items():
        print(f"  {'OK' if ok else 'MISSING'}: {k}")
    print("\n== GitHub CI secrets (local check if exported) ==")
    for k, ok in api["github_ci"].items():
        print(f"  {'OK' if ok else 'MISSING'}: {k}")
    print("\n== Frontend ==")
    for k, ok in fe["frontend"].items():
        print(f"  {'OK' if ok else 'MISSING'}: {k}")

    print("\n== GitHub Settings -> Secrets (set manually) ==")
    print("  DEALIX_API_BASE=https://api.dealix.me")
    print("  DEALIX_API_KEY=<Bearer token matching API_KEYS or admin>")
    print("  DEALIX_ADMIN_API_KEY=<same as ADMIN_API_KEYS entry>")
    print("  DEALIX_SYNC_EVIDENCE=1  (optional)")

    if api["ready_for_api_deploy"] and fe["ready_for_fe_deploy"]:
        print("\nRAILWAY_ENV_CHECK=PASS (local env snapshot)")
        return 0
    print("\nRAILWAY_ENV_CHECK=INCOMPLETE — set vars on Railway / export locally to verify")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
