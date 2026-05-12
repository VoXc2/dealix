"""
Founder-only NPS dashboard data endpoints.

Endpoints (admin-scoped):
    GET /api/v1/admin/nps/responses?survey_id=...&since=...

Reads from PostHog Surveys via dealix/analytics/posthog_client.list_survey_responses.
Inert (returns empty list) when POSTHOG_PERSONAL_API_KEY + POSTHOG_PROJECT_ID
are missing.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from core.logging import get_logger
from dealix.analytics.posthog_client import list_survey_responses

router = APIRouter(prefix="/api/v1/admin/nps", tags=["admin", "nps"])
log = get_logger(__name__)


@router.get("/responses")
async def list_nps_responses(
    request: Request,
    survey_id: str = Query(default="nps_day14"),
    since: str | None = Query(default=None),
) -> dict[str, Any]:
    is_admin = bool(getattr(request.state, "is_super_admin", False))
    api_key = request.headers.get("x-api-key", "")
    admin_keys = {k.strip() for k in os.getenv("ADMIN_API_KEYS", "").split(",") if k.strip()}
    if not is_admin and api_key not in admin_keys:
        raise HTTPException(403, "admin_only")
    items = await list_survey_responses(survey_id, since=since)
    return {"survey_id": survey_id, "count": len(items), "items": items}
