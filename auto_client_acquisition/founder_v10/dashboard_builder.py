"""V11 — composer for the legacy ``/api/v1/founder/dashboard`` payload.

Wraps the existing section getters from ``api.routers.founder`` so any
single failure produces a typed degraded marker rather than a 5xx.

Output schema additions (over the legacy dashboard):
    - ``degraded`` (bool)
    - ``degraded_sections`` (list[str])
    - ``elapsed_ms`` (int) — populated by the cache layer
    - ``cache_hit`` (bool) — populated by the cache layer
    - ``source`` ("live" | "cache" | "degraded")
    - ``next_action_ar`` reflects degradation when present
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any


def _safe_section(
    name: str,
    fn: Callable[[], Any],
    *,
    default: Any,
    degraded_sections: list[str],
) -> Any:
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001 — never crash the dashboard
        degraded_sections.append(name)
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_message": str(exc)[:200],
            "_default": default,
        }


def build_dashboard_payload() -> dict[str, Any]:
    """Compose the founder dashboard payload using legacy section getters.

    Imports happen lazily so a missing optional module degrades cleanly.
    """
    from api.routers.founder import (
        _ceo_brief_top,
        _daily_loop_summary,
        _first_3_customers,
        _live_gates,
        _next_founder_action,
        _pending_approvals,
        _reliability,
        _service_counts,
        _unsafe_blocks,
        _weekly_summary,
    )

    degraded_sections: list[str] = []

    services = _safe_section(
        "services", _service_counts, default={}, degraded_sections=degraded_sections,
    )
    reliability = _safe_section(
        "reliability", _reliability, default={}, degraded_sections=degraded_sections,
    )
    live_gates = _live_gates()  # already error-wrapped internally
    daily_loop = _safe_section(
        "daily_loop",
        _daily_loop_summary,
        default={},
        degraded_sections=degraded_sections,
    )
    weekly_scorecard = _safe_section(
        "weekly_scorecard",
        _weekly_summary,
        default={},
        degraded_sections=degraded_sections,
    )
    ceo_brief = _safe_section(
        "ceo_brief", _ceo_brief_top, default={}, degraded_sections=degraded_sections,
    )
    first_3_customers = _safe_section(
        "first_3_customers",
        _first_3_customers,
        default={},
        degraded_sections=degraded_sections,
    )
    pending_approvals = _safe_section(
        "pending_approvals",
        _pending_approvals,
        default={"count": 0, "first_3": []},
        degraded_sections=degraded_sections,
    )
    unsafe_blocks = _safe_section(
        "unsafe_blocks",
        _unsafe_blocks,
        default={"count": 0, "names": []},
        degraded_sections=degraded_sections,
    )
    next_founder_action = _safe_section(
        "next_founder_action",
        _next_founder_action,
        default="no_action_today",
        degraded_sections=degraded_sections,
    )

    degraded = bool(degraded_sections)
    next_action_ar = (
        "راجع القسم المتأخر، لكن التشغيل الأساسي مستمر"
        if degraded
        else "استمر في الحلقة اليومية"
    )
    next_action_en = (
        "Review the degraded section; core operations continue."
        if degraded
        else "Continue the daily loop."
    )

    return {
        "schema_version": 2,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "لوحة المؤسس — Dealix",
        "title_en": "Founder Dashboard — Dealix",
        "services": services,
        "reliability": reliability,
        "live_gates": live_gates,
        "daily_loop": daily_loop,
        "weekly_scorecard": weekly_scorecard,
        "ceo_brief": ceo_brief,
        "first_3_customers": first_3_customers,
        "pending_approvals": pending_approvals,
        "unsafe_blocks": unsafe_blocks,
        "next_founder_action": next_founder_action,
        "next_action_ar": next_action_ar,
        "next_action_en": next_action_en,
        "degraded": degraded,
        "degraded_sections": degraded_sections,
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }
