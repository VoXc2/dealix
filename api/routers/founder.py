"""Founder v5 — aggregate read-only dashboard.

Composes one bilingual snapshot across the 12 v5 layers + the
self-growth perimeter so the founder can see the full state of the
business in one HTTP call instead of 12. Read-only; never mutates
state; never sends a message; never charges anything.

Designed to be safe to call from a phone. Bilingual fields where
human-facing.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _safe(fn, *, default: Any) -> Any:
    """Run fn(); on any error, return a typed error blob.

    The dashboard MUST stay reachable even if one layer is mid-deploy
    or has a probe failure — so each section is wrapped.
    """
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001 — never crash the dashboard
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_message": str(exc)[:200],
            "_default": default,
        }


def _service_counts() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import (
        service_activation_matrix,
    )
    return service_activation_matrix.counts()


def _reliability() -> dict[str, Any]:
    from auto_client_acquisition.reliability_os import build_health_matrix
    matrix = build_health_matrix()
    # Trim to the founder-relevant fields — overall + status counts +
    # a one-line status per subsystem. Full matrix still lives at
    # /api/v1/reliability/health-matrix for deep inspection.
    subs = [
        {"name": s.get("name"), "status": s.get("status")}
        for s in matrix.get("subsystems") or []
    ]
    return {
        "overall_status": matrix.get("overall_status"),
        "counts": matrix.get("counts"),
        "subsystems": subs,
    }


def _live_gates() -> dict[str, Any]:
    """All live-action gates. Every value should be `BLOCKED` on a
    healthy production deploy. The dashboard surfaces this so the
    founder catches misconfiguration immediately."""
    out: dict[str, str] = {}

    # 1. Live charge — finance_os
    try:
        from auto_client_acquisition.finance_os import is_live_charge_allowed
        live = is_live_charge_allowed()
        out["live_charge"] = (
            "BLOCKED" if not live.get("allowed") else "ALLOWED"
        )
    except BaseException as exc:  # noqa: BLE001
        out["live_charge"] = f"UNKNOWN ({type(exc).__name__})"

    # 2. WhatsApp live send — settings flag
    try:
        from core.config.settings import get_settings
        flag = getattr(get_settings(), "whatsapp_allow_live_send", False)
        out["whatsapp_live_send"] = "BLOCKED" if not flag else "ALLOWED"
    except BaseException as exc:  # noqa: BLE001
        out["whatsapp_live_send"] = f"UNKNOWN ({type(exc).__name__})"

    # 3. Email live send — no flag exists, so always BLOCKED
    out["email_live_send"] = "BLOCKED (no flag exists by design)"

    # 4. LinkedIn / scraping — agent_governance forbids
    try:
        from auto_client_acquisition.agent_governance import (
            FORBIDDEN_TOOLS,
            ToolCategory,
        )
        ok = (
            ToolCategory.LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS
            and ToolCategory.SCRAPE_WEB in FORBIDDEN_TOOLS
        )
        out["linkedin_and_scraping"] = "BLOCKED" if ok else "MISCONFIGURED"
    except BaseException as exc:  # noqa: BLE001
        out["linkedin_and_scraping"] = f"UNKNOWN ({type(exc).__name__})"

    return out


def _daily_loop_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today()
    decisions = loop.get("decisions") or []
    return {
        "decisions_count": len(decisions),
        "top_3_decisions": decisions[:3],
        "open_loops": loop.get("decline_or_open_loops", []),
    }


def _weekly_summary() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard
    return weekly_growth_scorecard.build_scorecard()


def _ceo_brief_top() -> dict[str, Any]:
    from auto_client_acquisition.role_command_os import (
        RoleName,
        build_role_brief,
    )
    brief = build_role_brief(RoleName.CEO)
    return {
        "summary_ar": brief.summary_ar,
        "summary_en": brief.summary_en,
        "top_decisions": [d.model_dump() for d in brief.top_decisions[:3]],
        "next_action_ar": brief.next_action_ar,
        "next_action_en": brief.next_action_en,
    }


@router.get("/status")
async def status() -> dict:
    return {
        "module": "founder",
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
        "endpoints": ["/dashboard"],
    }


@router.get("/dashboard")
async def dashboard() -> dict:
    """Single bilingual snapshot of the entire v5 stack.

    Read-only. Never sends, never charges, never writes. Safe to
    call from a phone. Composes:

      - service_activation_matrix.counts()
      - reliability_os.build_health_matrix() (trimmed)
      - finance_os.is_live_charge_allowed() + 3 other live gates
      - daily_growth_loop.build_today() (top 3 only)
      - weekly_growth_scorecard
      - role_command_os CEO brief (top 3 decisions only)
    """
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "لوحة المؤسس — Dealix",
        "title_en": "Founder Dashboard — Dealix",
        "services": _safe(_service_counts, default={}),
        "reliability": _safe(_reliability, default={}),
        "live_gates": _live_gates(),  # never errors — internally wrapped
        "daily_loop": _safe(_daily_loop_summary, default={}),
        "weekly_scorecard": _safe(_weekly_summary, default={}),
        "ceo_brief": _safe(_ceo_brief_top, default={}),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }
