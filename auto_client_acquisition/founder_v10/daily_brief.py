"""Founder v10 daily brief — composes everything.

Defensive: every helper is wrapped in try/except so this module NEVER
crashes the API. PII is never embedded — only counts, statuses, and
already-redacted snippets from the underlying layers.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_v10.blockers import find_blockers
from auto_client_acquisition.founder_v10.cost_summary import summarize_cost
from auto_client_acquisition.founder_v10.evidence_summary import summarize_evidence
from auto_client_acquisition.founder_v10.next_actions import compute_next_action
from auto_client_acquisition.founder_v10.schemas import DailyBrief


def _safe(fn, default):
    try:
        return fn()
    except Exception:
        return default


def _service_counts() -> dict[str, Any]:
    from auto_client_acquisition.self_growth_os import service_activation_matrix
    return service_activation_matrix.counts()


def _reliability_register() -> list[dict[str, Any]]:
    from auto_client_acquisition.reliability_os import build_health_matrix
    matrix = build_health_matrix()
    out: list[dict[str, Any]] = []
    for sub in matrix.get("subsystems") or []:
        status = sub.get("status") or "unknown"
        out.append({
            "id": f"reliability:{sub.get('name', 'unknown')}",
            "risk_type": "reliability",
            "level": _level_from_status(str(status)),
            "detected_in": "auto_client_acquisition.reliability_os",
            "action": "investigate_subsystem",
            "subsystem": sub.get("name"),
            "status": status,
        })
    return out


def _level_from_status(status: str) -> str:
    s = status.lower()
    if s in {"down", "blocked"}:
        return "blocked"
    if s == "degraded":
        return "high"
    if s == "warning":
        return "medium"
    return "low"


def _top_decisions() -> list[dict[str, Any]]:
    from auto_client_acquisition.self_growth_os import daily_growth_loop
    loop = daily_growth_loop.build_today() or {}
    decisions = loop.get("decisions") or []
    out: list[dict[str, Any]] = []
    for d in decisions[:3]:
        if isinstance(d, dict):
            out.append(d)
        else:
            out.append({"title": str(d)})
    return out


def _safety_eval_count() -> dict[str, Any]:
    """Optional: if safety_v10 ships, surface the eval count.

    Returns a dict with ``status`` and ``count`` so the brief stays
    consistent across configurations.
    """
    try:
        from auto_client_acquisition import safety_v10  # type: ignore[attr-defined]
        if hasattr(safety_v10, "last_eval_count"):
            return {
                "status": "available",
                "count": int(safety_v10.last_eval_count() or 0),
            }
    except Exception:
        pass
    return {"status": "no eval run today", "count": 0}


def _build_summary(
    service_counts: dict[str, Any],
    decisions: list[dict[str, Any]],
    blockers: list,
) -> tuple[str, str]:
    total_services = service_counts.get("total", 0) if isinstance(service_counts, dict) else 0
    summary_ar = (
        f"تقرير اليوم: {total_services} خدمة، "
        f"{len(decisions)} قرار من حلقة النمو، "
        f"{len(blockers)} حاجز نشط."
    )
    summary_en = (
        f"Today: {total_services} services tracked, "
        f"{len(decisions)} decisions from growth loop, "
        f"{len(blockers)} active blockers."
    )
    return summary_ar, summary_en


def build_daily_brief() -> DailyBrief:
    """Compose the bilingual founder daily brief."""
    service_counts = _safe(_service_counts, default={"total": 0})
    risk_register = _safe(_reliability_register, default=[])
    decisions = _safe(_top_decisions, default=[])
    evidence = _safe(lambda: summarize_evidence(limit=10), default={
        "total": 0, "by_type": {}, "by_month": {}, "note": "unavailable",
    })
    cost = _safe(lambda: summarize_cost(period_days=7), default={
        "period_days": 7, "total_usd": 0.0, "by_provider": {},
        "note": "no cost data yet",
    })
    safety = _safe(_safety_eval_count, default={"status": "no eval run today", "count": 0})

    blockers = _safe(find_blockers, default=[])
    blocker_titles: list[str] = []
    for b in blockers:
        # Defensive: blockers may be a list of Blocker or dict on error
        if hasattr(b, "title_en"):
            blocker_titles.append(b.title_en or b.id)
        elif isinstance(b, dict):
            blocker_titles.append(str(b.get("title_en") or b.get("id") or ""))

    nxt = _safe(compute_next_action, default={
        "next_action_ar": "",
        "next_action_en": "",
    })

    summary_ar, summary_en = _build_summary(service_counts, decisions, blocker_titles)

    evidence_summary = dict(evidence)
    evidence_summary["safety_eval"] = safety
    evidence_summary["service_counts"] = service_counts

    return DailyBrief(
        summary_ar=summary_ar,
        summary_en=summary_en,
        top_3_decisions=decisions,
        cost_summary_usd=float(cost.get("total_usd", 0.0) or 0.0),
        risk_register=risk_register,
        evidence_summary=evidence_summary,
        blockers=blocker_titles,
        next_action_ar=str(nxt.get("next_action_ar", "")),
        next_action_en=str(nxt.get("next_action_en", "")),
    )
