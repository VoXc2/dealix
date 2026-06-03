"""Load commercial market intelligence pack (YAML) for digest and APIs."""

from __future__ import annotations

from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS_PATH = REPO_ROOT / "dealix" / "config" / "market_intelligence_refs.yaml"

# Pillar order for weekly rotation (founder reads one deep doc per week)
PILLAR_ROTATION = (
    "saas_market",
    "governed_ai",
    "pdpl_legal",
    "founder_revops",
    "content_gtm",
    "positioning",
    "cloud_residency",
    "sales_champion",
)


@lru_cache(maxsize=1)
def load_market_intelligence_refs() -> dict[str, Any]:
    if not REFS_PATH.is_file():
        return {"version": "0", "pillars": {}, "index": ""}
    data = yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def market_intelligence_pillars_flat() -> list[dict[str, str]]:
    refs = load_market_intelligence_refs()
    out: list[dict[str, str]] = []
    for key, item in (refs.get("pillars") or {}).items():
        if isinstance(item, dict) and item.get("path"):
            out.append(
                {
                    "id": str(key),
                    "doc": str(item["path"]),
                    "topic_ar": str(item.get("label_ar") or key),
                }
            )
    return sorted(out, key=lambda x: x["id"])


def market_intelligence_status() -> dict[str, Any]:
    refs = load_market_intelligence_refs()
    pillars = refs.get("pillars") or {}
    missing: list[str] = []
    for _key, item in pillars.items():
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if rel and not (REPO_ROOT / str(rel)).is_file():
            missing.append(str(rel))
    index = refs.get("index")
    if index and not (REPO_ROOT / str(index)).is_file():
        missing.append(str(index))
    return {
        "ok": bool(pillars) and not missing,
        "pillar_count": len(pillars),
        "missing_paths": missing,
        "index": index,
        "version": refs.get("version"),
    }


def pillar_of_week(now: datetime | None = None) -> dict[str, str] | None:
    """Rotate one pillar doc per ISO week for founder deep read."""
    refs = load_market_intelligence_refs()
    pillars = refs.get("pillars") or {}
    if not pillars:
        return None
    dt = now or datetime.now(UTC)
    week = dt.isocalendar().week
    key = PILLAR_ROTATION[week % len(PILLAR_ROTATION)]
    item = pillars.get(key)
    if not isinstance(item, dict):
        return None
    return {
        "id": key,
        "doc": str(item.get("path") or ""),
        "topic_ar": str(item.get("label_ar") or key),
    }


def build_market_intel_digest_block(now: datetime | None = None) -> dict[str, Any]:
    dt = now or datetime.now(UTC)
    st = market_intelligence_status()
    pow_doc = pillar_of_week(dt)
    is_friday = dt.weekday() == 4  # Monday=0
    refs = load_market_intelligence_refs()
    return {
        "status_ok": st["ok"],
        "pillar_of_week": pow_doc,
        "is_friday_review": is_friday,
        "friday_checklist": (
            "docs/commercial/MARKET_INTELLIGENCE_WEEKLY_REVIEW_CHECKLIST_AR.md"
            if is_friday
            else None
        ),
        "master_index": refs.get("index"),
        "implementation_playbook": "docs/commercial/MARKET_INTELLIGENCE_IMPLEMENTATION_PLAYBOOK_AR.md",
        "external_sources": refs.get("external_sources") or {},
    }
