#!/usr/bin/env python3
"""
cron_daily_ops.py — single-shot CLI to run one daily-ops window.

Used by Railway cron (or any external scheduler). Each invocation runs
exactly ONE window and exits — perfect for cron.

Usage:
    python scripts/cron_daily_ops.py --window morning
    python scripts/cron_daily_ops.py --window scorecard --dry-run

Recommended Railway cron schedule (KSA = UTC+3):
    "30 5 * * *"   morning      (08:30 KSA)
    "30 9 * * *"   midday       (12:30 KSA)
    "30 13 * * *"  closing      (16:30 KSA)
    "0  15 * * *"  scorecard    (18:00 KSA)

Exit codes:
    0   window ran cleanly (decisions written, no orchestrator error)
    1   window failed mid-run
    2   bad arguments / unknown window
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cron_daily_ops")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat()


async def _run(window: str, dry_run: bool) -> dict[str, Any]:
    from auto_client_acquisition.revenue_company_os.daily_ops_orchestrator import (
        WINDOWS, run_window,
    )
    from db.session import get_session

    if window not in WINDOWS:
        raise SystemExit(f"unknown_window: {window} (must be one of {list(WINDOWS)})")

    if dry_run:
        return {
            "dry_run": True,
            "window": window,
            "roles_planned": list(WINDOWS[window]),
            "would_call": "run_window(session, window=...)",
            "as_of": _now_iso(),
        }

    async with get_session() as session:
        result = await run_window(session, window=window)
        await session.commit()

    # Run self-growth auto-loop in the closing window (one extra call per day)
    if window == "closing":
        try:
            from auto_client_acquisition.revenue_company_os.self_growth_mode import loop_once
            sg = await loop_once()
            result["self_growth"] = sg
        except Exception as exc:  # noqa: BLE001
            log.warning("self_growth_loop_failed err=%s", str(exc)[:200])
            result["self_growth_error"] = str(exc)[:200]
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Run one daily-ops window")
    p.add_argument(
        "--window",
        required=True,
        choices=("morning", "midday", "closing", "scorecard"),
        help="Which daily-ops window to execute",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan without touching the database",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress JSON output (just return exit code)",
    )
    args = p.parse_args()

    try:
        result = asyncio.run(_run(args.window, args.dry_run))
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        log.error("cron_failed window=%s err=%s", args.window, exc)
        if not args.quiet:
            print(json.dumps({
                "ok": False,
                "window": args.window,
                "error": f"{type(exc).__name__}: {str(exc)[:300]}",
                "as_of": _now_iso(),
            }, ensure_ascii=False))
        return 1

    err = result.get("error") if isinstance(result, dict) else None
    payload = {"ok": err is None, **(result if isinstance(result, dict) else {})}
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, default=str))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
