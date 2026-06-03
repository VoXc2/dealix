"""Optional HTTP client for founder commercial digest."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def fetch_founder_dashboard(
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
) -> dict[str, Any] | None:
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return None
    req = Request(
        f"{base}/api/v1/ops-autopilot/founder-dashboard",
        headers={"X-Admin-API-Key": key},
        method="GET",
    )
    try:
        with urlopen(req, timeout=20) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def fetch_war_room_today_pack(
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
) -> dict[str, Any] | None:
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return None
    req = Request(
        f"{base}/api/v1/ops-autopilot/war-room/today-pack",
        headers={"X-Admin-API-Key": key},
        method="GET",
    )
    try:
        with urlopen(req, timeout=25) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def import_war_room_targets_api(
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
    use_default_csv: bool = True,
) -> dict[str, Any] | None:
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return None
    payload = {"use_default_csv": use_default_csv, "rows": []}
    req = Request(
        f"{base}/api/v1/ops-autopilot/war-room/import-targets",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Admin-API-Key": key,
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def trigger_daily_targeting(
    *,
    api_base: str | None = None,
    admin_key: str | None = None,
) -> dict[str, Any] | None:
    base = (api_base or os.environ.get("DEALIX_API_BASE") or "").rstrip("/")
    key = admin_key or os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""
    if not base or not key:
        return None
    req = Request(
        f"{base}/api/v1/automation/daily-targeting/run",
        data=b"{}",
        headers={
            "Content-Type": "application/json",
            "X-Admin-API-Key": key,
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None
