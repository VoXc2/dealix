"""Load founder weekly/daily strategy doc references (YAML)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS_PATH = REPO_ROOT / "dealix" / "config" / "founder_weekly_strategy_refs.yaml"


@lru_cache(maxsize=1)
def load_founder_strategy_refs() -> dict[str, Any]:
    if not REFS_PATH.is_file():
        return {"version": "0", "daily": [], "weekly": [], "ui_routes": {}}
    data = yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def strategy_links_flat() -> dict[str, str]:
    """Paths keyed by doc id for digest / API."""
    refs = load_founder_strategy_refs()
    out: dict[str, str] = {}
    for section in ("daily", "weekly"):
        for item in refs.get(section) or []:
            if isinstance(item, dict) and item.get("id") and item.get("path"):
                out[str(item["id"])] = str(item["path"])
    return out


def strategy_refs_status() -> dict[str, Any]:
    refs = load_founder_strategy_refs()
    daily = refs.get("daily") or []
    weekly = refs.get("weekly") or []
    missing: list[str] = []
    for item in [*daily, *weekly]:
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if rel and not (REPO_ROOT / str(rel)).is_file():
            missing.append(str(rel))
    return {
        "ok": len(daily) >= 2 and len(weekly) >= 1 and not missing,
        "daily_count": len(daily),
        "weekly_count": len(weekly),
        "missing_paths": missing,
        "cadence_ar": refs.get("cadence_ar"),
    }
