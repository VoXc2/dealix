"""Compose the weekly executive report.

Pure read-only orchestration over existing layers. Defensive: every
upstream call is wrapped so a single failure produces a degraded
field rather than crashing the whole report. NEVER calls an LLM,
NEVER opens a network connection, NEVER persists.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.executive_reporting.decision_summary import (
    decision_summary,
)
from auto_client_acquisition.executive_reporting.next_week_plan import (
    next_week_plan,
)
from auto_client_acquisition.executive_reporting.proof_summary import (
    proof_summary,
)
from auto_client_acquisition.executive_reporting.risk_summary import (
    risk_summary,
)
from auto_client_acquisition.executive_reporting.schemas import WeeklyReport


_FORBIDDEN_TOKENS = ("نضمن", "guaranteed", "blast", "scrape")


def _safe(fn, *args, default=None, **kwargs):
    """Wrap a callable so any exception becomes ``default``."""
    try:
        return fn(*args, **kwargs)
    except Exception:  # noqa: BLE001 — defensive composition
        return default


def _scrub(text: str) -> str:
    """Remove forbidden marketing tokens from a string."""
    if not isinstance(text, str):
        return ""
    out = text
    for tok in _FORBIDDEN_TOKENS:
        out = out.replace(tok, "[redacted]")
    return out


def _build_executive_summary(
    *,
    counts: dict[str, Any],
    proof: dict[str, Any],
    risks: list[str],
    decisions: list[dict[str, Any]],
) -> tuple[str, str]:
    live = counts.get("live", 0) if isinstance(counts, dict) else 0
    pilot = counts.get("pilot", 0) if isinstance(counts, dict) else 0
    partial = counts.get("partial", 0) if isinstance(counts, dict) else 0
    total = counts.get("total", 0) if isinstance(counts, dict) else 0
    proof_total = int(proof.get("total", 0) or 0)
    risk_count = len(risks)
    decision_count = len(decisions)

    summary_ar = (
        "ملخص تنفيذي أسبوعي: "
        f"{live} خدمات حية، {pilot} تجريبية، {partial} جزئية من أصل {total}. "
        f"تم تسجيل {proof_total} حدث إثبات. "
        f"عدد المخاطر المرصودة: {risk_count}. "
        f"قرارات بانتظار المؤسس: {decision_count}. "
        "لا إرسال خارجي، لا ادعاءات تسويقية، الموافقة البشرية مطلوبة قبل أي نشر."
    )
    summary_en = (
        "Weekly executive summary: "
        f"{live} live, {pilot} pilot, {partial} partial out of {total} services. "
        f"{proof_total} proof events recorded. "
        f"Open risks: {risk_count}. "
        f"Founder decisions pending: {decision_count}. "
        "No external send, no marketing claims, human approval required before any publish."
    )
    return summary_ar, summary_en


def _render_markdown_ar(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Dealix — التقرير التنفيذي الأسبوعي")
    if report.get("week_label"):
        lines.append(f"_الأسبوع: {report['week_label']}_")
    lines.append(f"_تم التوليد: {report.get('generated_at')}_")
    lines.append("")
    lines.append("## الملخص التنفيذي")
    lines.append(report.get("executive_summary_ar", ""))
    lines.append("")
    lines.append("## حركة الإيرادات")
    pipe = report.get("pipeline") or {}
    counts = pipe.get("counts") or {}
    if counts:
        lines.append(
            f"- خدمات حية: {counts.get('live', 0)} | "
            f"تجريبية: {counts.get('pilot', 0)} | "
            f"جزئية: {counts.get('partial', 0)} | "
            f"الإجمالي: {counts.get('total', 0)}"
        )
    else:
        lines.append("- لا بيانات حركة متاحة")
    lines.append("")
    lines.append("## الإثباتات (مجهولة الهوية)")
    proof = report.get("proof") or {}
    lines.append(f"- إجمالي الأحداث: {proof.get('total', 0)}")
    by_type = proof.get("by_type") or {}
    for tp, ct in list(by_type.items())[:6]:
        lines.append(f"  - {tp}: {ct}")
    lines.append("")
    lines.append("## المخاطر")
    risks = report.get("risks") or []
    if risks:
        for r in risks[:8]:
            lines.append(f"- {r}")
    else:
        lines.append("- لا مخاطر مرصودة")
    lines.append("")
    lines.append("## القرارات المطلوبة من المؤسس")
    decisions = report.get("decisions") or []
    if decisions:
        for d in decisions:
            t = d.get("title_ar") or d.get("title_en") or ""
            lines.append(f"- {t}")
            rec = d.get("recommendation_ar") or ""
            if rec:
                lines.append(f"  - التوصية: {rec}")
    else:
        lines.append("- لا قرارات معلقة")
    lines.append("")
    lines.append("## خطة الأسبوع القادم")
    plan = report.get("next_week_plan") or []
    if plan:
        for p in plan:
            lines.append(f"- {p}")
    else:
        lines.append("- لا خطة محسوبة (مدخلات غير متاحة)")
    lines.append("")
    lines.append("## ضوابط ثابتة")
    g = report.get("guardrails") or {}
    lines.append(f"- منع الإرسال الحي: {g.get('no_live_send')}")
    lines.append(f"- منع الكشط: {g.get('no_scraping')}")
    lines.append(f"- منع التواصل البارد: {g.get('no_cold_outreach')}")
    lines.append(
        f"- موافقة بشرية لكل إجراء خارجي: "
        f"{g.get('approval_required_for_external_actions')}"
    )
    return _scrub("\n".join(lines))


def _render_markdown_en(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Dealix — Weekly Executive Report")
    if report.get("week_label"):
        lines.append(f"_Week: {report['week_label']}_")
    lines.append(f"_generated_at: {report.get('generated_at')}_")
    lines.append("")
    lines.append("## Executive summary")
    lines.append(report.get("executive_summary_en", ""))
    lines.append("")
    lines.append("## Revenue movement")
    pipe = report.get("pipeline") or {}
    counts = pipe.get("counts") or {}
    if counts:
        lines.append(
            f"- live: {counts.get('live', 0)} | "
            f"pilot: {counts.get('pilot', 0)} | "
            f"partial: {counts.get('partial', 0)} | "
            f"total: {counts.get('total', 0)}"
        )
    else:
        lines.append("- no movement data available")
    lines.append("")
    lines.append("## Proof events (anonymized)")
    proof = report.get("proof") or {}
    lines.append(f"- total events: {proof.get('total', 0)}")
    by_type = proof.get("by_type") or {}
    for tp, ct in list(by_type.items())[:6]:
        lines.append(f"  - {tp}: {ct}")
    lines.append("")
    lines.append("## Risks")
    risks = report.get("risks") or []
    if risks:
        for r in risks[:8]:
            lines.append(f"- {r}")
    else:
        lines.append("- no risks observed")
    lines.append("")
    lines.append("## Founder decisions")
    decisions = report.get("decisions") or []
    if decisions:
        for d in decisions:
            t = d.get("title_en") or d.get("title_ar") or ""
            lines.append(f"- {t}")
            rec = d.get("recommendation_en") or ""
            if rec:
                lines.append(f"  - recommendation: {rec}")
    else:
        lines.append("- no pending decisions")
    lines.append("")
    lines.append("## Next-week plan")
    plan = report.get("next_week_plan") or []
    if plan:
        for p in plan:
            lines.append(f"- {p}")
    else:
        lines.append("- no plan computed (inputs unavailable)")
    lines.append("")
    lines.append("## Hard guardrails")
    g = report.get("guardrails") or {}
    lines.append(f"- no_live_send: {g.get('no_live_send')}")
    lines.append(f"- no_scraping: {g.get('no_scraping')}")
    lines.append(f"- no_cold_outreach: {g.get('no_cold_outreach')}")
    lines.append(
        f"- approval_required_for_external_actions: "
        f"{g.get('approval_required_for_external_actions')}"
    )
    return _scrub("\n".join(lines))


def _default_week_label() -> str:
    now = datetime.now(UTC)
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def build_weekly_report(
    week_label: str = "",
    ledger: Any | None = None,
) -> WeeklyReport:
    """Compose the full weekly report. Pure read-only.

    All upstream calls are individually wrapped so a single failure
    in one layer produces a degraded field but the report still
    builds. Returns a populated ``WeeklyReport``.
    """
    # Imports are deferred so a missing optional layer doesn't
    # break import of this module.
    from auto_client_acquisition.self_growth_os import (
        daily_growth_loop,
        service_activation_matrix,
        weekly_growth_scorecard,
    )
    from auto_client_acquisition.reliability_os import build_health_matrix

    label = week_label.strip() or _default_week_label()

    counts = _safe(service_activation_matrix.counts, default={}) or {}
    candidates = (
        _safe(service_activation_matrix.candidates_for_promotion, default=[]) or []
    )
    scorecard = _safe(weekly_growth_scorecard.build_scorecard, default={}) or {}
    loop = _safe(daily_growth_loop.build_today, default={}) or {}
    health = _safe(build_health_matrix, default={}) or {}
    proof = proof_summary(ledger=ledger, limit=200)

    # Pull recent ledger events for risk extraction.
    proof_events: list[Any] = []
    try:
        from auto_client_acquisition.proof_ledger import get_default_ledger
        led = ledger or get_default_ledger()
        proof_events = _safe(led.list_events, limit=200, default=[]) or []
    except Exception:  # noqa: BLE001
        proof_events = []

    risks = risk_summary(health, proof_events)
    decisions = decision_summary(loop, limit=5)

    revenue_movement = {
        "counts": counts,
        "next_promotion_candidates": (
            (scorecard.get("service_activation") or {}).get("next_promotion_candidates")
            or []
        ),
    }
    pipeline = {
        "counts": counts,
        "scorecard_recommendations": scorecard.get("recommendations") or [],
        "open_founder_decisions": scorecard.get("open_founder_decisions") or [],
    }
    delivery = {
        "perimeter_status": loop.get("perimeter_status") or {},
        "service_to_promote": loop.get("service_to_promote") or {},
        "geo_aio": scorecard.get("geo_aio") or {},
        "internal_linking": scorecard.get("internal_linking") or {},
    }

    plan = next_week_plan(
        scorecard=scorecard,
        loop=loop,
        health_matrix=health,
        promotion_candidates=candidates,
        limit=7,
    )

    summary_ar, summary_en = _build_executive_summary(
        counts=counts,
        proof=proof,
        risks=risks,
        decisions=decisions,
    )
    summary_ar = _scrub(summary_ar)
    summary_en = _scrub(summary_en)

    guardrails = {
        "no_live_send": True,
        "no_scraping": True,
        "no_cold_outreach": True,
        "approval_required_for_external_actions": True,
        "no_llm_call": True,
        "no_pii_in_report": True,
    }

    intermediate: dict[str, Any] = {
        "week_label": label,
        "generated_at": datetime.now(UTC).isoformat(),
        "executive_summary_ar": summary_ar,
        "executive_summary_en": summary_en,
        "revenue_movement": revenue_movement,
        "pipeline": pipeline,
        "delivery": delivery,
        "proof": proof,
        "risks": risks,
        "decisions": decisions,
        "next_week_plan": plan,
        "guardrails": guardrails,
    }

    md_ar = _render_markdown_ar(intermediate)
    md_en = _render_markdown_en(intermediate)

    return WeeklyReport(
        week_label=label,
        executive_summary_ar=summary_ar,
        executive_summary_en=summary_en,
        revenue_movement=revenue_movement,
        pipeline=pipeline,
        delivery=delivery,
        proof=proof,
        risks=risks,
        decisions=decisions,
        next_week_plan=plan,
        markdown_ar=md_ar,
        markdown_en=md_en,
        guardrails=guardrails,
    )
