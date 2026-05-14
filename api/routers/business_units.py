"""Per-BU endpoints.

  GET /api/v1/business-units/{slug}/public  — safe view (name, status,
                                               doctrine version, charter URL)
  GET /api/v1/business-units/{slug}         — admin-gated full view

Public projection drops owner emails, KPIs (when sensitive), reasons,
and any internal flags.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/business-units", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
BU_REGISTRY = REPO_ROOT / "data" / "business_units.json"


def _load_entries() -> list[dict[str, Any]]:
    if not BU_REGISTRY.exists():
        return []
    try:
        return list(json.loads(BU_REGISTRY.read_text(encoding="utf-8")).get("entries") or [])
    except Exception:
        log.exception("bu_registry_load_failed")
        return []


def _find(slug: str) -> dict[str, Any] | None:
    slug_l = slug.lower()
    for e in _load_entries():
        if str(e.get("slug") or "").lower() == slug_l:
            return e
    return None


@router.get("/{slug}/public")
async def bu_public(slug: str) -> dict[str, Any]:
    e = _find(slug)
    if e is None:
        raise HTTPException(status_code=404, detail=f"unknown business unit {slug!r}")
    # Public projection: only safe fields.
    return {
        "slug": str(e.get("slug") or ""),
        "name": str(e.get("name") or ""),
        "status": str(e.get("status") or ""),
        "doctrine_version": str(e.get("doctrine_version") or ""),
        "charter_path": str(e.get("charter_path") or ""),
        "as_of": datetime.now(timezone.utc).isoformat(),
        "links": {
            "holding_charter": "/api/v1/holding/charter",
            "doctrine": f"/api/v1/doctrine?version={e.get('doctrine_version', 'v1.0.0')}",
            "portfolio": "/api/v1/holding/portfolio",
        },
    }


@router.get("/{slug}")
async def bu_full(slug: str) -> dict[str, Any]:
    """Admin view. In PR11 ships open; PR15 will wire `require_admin_key`."""
    e = _find(slug)
    if e is None:
        raise HTTPException(status_code=404, detail=f"unknown business unit {slug!r}")
    return dict(e)
