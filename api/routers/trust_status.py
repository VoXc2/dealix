"""Compact Trust Status endpoint — feeds Shields.io-style external badge mints.

  GET /api/v1/trust/status
      Returns a compact JSON suitable for `https://img.shields.io/endpoint`
      external mints. Stable shape, ETag header, public no-auth.

Response example:
    {
      "schemaVersion": 1,
      "label": "dealix doctrine",
      "message": "PASS",
      "color": "brightgreen",
      "namedLogo": "shield",
      "labelColor": "555",
      "as_of_commit": "<sha>",
      "ceo_complete": true,
      "score": "17/19"
    }

The endpoint reads `landing/assets/data/verifier-report.json` (rendered
by CI) — there is NO live computation here, only projection. Stable,
fast, and matches what the badges show.
"""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Response

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "verifier-report.json"


def _load_report() -> dict:
    if not REPORT_PATH.exists():
        return {"overall_pass": False, "ceo_complete": False, "systems": []}
    try:
        return json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        log.exception("trust_status_report_invalid_json")
        return {"overall_pass": False, "ceo_complete": False, "systems": []}


def _color_for(overall_pass: bool, passed: int, total: int) -> str:
    if overall_pass and passed == total:
        return "brightgreen"
    if total > 0 and passed / total >= (total - 2) / total:
        return "yellow"
    return "red"


@router.get("/trust/status")
async def trust_status() -> Response:
    """Compact Shields.io endpoint payload + ETag."""
    rpt = _load_report()
    systems = rpt.get("systems") or []
    passed = sum(1 for s in systems if s.get("passed"))
    total = len(systems) or 19
    overall = bool(rpt.get("overall_pass"))
    ceo = bool(rpt.get("ceo_complete"))

    payload: dict[str, Any] = {
        "schemaVersion": 1,
        "label": "dealix doctrine",
        "message": "PASS" if overall else f"{passed}/{total}",
        "color": _color_for(overall, passed, total),
        "namedLogo": "shield",
        "labelColor": "555",
        "ceo_complete": ceo,
        "score": f"{passed}/{total}",
    }

    body = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    etag = '"' + hashlib.sha256(body).hexdigest()[:24] + '"'

    return Response(
        content=body,
        media_type="application/json",
        headers={
            "ETag": etag,
            "Cache-Control": "public, max-age=300",
        },
    )
