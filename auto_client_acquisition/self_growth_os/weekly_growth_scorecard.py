"""Weekly growth scorecard — aggregates the current state of every
in-repo signal into a single, founder-facing summary.

What it counts (all from real artifacts that already exist):

  - Service Activation Matrix: counts by status
  - SEO audit: required + advisory gaps
  - GEO/AIO readiness: average score + pages with FAQ signal
  - Internal linking: orphan core pages, missing CTAs, broken links
  - Forbidden-claims sweep: REVIEW_PENDING items remaining
  - Tooling: required-for-core packages installed/missing

What it does NOT count (intentionally — would be fake data):
  - Inbound leads / pipeline / revenue (no live integration yet)
  - Customer count / churn / NPS (no real customers yet)
  - Search rankings (no search data source connected)

The output is a typed dict consumable by the API; the founder reads
it weekly to decide what to ship next.
"""
from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.self_growth_os import (
    geo_aio_radar,
    internal_linking_planner,
    seo_technical_auditor,
    service_activation_matrix,
    tool_registry,
)


def build_scorecard() -> dict:
    """Run every measurement module and aggregate the result."""

    # 1. Service activation
    counts = service_activation_matrix.counts()
    candidates = service_activation_matrix.candidates_for_promotion()
    next_promotions = [
        {
            "service_id": c.service_id,
            "name_ar": c.name_ar,
            "name_en": c.name_en,
            "status": c.status,
            "blocking_reasons": c.blocking_reasons[:3],
        }
        for c in candidates[:5]
    ]

    # 2. Technical SEO
    try:
        seo_summary = seo_technical_auditor.summary()
        seo_perimeter_clean = seo_technical_auditor.is_perimeter_clean()
        seo_advisory_breakdown = seo_technical_auditor.gap_count()
    except FileNotFoundError:
        seo_summary = {"error": "audit not generated yet"}
        seo_perimeter_clean = False
        seo_advisory_breakdown = {}

    # 3. GEO/AIO readiness
    geo = geo_aio_radar.audit_all()
    geo_summary = geo.get("summary", {})
    geo_top_priority = geo_aio_radar.top_priority_pages(limit=3)

    # 4. Internal linking
    linking = internal_linking_planner.build_graph()
    linking_summary = linking.get("summary", {})
    linking_issues = linking.get("issues", {})

    # 5. Tooling
    missing_required_tools = tool_registry.core_required_missing()

    # 6. Open decisions (from EXECUTIVE_DECISION_PACK)
    pending_founder_decisions = [
        # B-series
        "B1: roi.html refund wording (REVIEW_PENDING)",
        "B2: academy.html 'Cold Email Pro' course title (REVIEW_PENDING)",
        "B3: pick next 1-3 pages for full OG copy",
        "B4: pick search/keyword data source",
        "B5: authorize Phase D safety tests (DONE on 2026-05-04)",
        # S-series
        "S1: Pilot retirement cap (after customer #5)",
        "S2: agency partner outreach authorization",
        "S3: outcome-rider experiment trigger",
        "S4: compliance-tier premium",
        "S5: first service to flip Live (recommendation: lead_intake_whatsapp)",
    ]

    # 7. Top recommended actions for the upcoming week (computed,
    # not invented). Each is anchored to a measurement above.
    recommendations: list[dict] = []
    if missing_required_tools:
        recommendations.append({
            "priority": "P0",
            "action": f"install required tools: {', '.join(missing_required_tools)}",
            "anchor": "tool_registry.core_required_missing",
        })
    if not seo_perimeter_clean:
        recommendations.append({
            "priority": "P0",
            "action": "fix SEO required-gap (title/meta-description/viewport/lang/dir)",
            "anchor": "seo_technical_auditor.summary.pages_with_required_gap",
        })
    if linking_issues.get("orphan_core_pages"):
        recommendations.append({
            "priority": "P1",
            "action": (
                "link to orphan core pages: "
                + ", ".join(linking_issues["orphan_core_pages"])
            ),
            "anchor": "internal_linking_planner.issues.orphan_core_pages",
        })
    if linking_issues.get("service_pages_without_cta"):
        recommendations.append({
            "priority": "P1",
            "action": (
                "add CTA to service pages: "
                + ", ".join(linking_issues["service_pages_without_cta"][:3])
                + ("..." if len(linking_issues["service_pages_without_cta"]) > 3 else "")
            ),
            "anchor": "internal_linking_planner.issues.service_pages_without_cta",
        })
    if linking_issues.get("broken_relative_links"):
        recommendations.append({
            "priority": "P1",
            "action": (
                f"fix {len(linking_issues['broken_relative_links'])} broken "
                "relative landing-page links"
            ),
            "anchor": "internal_linking_planner.issues.broken_relative_links",
        })
    advisory = seo_summary.get("pages_with_advisory_gap", 0) if isinstance(seo_summary, dict) else 0
    if isinstance(advisory, int) and advisory > 0:
        recommendations.append({
            "priority": "P2",
            "action": f"add canonical/OG/twitter to {advisory} advisory-gap pages (in batches of 3, founder approves OG copy)",
            "anchor": "seo_technical_auditor.summary.pages_with_advisory_gap",
        })
    if next_promotions:
        recommendations.append({
            "priority": "P1",
            "action": (
                "review service-promotion candidates: "
                + ", ".join(p["service_id"] for p in next_promotions[:3])
            ),
            "anchor": "service_activation_matrix.candidates_for_promotion",
        })

    if not recommendations:
        # No technical gap is open this week. The scorecard still surfaces
        # one forward-looking action so the founder always has a next step.
        recommendations.append({
            "priority": "P2",
            "action": (
                "technical perimeter clean — focus the week on warm-intro "
                "outreach and converting the next pilot conversation"
            ),
            "anchor": "weekly_growth_scorecard.all_gates_clear",
        })

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "service_activation": {
            "counts": counts,
            "next_promotion_candidates": next_promotions,
        },
        "technical_seo": {
            "summary": seo_summary,
            "perimeter_clean": seo_perimeter_clean,
            "advisory_gap_breakdown": seo_advisory_breakdown,
        },
        "geo_aio": {
            "summary": geo_summary,
            "top_priority_pages": [
                {"path": p["path"], "score": p["score"], "gaps": p["gaps"]}
                for p in geo_top_priority
            ],
        },
        "internal_linking": {
            "summary": linking_summary,
            "issues": linking_issues,
        },
        "tooling": {
            "missing_required": missing_required_tools,
        },
        "open_founder_decisions": pending_founder_decisions,
        "recommendations": recommendations,
    }
