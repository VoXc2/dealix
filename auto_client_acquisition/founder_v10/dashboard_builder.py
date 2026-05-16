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
    The section getters are independent read-only aggregations, each
    error-isolated by ``_safe_section`` — they are run concurrently so the
    cold-cache build is bounded by the slowest section, not their sum.
    """
    from concurrent.futures import ThreadPoolExecutor

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

    degraded_sections: list[str] = []  # list.append is atomic under the GIL

    # (payload key, getter, default-on-error)
    section_specs: list[tuple[str, Callable[[], Any], Any]] = [
        ("services", _service_counts, {}),
        ("reliability", _reliability, {}),
        ("daily_loop", _daily_loop_summary, {}),
        ("weekly_scorecard", _weekly_summary, {}),
        ("ceo_brief", _ceo_brief_top, {}),
        ("first_3_customers", _first_3_customers, {}),
        ("pending_approvals", _pending_approvals, {"count": 0, "first_3": []}),
        ("unsafe_blocks", _unsafe_blocks, {"count": 0, "names": []}),
        ("next_founder_action", _next_founder_action, "no_action_today"),
    ]

    with ThreadPoolExecutor(max_workers=len(section_specs) + 1) as pool:
        section_futures = {
            key: pool.submit(
                _safe_section, key, fn,
                default=default, degraded_sections=degraded_sections,
            )
            for key, fn, default in section_specs
        }
        live_gates_future = pool.submit(_live_gates)  # error-wrapped internally
        section = {key: fut.result() for key, fut in section_futures.items()}
        live_gates = live_gates_future.result()

    services = section["services"]
    reliability = section["reliability"]
    daily_loop = section["daily_loop"]
    weekly_scorecard = section["weekly_scorecard"]
    ceo_brief = section["ceo_brief"]
    first_3_customers = section["first_3_customers"]
    pending_approvals = section["pending_approvals"]
    unsafe_blocks = section["unsafe_blocks"]
    next_founder_action = section["next_founder_action"]

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
