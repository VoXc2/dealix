"""Search radar router — deterministic, no-LLM keyword priority feed.

Wraps ``auto_client_acquisition.self_growth_os.search_radar``. Two
endpoints:

  GET /api/v1/search-radar/status   — module + guardrails + disclosure
  GET /api/v1/search-radar/report   — full deterministic report

There is no POST: the radar is read-only and never auto-publishes.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.self_growth_os import search_radar

router = APIRouter(prefix="/api/v1/search-radar", tags=["search-radar"])


@router.get("/status")
async def search_radar_status() -> dict:
    """Module status + guardrails + data-source disclosure.

    Cheap probe: confirms the seed YAML is present and re-states that
    no external search API is being called.
    """
    return search_radar.status()


@router.get("/report")
async def search_radar_report() -> dict:
    """Full deterministic search-radar report.

    Composes weak-landing-page signals + the manually-curated seed list
    + the Service Activation Matrix bundle hints. Never calls a search
    API, never invents volume numbers.
    """
    try:
        return search_radar.build_search_radar()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
