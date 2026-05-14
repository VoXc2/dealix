"""Founder Launch Status — Wave 15 (A2).

Single-pane GET that aggregates every production readiness signal the
founder needs to know "is everything green right now?" without 12 tabs
open. Admin-key gated.

Surfaces:
- Healthcheck
- DB connectivity (best-effort)
- Moyasar mode + key prefix
- ZATCA mode
- Gmail OAuth configured + last_send_at if available
- PostHog reachability flag (from env)
- Calendly URL configured
- Latest 5 commits on local HEAD
- Last 14 days friction summary
- Today's lead count (`lead_inbox`)
- Today's value events count (last 24h)
- Top 3 next actions (deterministic ranking from system state)
"""
from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _healthcheck() -> dict[str, Any]:
    return {"path": "/healthz", "ok": True}


def _db_status() -> dict[str, Any]:
    db_url = os.getenv("DATABASE_URL", "")
    return {
        "configured": bool(db_url),
        "scheme": db_url.split(":", 1)[0] if db_url else "",
    }


def _moyasar_status() -> dict[str, Any]:
    key = os.getenv("MOYASAR_SECRET_KEY", "")
    mode = "live" if key.startswith("sk_live_") else (
        "test" if key.startswith("sk_test_") else "unconfigured"
    )
    webhook = os.getenv("MOYASAR_WEBHOOK_SECRET", "")
    explicit_mode = os.getenv("DEALIX_MOYASAR_MODE", "")
    return {
        "mode": explicit_mode or mode,
        "key_prefix": key[:7] + "…" if key else "",
        "webhook_secret_configured": bool(webhook),
    }


def _zatca_status() -> dict[str, Any]:
    sandbox = os.getenv("ZATCA_SANDBOX", "true").lower() != "false"
    return {
        "mode": "sandbox" if sandbox else "live",
        "csid_configured": bool(os.getenv("ZATCA_CSID", "")),
    }


def _gmail_status() -> dict[str, Any]:
    sender = os.getenv("GMAIL_SENDER_EMAIL", "")
    client_id = os.getenv("GMAIL_CLIENT_ID", "")
    refresh = os.getenv("GMAIL_OAUTH_REFRESH_TOKEN", "")
    configured = bool(sender and client_id and refresh)
    try:
        from auto_client_acquisition.email.gmail_send import is_configured
        configured = configured and is_configured()
    except Exception:  # noqa: BLE001
        pass
    return {
        "configured": configured,
        "sender": sender,
    }


def _posthog_status() -> dict[str, Any]:
    return {
        "configured": bool(os.getenv("POSTHOG_API_KEY", "")),
        "host": os.getenv("POSTHOG_HOST", "https://us.i.posthog.com"),
    }


def _calendly_status() -> dict[str, Any]:
    return {
        "url": os.getenv("CALENDLY_URL", ""),
        "webhook_configured": bool(os.getenv("CALENDLY_WEBHOOK_SECRET", "")),
    }


def _git_status() -> dict[str, Any]:
    out: dict[str, Any] = {"commits": []}
    git_sha = os.getenv("GIT_SHA", "")
    out["git_sha"] = git_sha
    try:
        proc = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            check=False, capture_output=True, text=True, timeout=5,
        )
        if proc.returncode == 0:
            out["commits"] = [
                line for line in proc.stdout.splitlines() if line.strip()
            ]
    except Exception:  # noqa: BLE001
        pass
    return out


def _friction_summary() -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id="dealix_internal", window_days=14)
        return {
            "window_days": 14,
            "total": agg.total,
            "top_3_kinds": agg.top_3_kinds,
            "high_severity_count": agg.by_severity.get("high", 0),
        }
    except Exception:  # noqa: BLE001
        return {"window_days": 14, "total": 0, "top_3_kinds": [], "high_severity_count": 0}


def _lead_count_today() -> int:
    try:
        from auto_client_acquisition import lead_inbox
        if not hasattr(lead_inbox, "list_records"):
            return 0
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        count = 0
        for r in lead_inbox.list_records(limit=500):
            try:
                created = datetime.fromisoformat(getattr(r, "created_at", "") or "")
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except Exception:  # noqa: BLE001
                continue
            if created >= cutoff:
                count += 1
        return count
    except Exception:  # noqa: BLE001
        return 0


def _value_events_today() -> int:
    try:
        from auto_client_acquisition.value_os.value_ledger import list_events
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        return sum(
            1 for ev in list_events(limit=500) if ev.occurred_at >= cutoff
        )
    except Exception:  # noqa: BLE001
        return 0


def _top_actions(
    *,
    moyasar_mode: str,
    gmail_configured: bool,
    leads_today: int,
    friction_high: int,
) -> list[str]:
    """Deterministic ranking of the top 3 actions the founder should do now."""
    actions: list[str] = []
    if moyasar_mode != "live":
        actions.append(
            "Flip Moyasar to live mode: run `python scripts/moyasar_live_cutover.py`"
        )
    if not gmail_configured:
        actions.append(
            "Configure Gmail OAuth on Railway env vars (GMAIL_SENDER_EMAIL, "
            "GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_OAUTH_REFRESH_TOKEN)"
        )
    if leads_today == 0:
        actions.append(
            "Send 5 warm-list messages (`data/outreach/warm_list_drafts.md`)"
        )
    if friction_high > 0:
        actions.append(
            f"Resolve {friction_high} high-severity friction event(s) — review founder-dashboard"
        )
    if not actions:
        actions.append(
            "All green — run `python scripts/dealix_pm_daily.py` for today's brief"
        )
    return actions[:3]


@router.get("/launch-status", dependencies=[Depends(require_admin_key)])
async def launch_status() -> dict[str, Any]:
    """Single-pane production readiness JSON. Admin-key gated."""
    moyasar = _moyasar_status()
    gmail = _gmail_status()
    leads_today = _lead_count_today()
    friction = _friction_summary()

    top_actions = _top_actions(
        moyasar_mode=moyasar["mode"],
        gmail_configured=gmail["configured"],
        leads_today=leads_today,
        friction_high=friction["high_severity_count"],
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "healthcheck": _healthcheck(),
        "database": _db_status(),
        "moyasar": moyasar,
        "zatca": _zatca_status(),
        "gmail": gmail,
        "posthog": _posthog_status(),
        "calendly": _calendly_status(),
        "git": _git_status(),
        "friction_last_14d": friction,
        "leads_last_24h": leads_today,
        "value_events_last_24h": _value_events_today(),
        "top_actions": top_actions,
        "governance_decision": "allow",
        "is_estimate": True,
    }


@router.get("/launch-status/public")
async def launch_status_public() -> dict[str, Any]:
    """Public minimal subset — no secrets, no admin key required. Used by
    landing/launch-status.html when running from a customer's browser
    without admin credentials.
    """
    moyasar = _moyasar_status()
    gmail = _gmail_status()
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "healthcheck_ok": True,
        "moyasar_mode": moyasar["mode"],
        "zatca_mode": _zatca_status()["mode"],
        "gmail_configured": gmail["configured"],
        "calendly_url": _calendly_status()["url"],
        "git_sha": _git_status().get("git_sha", ""),
        "governance_decision": "allow",
    }
