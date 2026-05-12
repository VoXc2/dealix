"""
PostHog capture via HTTP (no heavy SDK dependency, async, fire-and-forget).

Env:
  POSTHOG_API_KEY     — project API key (phc_...)
  POSTHOG_HOST        — https://us.i.posthog.com (default) or https://eu.i.posthog.com
  POSTHOG_ENABLED     — optional, set to 'false' to disable without removing key

Usage:
  from dealix.analytics import capture_event, FUNNEL_EVENTS
  await capture_event(FUNNEL_EVENTS.LEAD_CAPTURED, distinct_id="lead_123",
                      properties={"source": "landing", "plan_interest": "growth"})
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import httpx

log = logging.getLogger(__name__)


class FUNNEL_EVENTS:  # noqa: N801  (namespace constants)
    """Canonical funnel event names — [object] [verb] format."""

    LANDING_VIEW = "landing viewed"
    DEMO_REQUESTED = "demo requested"
    LEAD_CAPTURED = "lead captured"
    LEAD_QUALIFIED = "lead qualified"
    MEETING_BOOKED = "meeting booked"
    PROPOSAL_SENT = "proposal sent"
    CHECKOUT_STARTED = "checkout started"
    PAYMENT_SUCCEEDED = "payment succeeded"
    PAYMENT_FAILED = "payment failed"
    DEAL_WON = "deal won"
    DEAL_LOST = "deal lost"
    WORKFLOW_FAILED = "workflow failed"


def _host() -> str:
    # Dealix project is hosted on PostHog US Cloud (project id 394094).
    # EU remains supported by setting POSTHOG_HOST=https://eu.i.posthog.com.
    return os.getenv("POSTHOG_HOST", "https://us.i.posthog.com").rstrip("/")


def _api_key() -> str:
    return os.getenv("POSTHOG_API_KEY", "")


def _enabled() -> bool:
    return os.getenv("POSTHOG_ENABLED", "true").lower() not in {"false", "0", "no", "off"}


async def capture_event(
    event: str,
    distinct_id: str,
    properties: dict[str, Any] | None = None,
    *,
    timeout: float = 3.0,
) -> bool:
    """Fire-and-forget event capture. Never raises — returns False on failure."""
    if not _enabled():
        return False
    api_key = _api_key()
    if not api_key:
        log.debug("posthog_not_configured event=%s", event)
        return False
    try:
        payload = {
            "api_key": api_key,
            "event": event,
            "distinct_id": str(distinct_id),
            "properties": {
                **(properties or {}),
                "$lib": "dealix-python",
                "source": (properties or {}).get("source", "backend"),
            },
        }
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.post(f"{_host()}/i/v0/e/", json=payload)
            return 200 <= r.status_code < 300
    except Exception as e:  # pragma: no cover
        log.warning("posthog_capture_failed event=%s err=%s", event, e)
        return False


_BACKGROUND_TASKS: set[asyncio.Task] = set()


def capture_event_sync(
    event: str, distinct_id: str, properties: dict[str, Any] | None = None
) -> None:
    """Schedule an async capture without awaiting (best-effort)."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            task = loop.create_task(capture_event(event, distinct_id, properties))
            _BACKGROUND_TASKS.add(task)
            task.add_done_callback(_BACKGROUND_TASKS.discard)
        else:
            loop.run_until_complete(capture_event(event, distinct_id, properties))
    except Exception as e:  # pragma: no cover
        log.debug("posthog_capture_sync_failed err=%s", e)


async def get_feature_flag(
    flag_key: str,
    distinct_id: str,
    *,
    default: bool | None = None,
    timeout: float = 3.0,
) -> bool | str | None:
    """Evaluate a PostHog feature flag.

    Returns:
        True / False / "<variant>" — when PostHog is configured AND
            answers definitively.
        `default` — when PostHog answers with no decision (typically
            None) or the request fails.

    Importantly, when no PostHog API key is configured we return
    None (not False) so callers that want to chain on env / static
    defaults can do so."""
    api_key = _api_key()
    if not api_key:
        return default
    try:
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.post(
                f"{_host()}/decide/?v=3",
                json={"api_key": api_key, "distinct_id": str(distinct_id)},
            )
            r.raise_for_status()
            data = r.json()
            flags = data.get("featureFlags", {}) or {}
            if flag_key not in flags:
                return default
            val = flags[flag_key]
            # Multivariate returns string; boolean for on/off
            return val
    except Exception as e:  # pragma: no cover
        log.warning("posthog_flag_failed flag=%s err=%s", flag_key, e)
        return default


# ── T3c — Surveys helpers ──────────────────────────────────────────


async def survey(
    *,
    survey_id: str,
    distinct_id: str,
    answer: Any,
    locale: str = "ar",
    metadata: dict[str, Any] | None = None,
    timeout: float = 3.0,
) -> bool:
    """Record a survey response back to PostHog (server-side path).

    Used when surveys fire from email links / backend events; the FE
    PostHog SDK handles the in-app path.
    """
    api_key = _api_key()
    if not api_key or not _enabled():
        return False
    props: dict[str, Any] = {
        "$survey_id": survey_id,
        "$survey_response": answer,
        "locale": locale,
    }
    if metadata:
        props.update(metadata)
    try:
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.post(
                f"{_host()}/capture/",
                json={
                    "api_key": api_key,
                    "event": "survey sent",
                    "distinct_id": distinct_id,
                    "properties": props,
                },
            )
            r.raise_for_status()
        return True
    except Exception:
        log.warning("posthog_survey_failed survey=%s", survey_id, exc_info=True)
        return False


async def list_survey_responses(
    survey_id: str, *, since: str | None = None, timeout: float = 10.0
) -> list[dict[str, Any]]:
    """Pull recent responses via the PostHog query API (personal-key auth).

    Returns [] when POSTHOG_PERSONAL_API_KEY / POSTHOG_PROJECT_ID are
    unset, so the founder's NPS dashboard degrades gracefully.
    """
    pkey = os.getenv("POSTHOG_PERSONAL_API_KEY", "").strip()
    project = os.getenv("POSTHOG_PROJECT_ID", "").strip()
    if not (pkey and project):
        return []
    try:
        where = [f"properties.$survey_id = '{survey_id}'"]
        if since:
            where.append(f"timestamp > '{since}'")
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.post(
                f"{_host()}/api/projects/{project}/query/",
                headers={"Authorization": f"Bearer {pkey}"},
                json={
                    "query": {
                        "kind": "EventsQuery",
                        "select": ["properties.$survey_response", "distinct_id", "timestamp"],
                        "event": "survey sent",
                        "where": where,
                        "orderBy": ["timestamp DESC"],
                        "limit": 500,
                    }
                },
            )
            r.raise_for_status()
            data = r.json()
        return [
            {"response": row[0], "distinct_id": row[1], "timestamp": row[2]}
            for row in (data.get("results") or [])
        ]
    except Exception:
        log.warning("posthog_survey_query_failed survey=%s", survey_id, exc_info=True)
        return []
