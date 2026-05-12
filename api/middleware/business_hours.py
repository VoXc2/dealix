"""
Saudi business-hours middleware (opt-in).

When `BUSINESS_HOURS_ENFORCE=1`, requests tagged as "non-urgent
notification triggers" (header `X-Dealix-Intent: notify`) are delayed
until Sun–Thu 09:00–18:00 Asia/Riyadh by responding with `425 Too Early`
and a `Retry-After` hint.

The middleware never blocks customer-facing reads or writes — only
explicitly-tagged notification triggers. This is a guardrail, not a
firewall: the caller chooses to set the header. Existing transactional
flows (invite emails, billing receipts) do NOT set the header and are
unaffected.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from core.logging import get_logger

log = get_logger(__name__)

_RIYADH_OFFSET = timedelta(hours=3)


def _enabled() -> bool:
    return os.getenv("BUSINESS_HOURS_ENFORCE", "").strip().lower() in {"1", "true", "yes"}


def _is_business_hours_now() -> bool:
    now_utc = datetime.now(timezone.utc)
    riyadh = now_utc + _RIYADH_OFFSET
    weekday = riyadh.weekday()  # Mon=0 … Sun=6
    # Sun–Thu => Python weekday 6,0,1,2,3.
    if weekday in {4, 5}:  # Fri (4) or Sat (5)
        return False
    return 9 <= riyadh.hour < 18


def _next_open_window_iso() -> str:
    now_utc = datetime.now(timezone.utc)
    riyadh = now_utc + _RIYADH_OFFSET
    while True:
        weekday = riyadh.weekday()
        if weekday in {4, 5}:
            riyadh = (riyadh + timedelta(days=1)).replace(hour=9, minute=0, second=0)
            continue
        if riyadh.hour >= 18:
            riyadh = (riyadh + timedelta(days=1)).replace(hour=9, minute=0, second=0)
            continue
        if riyadh.hour < 9:
            riyadh = riyadh.replace(hour=9, minute=0, second=0)
        break
    return (riyadh - _RIYADH_OFFSET).isoformat()


class BusinessHoursMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Any
    ) -> Response:
        if not _enabled():
            return await call_next(request)
        intent = request.headers.get("x-dealix-intent", "").lower()
        if intent != "notify":
            return await call_next(request)
        if _is_business_hours_now():
            return await call_next(request)
        next_open = _next_open_window_iso()
        log.info(
            "business_hours_deferred",
            path=request.url.path,
            next_open_utc=next_open,
        )
        return JSONResponse(
            status_code=425,
            content={
                "detail": "outside_business_hours",
                "next_open_utc": next_open,
                "policy": "Sun-Thu 09:00-18:00 Asia/Riyadh",
            },
            headers={"Retry-After": "3600"},
        )
