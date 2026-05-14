"""Dealix Group — public holding endpoints.

  GET /api/v1/holding/charter   — public Charter snapshot pinned to commit SHA
  GET /api/v1/holding/portfolio — public-safe BU portfolio aggregate
  GET /api/v1/holding/board     — public board listing (names + roles only)

All three are public, no auth. The portfolio endpoint applies a
public-safe projection: counts by status, count by sector, last 5 BU
names + status. No revenue numbers, no client names, no contact details.

Locked by `tests/test_holding_endpoints.py`.
"""
from __future__ import annotations

import json
import logging
import subprocess
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/holding", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
CHARTER_PATH = REPO_ROOT / "docs" / "holding" / "HOLDING_CHARTER.md"
BU_REGISTRY = REPO_ROOT / "data" / "business_units.json"
BOARD_DOC = REPO_ROOT / "docs" / "holding" / "BOARD_OF_DIRECTORS.md"


@lru_cache(maxsize=1)
def _commit_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        log.warning("holding_charter_sha_lookup_failed", exc_info=True)
    return "unknown"


def _load_registry() -> dict:
    if not BU_REGISTRY.exists():
        return {"entries": []}
    try:
        return json.loads(BU_REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return {"entries": []}


@router.get("/charter")
async def holding_charter() -> dict[str, Any]:
    """Public Charter snapshot. Pinned to current commit SHA."""
    return {
        "name": "Dealix Group",
        "commit_sha": _commit_sha(),
        "charter_path": "docs/holding/HOLDING_CHARTER.md",
        "operating_principles": [
            "Cash now.",
            "Proof always.",
            "Governance by default.",
            "Productize repetition.",
        ],
        "holding_non_negotiables": [
            "Zero unverifiable units.",
            "Doctrine version pinning at the group level.",
            "Every BU publishes a Trust Pack before first invoice.",
            "No BU is killed quietly — board memo required.",
        ],
        "links": {
            "portfolio": "/api/v1/holding/portfolio",
            "board": "/api/v1/holding/board",
            "doctrine": "/api/v1/doctrine",
            "promise": "/api/v1/dealix-promise",
        },
        "disclaimer": (
            "This endpoint publishes the Dealix Group operating charter. "
            "It is doctrine, not legal text."
        ),
    }


@router.get("/portfolio")
async def holding_portfolio() -> dict[str, Any]:
    """Public-safe BU portfolio aggregate. No client/revenue data."""
    data = _load_registry()
    entries = data.get("entries") or []

    by_status: Counter[str] = Counter()
    by_sector: Counter[str] = Counter()
    by_doctrine: Counter[str] = Counter()

    for e in entries:
        by_status[str(e.get("status") or "unknown")] += 1
        by_sector[str(e.get("sector") or "unspecified")] += 1
        by_doctrine[str(e.get("doctrine_version") or "unpublished")] += 1

    # Last 5 BU names + status only — no owner, no charter path, no
    # internal flags, no reason text.
    recent = []
    for e in entries[-5:]:
        recent.append({
            "slug": str(e.get("slug") or ""),
            "name": str(e.get("name") or ""),
            "status": str(e.get("status") or ""),
        })

    return {
        "name": "Dealix Group",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "count": len(entries),
        "by_status": dict(by_status),
        "by_sector": dict(by_sector),
        "by_doctrine_version": dict(by_doctrine),
        "recent_units": recent,
        "doctrine": (
            "Public projection: BU names, status, and sector only. No "
            "owner emails, no revenue, no client lists, no contact "
            "details."
        ),
    }


@router.get("/board")
async def holding_board() -> dict[str, Any]:
    """Public board listing.

    PR10 ships without `data/board_of_directors.json` (added in PR15);
    in that interim state the endpoint returns the minimum public
    contract so prospects know the board exists.
    """
    board_data_path = REPO_ROOT / "data" / "board_of_directors.json"
    members: list[dict[str, Any]] = []
    if board_data_path.exists():
        try:
            d = json.loads(board_data_path.read_text(encoding="utf-8"))
            for m in (d.get("members") or []):
                # Strip every contact-detail field defensively.
                members.append({
                    "name": str(m.get("name") or ""),
                    "role": str(m.get("role") or ""),
                    "independent": bool(m.get("independent", False)),
                })
        except Exception:
            log.exception("holding_board_load_failed")

    return {
        "name": "Dealix Group Board",
        "members": members,
        "doctrine": (
            "Public projection: name, role, independence flag only. "
            "No emails, no phone numbers, no addresses."
        ),
        "charter_path": "docs/holding/BOARD_CHARTER.md",
    }
