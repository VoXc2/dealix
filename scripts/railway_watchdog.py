#!/usr/bin/env python3
"""Dealix Railway watchdog.

Designed for Railway Cron. Exits non-zero if public API health fails.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import UTC, datetime, timezone

API_URL = os.getenv("APP_URL") or os.getenv("DEALIX_API_URL") or "https://api.dealix.me"
API_URL = API_URL.rstrip("/")
HEALTH_PATH = os.getenv("DEALIX_HEALTH_PATH", "/healthz")
HEALTH_URL = f"{API_URL}{HEALTH_PATH}"


def check_health() -> dict[str, object]:
    started = time.time()
    try:
        req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "dealix-railway-watchdog/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = {"raw": body[:1000]}
            return {
                "ok": 200 <= response.status < 300,
                "status": int(response.status),
                "latency_ms": round((time.time() - started) * 1000),
                "body": parsed,
            }
    except Exception as exc:
        return {"ok": False, "error": repr(exc), "latency_ms": round((time.time() - started) * 1000)}


def main() -> int:
    payload = {
        "service": "dealix-watchdog",
        "checked_at": datetime.now(UTC).isoformat(),
        "health_url": HEALTH_URL,
        "result": check_health(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["result"].get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
