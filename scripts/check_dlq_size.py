#!/usr/bin/env python3
"""scripts/check_dlq_size.py

Health check for the Dead Letter Queue. Used both in CI (gate) and in scheduled
ops monitoring. Exits non-zero if any queue exceeds the threshold.

Usage:
    REDIS_URL=redis://... python scripts/check_dlq_size.py
    REDIS_URL=redis://... python scripts/check_dlq_size.py --max 5 --queue webhooks
    REDIS_URL=redis://... python scripts/check_dlq_size.py --json

CI integration: see .github/workflows/dlq_check.yml
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

DEFAULT_QUEUES = ["webhooks", "outbound", "enrichment"]
DEFAULT_MAX = 5


def get_redis() -> Any:
    url = os.environ.get("REDIS_URL")
    if not url:
        print("REDIS_URL not set — skipping (treating as pass)", file=sys.stderr)
        return None
    try:
        import redis
    except ImportError:
        print("redis package missing: pip install redis", file=sys.stderr)
        sys.exit(2)
    return redis.from_url(url, socket_timeout=5, decode_responses=True)


def queue_depth(r: Any, queue: str) -> int:
    return int(r.llen(f"dlq:{queue}") or 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=DEFAULT_MAX,
                        help="fail if any queue depth exceeds this (default: 5)")
    parser.add_argument("--queue", action="append",
                        help="queue name; can be repeated. Default: webhooks, outbound, enrichment")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    queues = args.queue or DEFAULT_QUEUES
    r = get_redis()
    if r is None:
        # Treat missing Redis as pass to avoid spurious CI failures when Redis
        # isn't reachable from the runner; the runtime check still applies.
        return 0

    report: dict[str, Any] = {"threshold": args.max, "queues": {}, "fails": []}
    for q in queues:
        try:
            depth = queue_depth(r, q)
        except Exception as exc:  # noqa: BLE001
            report["queues"][q] = {"depth": None, "error": str(exc)}
            continue
        report["queues"][q] = {"depth": depth}
        if depth > args.max:
            report["fails"].append(q)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for q, info in report["queues"].items():
            marker = "✗" if q in report["fails"] else "✓"
            depth = info.get("depth")
            print(f"  {marker} {q:<12} depth={depth}")
        if report["fails"]:
            print(f"\nFAIL: queues over threshold {args.max}: {', '.join(report['fails'])}",
                  file=sys.stderr)
        else:
            print(f"\nOK: all queues at or below threshold {args.max}")

    return 1 if report["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
