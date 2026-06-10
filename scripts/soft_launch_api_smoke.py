#!/usr/bin/env python3
"""Soft launch API smoke — TestClient, no live server required."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-smoke")
os.environ["DEALIX_ADMIN_API_KEY"] = "test-admin-smoke"

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Admin-API-Key": "test-admin-smoke"}
FAILURES: list[str] = []


def check(name: str, status: int, ok_codes: tuple[int, ...] = (200, 201)) -> None:
    if status in ok_codes:
        print(f"  ok: {name} ({status})")
    else:
        FAILURES.append(f"{name} status={status}")
        print(f"  FAIL: {name} ({status})")


def main() -> int:
    print("== soft_launch_api_smoke ==")
    r = client.get("/api/v1/ops-autopilot/marketing/calendar", headers=HEADERS)
    check("GET marketing/calendar", r.status_code)
    r = client.get("/api/v1/ops-autopilot/war-room/today-pack", headers=HEADERS)
    check("GET war-room/today-pack", r.status_code)
    r = client.post(
        "/api/v1/leads",
        headers=HEADERS,
        json={
            "company": "Smoke Co",
            "name": "Launch Smoke",
            "email": "smoke@example.sa",
            "phone": "+966501234567",
            "sector": "technology",
            "region": "Saudi Arabia",
            "budget": 50000,
            "message": "Soft launch smoke",
        },
    )
    check("POST /api/v1/leads", r.status_code)
    if FAILURES:
        print("SOFT_LAUNCH_API_SMOKE=FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("SOFT_LAUNCH_API_SMOKE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
