"""Blocker detection — defensive composition.

Scans for: degraded reliability, REVIEW_PENDING markers, unsafe action
attempts, and pending approvals over SLA. Each helper is wrapped so a
single layer probe failure can never break the whole brief.
"""
from __future__ import annotations

from auto_client_acquisition.founder_v10.schemas import Blocker


def _safe(fn, default):
    try:
        return fn()
    except Exception:  # noqa: BLE001
        return default


def _reliability_blockers() -> list[Blocker]:
    out: list[Blocker] = []
    try:
        from auto_client_acquisition.reliability_os import build_health_matrix
        matrix = build_health_matrix()
    except Exception:  # noqa: BLE001
        return out

    for sub in matrix.get("subsystems") or []:
        status = (sub.get("status") or "").lower()
        if status in {"degraded", "blocked", "down"}:
            severity = "blocked" if status in {"blocked", "down"} else "high"
            sub_name = str(sub.get("name", "unknown"))
            out.append(Blocker(
                id=f"reliability:{sub_name}",
                title_ar=f"خلل في النظام الفرعي: {sub_name}",
                title_en=f"subsystem degraded: {sub_name}",
                severity=severity,
                blocking_layer="reliability_os",
            ))
    return out


def _approval_blockers() -> list[Blocker]:
    out: list[Blocker] = []
    try:
        from auto_client_acquisition.approval_center import list_pending
        pending = list_pending()
    except Exception:  # noqa: BLE001
        return out

    if not pending:
        return out
    # Surface the count rather than per-card to keep the brief PII-free.
    out.append(Blocker(
        id="approvals:pending",
        title_ar=f"موافقات معلّقة: {len(pending)}",
        title_en=f"pending approvals: {len(pending)}",
        severity="medium" if len(pending) < 5 else "high",
        blocking_layer="approval_center",
    ))
    return out


def _review_pending_blockers() -> list[Blocker]:
    """Detect REVIEW_PENDING markers in the daily growth loop output."""
    out: list[Blocker] = []
    try:
        from auto_client_acquisition.self_growth_os import daily_growth_loop
        loop = daily_growth_loop.build_today() or {}
    except Exception:  # noqa: BLE001
        return out

    flat = repr(loop).upper()
    if "REVIEW_PENDING" in flat:
        out.append(Blocker(
            id="growth:review_pending",
            title_ar="هناك مسوّدات تنتظر المراجعة.",
            title_en="REVIEW_PENDING markers found in growth loop",
            severity="medium",
            blocking_layer="self_growth_os",
        ))
    return out


def _unsafe_action_blockers() -> list[Blocker]:
    out: list[Blocker] = []
    try:
        from auto_client_acquisition.agent_governance import (
            FORBIDDEN_TOOLS,
            ToolCategory,
        )
        # If LinkedIn or scraping ever leaves FORBIDDEN_TOOLS, the
        # founder must be alerted immediately.
        required = {ToolCategory.LINKEDIN_AUTOMATION, ToolCategory.SCRAPE_WEB}
        missing = required - set(FORBIDDEN_TOOLS)
        if missing:
            out.append(Blocker(
                id="governance:perimeter_breach",
                title_ar="خلل في حواجز الأدوات الممنوعة.",
                title_en=f"forbidden-tools perimeter breached: {sorted(t.value for t in missing)}",
                severity="blocked",
                blocking_layer="agent_governance",
            ))
    except Exception:  # noqa: BLE001
        pass
    return out


def find_blockers() -> list[Blocker]:
    """Aggregate all blocker sources, defensively."""
    blockers: list[Blocker] = []
    blockers.extend(_safe(_reliability_blockers, default=[]))
    blockers.extend(_safe(_approval_blockers, default=[]))
    blockers.extend(_safe(_review_pending_blockers, default=[]))
    blockers.extend(_safe(_unsafe_action_blockers, default=[]))
    return blockers
