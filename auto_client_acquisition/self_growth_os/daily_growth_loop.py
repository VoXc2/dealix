"""Daily growth loop — what should I do today?

Composes the existing measurement modules into a single, founder-
facing daily brief. Pure read-only composition: never sends, never
calls LLMs (the personal-operator brief may; this module simply
forwards its dict).

Output structure:

  - decisions: top 3 strategic decisions from the personal-operator
  - seo_gaps: top 3 lowest-scoring landing pages from geo_aio_radar
  - partner_focus: 1 partner category to draft an intro for
  - service_to_promote: 1 partial/pilot service nearest to Live
  - perimeter_status: forbidden-claims + linking + SEO summary
  - decline_or_open_loops: anything blocked or needing approval

The intent: a founder running ``GET /api/v1/self-growth/daily-loop``
each morning can see one screen with everything that matters today,
without reading 6 different APIs.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.self_growth_os import (
    geo_aio_radar,
    internal_linking_planner,
    partner_distribution_radar,
    seo_technical_auditor,
    service_activation_matrix,
)


def _safe_call(fn, *args, default=None, **kwargs):
    """Defensive wrapper — keep the loop usable even if one input
    module errors (e.g. SEO report not yet generated)."""
    try:
        return fn(*args, **kwargs)
    except Exception:  # noqa: BLE001 — defensive at the orchestration layer
        return default


def _decisions_from_personal_operator() -> list[dict[str, Any]]:
    """Pull the top 3 decisions from the personal-operator daily-brief.

    If the personal-operator module isn't reachable in this process,
    return a structured fallback that still tells the founder what
    to read manually.
    """
    try:
        from auto_client_acquisition.personal_operator import (
            build_daily_brief,
            default_sami_profile,
        )
        brief = build_daily_brief(default_sami_profile())
        payload = brief.to_dict() if hasattr(brief, "to_dict") else dict(brief)
    except Exception:  # noqa: BLE001
        return [{
            "title_ar": "افتح /api/v1/personal-operator/daily-brief يدوياً",
            "title_en": "Open /api/v1/personal-operator/daily-brief manually",
            "rationale": "personal-operator module is not reachable in this process",
        }]

    decisions: list[dict[str, Any]] = []
    raw_decisions = payload.get("decisions") or payload.get("top_decisions") or []
    for d in raw_decisions[:3]:
        if isinstance(d, dict):
            decisions.append(d)
        elif isinstance(d, str):
            decisions.append({"title_ar": d, "title_en": d})
    if not decisions and payload.get("opportunities"):
        for opp in (payload.get("opportunities") or [])[:3]:
            if isinstance(opp, dict):
                decisions.append(opp)
    return decisions[:3]


def _next_partner_focus() -> dict[str, Any]:
    """Pick one partner category — rotate by day-of-year to avoid
    always recommending the same one."""
    summary = partner_distribution_radar.summary()
    cats = summary.get("categories") or []
    if not cats:
        return {}
    # Deterministic rotation — same day = same recommendation.
    idx = datetime.now(UTC).timetuple().tm_yday % len(cats)
    return partner_distribution_radar.get_category(cats[idx]["category_id"])


def _perimeter_status() -> dict[str, Any]:
    seo_clean = _safe_call(seo_technical_auditor.is_perimeter_clean, default=None)
    linking_clean = _safe_call(internal_linking_planner.is_clean, default=None)
    geo_summary = _safe_call(geo_aio_radar.audit_all, default={})
    return {
        "seo_required_perimeter_clean": seo_clean,
        "internal_linking_clean": linking_clean,
        "geo_aio_avg_score": (geo_summary.get("summary") or {}).get("average_score") if geo_summary else None,
    }


def _service_to_promote() -> dict[str, Any]:
    """Top candidate from service_activation_matrix. Most actionable
    is the one with the fewest blocking_reasons."""
    try:
        candidates = service_activation_matrix.candidates_for_promotion()
    except FileNotFoundError:
        return {}
    if not candidates:
        return {}
    candidates.sort(key=lambda c: len(c.blocking_reasons))
    top = candidates[0]
    return {
        "service_id": top.service_id,
        "name_ar": top.name_ar,
        "name_en": top.name_en,
        "status": top.status,
        "blocking_reasons": top.blocking_reasons[:3],
        "next_action_ar": top.next_activation_step_ar,
        "next_action_en": top.next_activation_step_en,
    }


def _seo_gap_pages(limit: int = 3) -> list[dict[str, Any]]:
    """Pages that would benefit most from a content/structure improvement."""
    try:
        pages = geo_aio_radar.top_priority_pages(limit=limit)
    except Exception:  # noqa: BLE001
        return []
    return [
        {"path": p["path"], "score": p["score"], "gaps": p["gaps"][:5]}
        for p in pages
    ]


def _open_loops() -> list[str]:
    """Items that need founder attention but aren't a daily action."""
    out = [
        "B1: roi.html refund wording (REVIEW_PENDING)",
        "B2: academy.html 'Cold Email Pro' course title (REVIEW_PENDING)",
        "B4: pick a search/keyword data source",
        "S5: pick first service to flip Live (recommendation: lead_intake_whatsapp)",
    ]
    # Add link issues as open loops if any.
    try:
        linking = internal_linking_planner.build_graph()
        broken = linking["issues"].get("broken_relative_links") or []
        if broken:
            out.append(f"{len(broken)} broken landing-page link(s) — see /internal-linking")
        orphans = linking["issues"].get("orphan_core_pages") or []
        if orphans:
            out.append(f"orphan core page(s): {', '.join(orphans)}")
    except Exception:  # noqa: BLE001
        pass
    return out


def build_today() -> dict[str, Any]:
    """Compose the full daily loop. This is the main entry point."""
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "decisions": _decisions_from_personal_operator(),
        "service_to_promote": _service_to_promote(),
        "partner_focus": _next_partner_focus(),
        "seo_gap_pages": _seo_gap_pages(limit=3),
        "perimeter_status": _perimeter_status(),
        "open_loops": _open_loops(),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


def to_markdown(loop: dict[str, Any]) -> str:
    """Render the loop as markdown for a CLI / email digest."""
    lines: list[str] = []
    lines.append("# Dealix — Daily Growth Loop")
    lines.append(f"_generated_at: {loop.get('generated_at')}_\n")

    lines.append("## Top 3 decisions (founder)")
    for d in loop.get("decisions") or []:
        title = d.get("title_ar") or d.get("name_ar") or d.get("title") or str(d)
        lines.append(f"- {title}")
    if not loop.get("decisions"):
        lines.append("- (none from personal-operator)")
    lines.append("")

    svc = loop.get("service_to_promote") or {}
    if svc:
        lines.append("## Service nearest to Live")
        lines.append(f"- **{svc.get('service_id')}** ({svc.get('status')}): {svc.get('name_ar', '')} · {svc.get('name_en', '')}")
        if svc.get("next_action_ar"):
            lines.append(f"  - next: {svc['next_action_ar'].strip()}")
        lines.append("")

    pf = loop.get("partner_focus") or {}
    if pf:
        lines.append("## Partner focus (today)")
        lines.append(f"- **{pf.get('category_id')}**: {pf.get('name_ar', '')}")
        lines.append(f"  - draft (AR): {pf.get('warm_intro_draft_ar', '')[:120]}…")
        lines.append("")

    lines.append("## SEO gap pages (lowest GEO score)")
    for p in loop.get("seo_gap_pages") or []:
        lines.append(f"- {p['path']} (score {p['score']}): {', '.join(p.get('gaps', [])[:3])}")
    lines.append("")

    lines.append("## Open loops (founder attention)")
    for o in loop.get("open_loops") or []:
        lines.append(f"- {o}")
    lines.append("")

    lines.append("## Hard guardrails (always)")
    g = loop.get("guardrails") or {}
    lines.append(f"- no_live_send: {g.get('no_live_send')}")
    lines.append(f"- no_scraping: {g.get('no_scraping')}")
    lines.append(f"- no_cold_outreach: {g.get('no_cold_outreach')}")
    lines.append(f"- approval_required_for_external_actions: {g.get('approval_required_for_external_actions')}")
    return "\n".join(lines)
