#!/usr/bin/env python3
"""Unified governed daily commercial ops — bridge, health, weekly pack, digest hooks."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

BRIEFS_DIR = REPO_ROOT / "data" / "founder_briefs"


def _api_base() -> str:
    return (
        os.environ.get("DEALIX_API_BASE")
        or os.environ.get("DEALIX_API_URL")
        or os.environ.get("NEXT_PUBLIC_API_URL")
        or ""
    ).rstrip("/")


def _admin_key() -> str:
    return os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""


def _http_json(
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None = None,
    query: str = "",
) -> dict[str, Any] | None:
    base = _api_base()
    key = _admin_key()
    if not base or not key:
        return None
    url = f"{base}{path}"
    if query:
        url = f"{url}?{query}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = Request(
        url,
        data=data,
        headers={
            "X-Admin-API-Key": key,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urlopen(req, timeout=45) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {}
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"API {method} {path}: SKIP ({exc})", file=sys.stderr)
        return None


def step_replay_postgres(*, limit: int = 50) -> dict[str, Any] | None:
    return _http_json(
        "POST",
        "/api/v1/ops-autopilot/ingest/replay-postgres",
        query=f"limit={limit}&sources=google_ads,meta_lead_ads",
    )


def step_full_ops_health() -> dict[str, Any] | None:
    return _http_json("GET", "/api/v1/ops-autopilot/full-ops-health")


def step_weekly_pack_if_monday() -> dict[str, Any] | None:
    if datetime.now(UTC).weekday() != 0:
        print("weekly-pack: skip (not Monday)")
        return None
    return _http_json(
        "POST",
        "/api/v1/ops-autopilot/marketing/weekly-pack/apply",
        body={"queue_approvals": True},
    )


def step_kpi_status() -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "apply_kpi_founder_commercial.py"
    if not script.is_file():
        print("kpi: script missing", file=sys.stderr)
        return 0
    return subprocess.call([py, str(script), "--status"], cwd=REPO_ROOT)


def step_commercial_digest(*, out_path: Path | None = None) -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "founder_commercial_digest.py"
    if not script.is_file():
        return 0
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    out = out_path or BRIEFS_DIR / f"commercial_{date}.md"
    args = [py, str(script), "--out", str(out)]
    if os.environ.get("DEALIX_SYNC_EVIDENCE") == "1":
        args.append("--sync-evidence")
    return subprocess.call(args, cwd=REPO_ROOT)


def step_war_room_sync() -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "commercial_war_room_sync.py"
    if not script.is_file():
        return 0
    return subprocess.call([py, str(script)], cwd=REPO_ROOT)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-api", action="store_true", help="Skip HTTP steps (offline digest only)")
    p.add_argument("--api-only", action="store_true", help="Only HTTP bridge/health/weekly-pack")
    p.add_argument("--with-business-now", action="store_true")
    p.add_argument("--replay-limit", type=int, default=50)
    args = p.parse_args()

    date = datetime.now(UTC).strftime("%Y-%m-%d")
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("DRY-RUN - Dealix Daily Ops")
        print("1. POST ingest/replay-postgres")
        print("2. GET full-ops-health -> data/founder_briefs/ops_health_DATE.json")
        print("3. Monday: POST marketing/weekly-pack/apply")
        print("4. apply_kpi_founder_commercial.py --status")
        print("5. commercial_war_room_sync.py")
        print("6. founder_commercial_digest.py")
        print("DEALIX_DAILY_OPS_VERDICT=READY")
        return 0

    degraded = False

    if not args.skip_api and _api_base() and _admin_key():
        print("== 1/6 Postgres -> Autopilot replay ==")
        replay = step_replay_postgres(limit=args.replay_limit)
        if replay:
            print(json.dumps(replay, ensure_ascii=False, indent=2))
        else:
            degraded = True

        print("\n== 2/6 Full Ops Health ==")
        health = step_full_ops_health()
        if health:
            hp = BRIEFS_DIR / f"ops_health_{date}.json"
            hp.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"WROTE {hp}")
        else:
            degraded = True

        print("\n== 3/6 Weekly marketing pack (Monday only) ==")
        wp = step_weekly_pack_if_monday()
        if wp:
            print(json.dumps(wp, ensure_ascii=False, indent=2))
    else:
        print("API steps skipped (set DEALIX_API_BASE + DEALIX_ADMIN_API_KEY)", file=sys.stderr)
        degraded = True

    if args.with_business_now:
        bn = REPO_ROOT / "scripts" / "run_business_now.sh"
        if bn.is_file():
            print("\n== optional: Business NOW ==")
            subprocess.call(["bash", str(bn)], cwd=REPO_ROOT)

    if args.api_only:
        verdict = "DEGRADED" if degraded else "READY"
        print(f"\nDEALIX_DAILY_OPS_VERDICT={verdict}")
        return 0

    print("\n== 4/6 KPI commercial status ==")
    step_kpi_status()

    print("\n== 5/6 War Room sync ==")
    step_war_room_sync()

    print("\n== 6/6 Commercial digest ==")
    step_commercial_digest()

    verdict = "DEGRADED" if degraded else "READY"
    print(f"\nDEALIX_DAILY_OPS_VERDICT={verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
