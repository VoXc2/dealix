#!/usr/bin/env python3
"""
cron_dealix_self_ops.py — daily Dealix-on-itself runner.

Runs daily_self_ops() which:
  1. Ensures Dealix's CustomerRecord exists
  2. Seeds 6 ICP-fit prospects if needed
  3. Generates 5 LLM-drafted LinkedIn intros
  4. Queues them in the Approval Queue

Recommended Railway cron: daily 06:00 KSA (03:00 UTC) — before founder
opens dealix smart-launch at 9 AM.

Usage:
    python scripts/cron_dealix_self_ops.py
    python scripts/cron_dealix_self_ops.py --prospects 10 --intros 3
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cron_dealix_self_ops")


async def _run(prospects: int, intros: int) -> dict:
    from auto_client_acquisition.self_ops import daily_self_ops
    r = await daily_self_ops(prospect_target=prospects, intro_count=intros)
    return {
        "customer_id": r.customer_id,
        "prospects_seeded": r.prospects_seeded,
        "drafts_generated": r.drafts_generated,
        "drafts_used_llm": r.drafts_used_llm,
        "errors": r.errors,
        "notes": r.notes,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--prospects", type=int, default=6)
    p.add_argument("--intros", type=int, default=5)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()
    try:
        result = asyncio.run(_run(args.prospects, args.intros))
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
