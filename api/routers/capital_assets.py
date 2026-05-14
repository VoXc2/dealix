"""Public Capital Assets endpoint.

A safe public view of the Dealix Capital Asset Library. Prospects,
partners, regulators, and auditors can see the count and types of
capital assets Dealix has registered, without ever seeing:
  - client names or IDs
  - customer-owned data
  - pricing, contracts, or revenue figures
  - raw evidence (which may contain PII)
  - free-text description (commercial-confidential by default)

  GET /api/v1/capital-assets/public
      Returns: {
        count, by_type, recent_titles_safe, generated_at,
        source, disclaimer
      }

The endpoint is public (no auth). The projection logic is what makes
this safe — see `_safe_projection()` and the locking test
`tests/test_public_capital_assets_are_safe.py`.
"""
from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.capital_os.asset_types import CapitalAssetType

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
CAPITAL_ASSET_INDEX = REPO_ROOT / "data" / "capital_asset_index.json"


# Fields that must NEVER appear in a public projection of a capital asset.
PUBLIC_FORBIDDEN_FIELDS: frozenset[str] = frozenset({
    "client_id",
    "client_name",
    "project_id",
    "project_name",
    "evidence",
    "description",
    "raw_evidence",
    "email",
    "phone",
    "price_sar",
    "amount_sar",
    "revenue",
    "contract",
    "git_author",
    "owner_email",
})


def _load_index() -> dict[str, Any]:
    if not CAPITAL_ASSET_INDEX.exists():
        return {"entries": []}
    try:
        return json.loads(CAPITAL_ASSET_INDEX.read_text(encoding="utf-8"))
    except Exception:
        log.exception("capital_asset_index_load_failed")
        return {"entries": []}


def _safe_projection(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Reduce a raw entry list to the safe public projection.

    No client identifiers. No raw evidence. No descriptions. Only:
      - count
      - count by CapitalAssetType
      - the last N safe titles, redacted to title-case asset_type labels
        when the entry has no `title` field
    """
    by_type: Counter[str] = Counter()
    safe_recent: list[dict[str, str]] = []
    valid_types = {t.value for t in CapitalAssetType}

    for entry in entries:
        asset_type = str(entry.get("asset_type") or "").strip()
        if asset_type not in valid_types:
            continue
        by_type[asset_type] += 1

    # Take the last 10 entries in order, safe-fielded.
    for entry in entries[-10:]:
        asset_type = str(entry.get("asset_type") or "").strip()
        if asset_type not in valid_types:
            continue
        title = entry.get("title")
        # Strip the title down to a short, label-safe summary.
        if isinstance(title, str) and title.strip():
            safe_title = title.strip()[:80]
        else:
            safe_title = asset_type.replace("_", " ").title()
        safe_recent.append({
            "asset_type": asset_type,
            "title_safe": safe_title,
        })

    return {
        "count": int(sum(by_type.values())),
        "by_type": dict(by_type),
        "recent_titles_safe": safe_recent,
    }


@router.get("/capital-assets/public")
async def capital_assets_public() -> dict[str, Any]:
    """Public-safe projection of the Capital Asset Library."""
    index = _load_index()
    entries = index.get("entries") or []
    projection = _safe_projection(entries)
    return {
        **projection,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "data/capital_asset_index.json",
        "disclaimer": (
            "This is a safe public projection. No client names, no "
            "customer data, no pricing, no evidence content. Raw "
            "capital assets are accessible only inside Dealix's "
            "private workspaces."
        ),
    }
