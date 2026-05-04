#!/usr/bin/env python3
"""
cron_sprint_auto_progression.py — auto-advance active sprints day-by-day.

Finds SprintRecord rows where:
  - status NOT in (completed, aborted)
  - started_at + (current_day + 1) days <= now
  → calls the next day's generator endpoint internally.

Each generator already emits a ProofEvent and updates SprintRecord. So
this cron just times the calls so the founder doesn't have to ping
"day 4 generate" manually each day.

Usage:
    python scripts/cron_sprint_auto_progression.py
    python scripts/cron_sprint_auto_progression.py --dry-run

Recommended Railway cron: daily 08:30 KSA (05:30 UTC) — one hour before
the morning daily-ops window so today's sprint output is ready when the
founder runs `dealix smart-launch`.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cron_sprint_progression")


# Map current_day → the next day's generator function name in
# api/routers/sprints.py. Day 5 is GET, others are POST internally.
_DAY_GENERATORS = {
    0: "day_1",  # newly started sprint (current_day=0 → run day 1)
    1: "day_2",
    2: "day_3",
    3: "day_4",
    4: "day_5",
    5: "day_6",
    6: "day_7",
}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _run(dry_run: bool) -> dict:
    from sqlalchemy import select
    from db.models import SprintRecord
    from db.session import get_session

    findings = {
        "as_of": _now().isoformat(),
        "scanned": 0,
        "advanced": 0,
        "errors": [],
        "details": [],
    }

    async with get_session() as session:
        rows = list((await session.execute(
            select(SprintRecord).where(
                SprintRecord.status.notin_(("completed", "aborted"))
            )
        )).scalars().all())
        findings["scanned"] = len(rows)

        for sprint in rows:
            if sprint.current_day >= 7:
                continue  # already done

            started = sprint.started_at
            if not started:
                continue
            elapsed_days = (_now() - started).days
            target_day = sprint.current_day + 1
            # Only progress if at least target_day days have passed since start
            if elapsed_days < target_day:
                continue

            generator_name = _DAY_GENERATORS.get(sprint.current_day)
            if not generator_name:
                continue

            if dry_run:
                log.info(
                    "DRY-RUN would call %s on sprint=%s (current=%d, elapsed=%d)",
                    generator_name, sprint.id, sprint.current_day, elapsed_days,
                )
                findings["details"].append({
                    "sprint_id": sprint.id, "would_call": generator_name,
                    "current_day": sprint.current_day, "elapsed_days": elapsed_days,
                })
                continue

            # Call the day-handler in-process via the FastAPI app.
            # We use the router's function directly to avoid HTTP overhead.
            try:
                from api.routers import sprints as sprints_router
                fn = getattr(sprints_router, generator_name, None)
                if fn is None:
                    findings["errors"].append({
                        "sprint_id": sprint.id, "error": f"generator_not_found:{generator_name}",
                    })
                    continue
                # Day 5 has different signature (no body)
                # The generators all accept (sprint_id) — call with just that
                result = await fn(sprint.id)
                findings["advanced"] += 1
                findings["details"].append({
                    "sprint_id": sprint.id,
                    "advanced_to_day": (result or {}).get("day", "?"),
                    "proof_event_id": (result or {}).get("proof_event_id"),
                })
                log.info(
                    "auto_advanced sprint=%s → day=%s", sprint.id,
                    (result or {}).get("day"),
                )
            except Exception as exc:  # noqa: BLE001
                log.warning("auto_advance_failed sprint=%s err=%s", sprint.id, exc)
                findings["errors"].append({
                    "sprint_id": sprint.id, "error": str(exc)[:200],
                })

    return findings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()
    try:
        result = asyncio.run(_run(args.dry_run))
    except Exception as exc:  # noqa: BLE001
        log.error("cron_failed err=%s", exc)
        if not args.quiet:
            print(json.dumps({"ok": False, "error": str(exc)[:300]}, ensure_ascii=False))
        return 1
    if not args.quiet:
        print(json.dumps({"ok": True, **result}, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
