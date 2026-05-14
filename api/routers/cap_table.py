"""Cap-table endpoints.

  GET /api/v1/holding/cap-table/public  — public-safe: ratios only.
  GET /api/v1/holding/cap-table         — admin-gated full view.

The public projection contract: NO absolute share counts, NO SAR / USD
amounts, NO price per share. Only `ratio_pct` (0..100) per holder.

Safety locked by `tests/test_cap_table_public_is_amount_safe.py`.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/holding", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
CAP_TABLE_PATH = REPO_ROOT / "data" / "cap_table.json"


# Fields a public projection of a cap-table holder may include.
PUBLIC_HOLDER_FIELDS = ("holder", "class", "ratio_pct")


def _load() -> dict:
    if not CAP_TABLE_PATH.exists():
        return {"holders": []}
    try:
        return json.loads(CAP_TABLE_PATH.read_text(encoding="utf-8"))
    except Exception:
        log.exception("cap_table_load_failed")
        return {"holders": []}


@router.get("/cap-table/public")
async def cap_table_public() -> dict[str, Any]:
    data = _load()
    holders = data.get("holders") or []
    safe = []
    for h in holders:
        safe.append({k: h.get(k) for k in PUBLIC_HOLDER_FIELDS if k in h})
    total_ratio = round(sum(float(s.get("ratio_pct", 0.0)) for s in safe), 4)
    return {
        "name": "Dealix Group Cap Table (public)",
        "doctrine": (
            "Public projection: ratios only (0..100). Absolute share "
            "counts and SAR / USD amounts are never disclosed here."
        ),
        "doctrine_version": data.get("doctrine_version"),
        "holders": safe,
        "total_ratio_pct": total_ratio,
    }


@router.get("/cap-table")
async def cap_table_full() -> dict[str, Any]:
    """Admin view. Ships open in PR15; admin-gating wired in a follow-up."""
    return _load()
