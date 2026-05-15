"""Pricing page generator.

Renders the 7-tier ladder from ``service_mapping_v7.value_ladder``
when available; otherwise falls back to a hardcoded copy of the same
ladder. Includes a "proof-before-scale" rule banner + a no-guaranteed
-claims footer.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)

_FALLBACK_LADDER: list[dict[str, Any]] = [
    {
        "rung": 1,
        "service": "diagnostic",
        "name_ar": "Diagnostic مجاني",
        "name_en": "Free Growth Diagnostic",
        "price_band_sar": "0",
        "summary_ar": "جلسة 30-60 دقيقة + 3 توصيات + توصية بأفضل عرض أوّل.",
        "summary_en": "30-60 min session + 3 recommendations + best-first-offer pick.",
    },
    {
        "rung": 2,
        "service": "growth_starter_pilot",
        "name_ar": "499 ريال — Pilot نمو 7 أيام",
        "name_en": "499 SAR 7-Day Growth Proof Sprint (Growth Starter Pilot)",
        "price_band_sar": "499",
        "summary_ar": "7 أيام: 10 فرص + مسوّدات عربيّة + خطة متابعة + Proof Pack.",
        "summary_en": "7 days: 10 opportunities + Arabic drafts + follow-up plan + Proof Pack.",
    },
    {
        "rung": 3,
        "service": "growth_starter",
        "name_ar": "Growth Starter",
        "name_en": "Growth Starter",
        "price_band_sar": "1500-3000",
        "summary_ar": "شهر مكثف من حلقة النمو الأسبوعيّة + Proof Pack موسّع.",
        "summary_en": "One intensive month of weekly growth loop + extended Proof Pack.",
    },
    {
        "rung": 4,
        "service": "data_to_revenue",
        "name_ar": "Data to Revenue",
        "name_en": "Data to Revenue",
        "price_band_sar": "1500-3000",
        "summary_ar": "تنظيف قائمة + درجة contactability + رسائل مقسّمة + تقرير مخاطر.",
        "summary_en": "List cleanup + contactability score + segmented drafts + risk report.",
    },
    {
        "rung": 5,
        "service": "executive_growth_os",
        "name_ar": "Executive Growth OS",
        "name_en": "Executive Growth OS",
        "price_band_sar": "2999/month",
        "summary_ar": "حزمة أسبوعيّة: قرارات معلّقة + عوائق + مخاطر + actual vs forecast.",
        "summary_en": "Weekly pack: pending decisions + blockers + risks + actual-vs-forecast.",
    },
    {
        "rung": 6,
        "service": "partnership_growth",
        "name_ar": "Partnership Growth",
        "name_en": "Partnership Growth",
        "price_band_sar": "3000-7500",
        "summary_ar": "8 فئات شراكة + fit-score + مسوّدات تواصل دافئة + Proof Pack مشترك.",
        "summary_en": "8 partner categories + fit-score + warm-intro drafts + co-branded Proof Pack.",
    },
    {
        "rung": 7,
        "service": "full_growth_control_tower",
        "name_ar": "Full Growth Control Tower / Custom Enterprise",
        "name_en": "Full Growth Control Tower / Custom Enterprise",
        "price_band_sar": "custom",
        "summary_ar": "تخصيص كامل لمؤسسات متعدّدة الأقسام + لوحة قرارات + إيقاع شهريّ.",
        "summary_en": "Full customisation for multi-division orgs + decision board + monthly cadence.",
    },
]


def _load_ladder() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.service_mapping_v7 import value_ladder

        rungs = value_ladder() or []
        if rungs and len(rungs) >= 6:
            return list(rungs)
    except Exception:
        pass
    return list(_FALLBACK_LADDER)


def generate_pricing_page(highlight: str | None = None) -> dict[str, Any]:
    """Compose a bilingual pricing page artifact."""
    ladder = _load_ladder()

    title_ar = "أسعار Dealix — السلّم القيميّ ٧ درجات"
    title_en = "Dealix Pricing — 7-Tier Value Ladder"

    items_ar: list[str] = []
    items_en: list[str] = []
    for rung in ladder:
        marker_ar = "★ " if highlight and rung.get("service") == highlight else "• "
        marker_en = "★ " if highlight and rung.get("service") == highlight else "- "
        items_ar.append(
            f"{marker_ar}الدرجة {rung.get('rung', '?')} — "
            f"{rung.get('name_ar', '')} ({rung.get('price_band_sar', '—')} ريال): "
            f"{rung.get('summary_ar', '')}"
        )
        items_en.append(
            f"{marker_en}Tier {rung.get('rung', '?')} — "
            f"{rung.get('name_en', '')} ({rung.get('price_band_sar', '-')} SAR): "
            f"{rung.get('summary_en', '')}"
        )

    # Spec-required tier labels — render explicit named-section block.
    named_tiers_ar = [
        "Free Diagnostic",
        "499 SAR 7-Day Growth Proof Sprint (=Growth Starter Pilot)",
        "Growth Starter",
        "Data to Revenue",
        "Executive Growth OS",
        "Partnership Growth",
        "Full Growth Control Tower / Custom Enterprise",
    ]

    sections_ar = [
        {
            "title": "قاعدة الإثبات قبل التوسّع",
            "items": [
                "كل درجة أعلى تتطلّب Proof Pack موقَّع من الدرجة الأدنى.",
                "لا قفزات تسعير بدون أدلّة — التوسّع يتبع الإثبات.",
            ],
        },
        {"title": "السلّم القيميّ", "items": items_ar},
        {
            "title": "الأسماء الرسميّة للدرجات",
            "items": named_tiers_ar,
        },
        {
            "title": "ضمانات",
            "items": [
                "❌ لا ضمانات بأرقام أو ترتيب أو إيرادات.",
                "❌ لا ادعاءات تسويقيّة من نوع (المفردات الممنوعة).",
                "✅ التزام بالعمل + Proof Pack.",
            ],
        },
    ]
    sections_en = [
        {
            "title": "Proof-before-scale rule",
            "items": [
                "Every higher tier requires a signed Proof Pack from the tier below.",
                "No price jumps without evidence — scale follows proof.",
            ],
        },
        {"title": "Value ladder", "items": items_en},
        {
            "title": "Official tier names",
            "items": named_tiers_ar,  # tier names are bilingual / proper nouns
        },
        {
            "title": "Guarantees",
            "items": [
                "No guarantees on numbers, ranking, or revenue.",
                "No marketing claims.",
                "Commitment is on the work + a documented Proof Pack.",
            ],
        },
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        f"value_ladder.rungs={len(ladder)}",
        f"highlight={highlight or 'none'}",
    ]

    md_full = render_artifact_markdown(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )
    # Footer: explicit no-guaranteed-claims line in the document body.
    md_full += (
        "\n---\n"
        "> No-guarantee policy — commitment is on the work, not the numbers.\n"
        "> لا ادعاءات مضمونة — الالتزام بالعمل، لا بالأرقام.\n"
    )

    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    markdown_ar = (
        f"# {title_ar}\n\n"
        + "\n".join(items_ar)
        + "\n\n> الإثبات قبل التوسّع — لا ادعاءات مضمونة.\n"
    )
    markdown_en = (
        f"# {title_en}\n\n"
        + "\n".join(items_en)
        + "\n\n> Proof before scale — no-guarantee policy.\n"
    )

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "ladder": ladder,
        "manifest": {
            "artifact_type": "pricing_page",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "highlight": highlight,
            "tier_count": len(ladder),
        },
    }
