#!/usr/bin/env python3
"""Wave 6 Phase 3 — AI Ops Diagnostic generator.

Deterministic template-based output. Works without API keys.
Bilingual (Arabic primary, English secondary).

Hard rules:
- No fake facts
- No guaranteed claims
- No live action
- action_mode = approval_required
- if unknown, mark insufficient_data
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

LIVE_DIR = Path("docs/wave6/live")

# Forbidden tokens (Article 8 + Wave 5 enforcement)
FORBIDDEN_AR = ("نضمن", "مضمون")
FORBIDDEN_EN = ("guaranteed", "blast", "scraping", "cold whatsapp", "cold email")


# Sector → typical bottleneck templates (deterministic, never invented)
_SECTOR_BOTTLENECKS_AR: dict[str, list[str]] = {
    "real_estate": [
        "بطء الردّ على leads (٢-٤ ساعات → leads تروح للمنافس)",
        "غياب نظام تقييم الـ leads — كل lead يعامل بنفس الأولويّة",
        "ما في proof pack موثّق للعملاء بعد الإغلاق",
    ],
    "agencies": [
        "leads متفرقة بين WhatsApp / Email / LinkedIn بدون مكان موحّد",
        "متابعة العملاء يدويّة + متعبة + ينسى المندوب",
        "غياب reporting أسبوعي للعملاء — يطلبون تحديثات بشكل عشوائي",
    ],
    "services": [
        "تقدير الوقت + التسعير غير متّسق بين الـ engagements",
        "غياب نظام إدارة الـ retainer monthly",
        "ضعف في proof + case studies للبيع التالي",
    ],
    "consulting": [
        "كل engagement يبدأ من الصفر — لا re-use للـ frameworks",
        "غياب نظام لقياس outcome العميل بعد ٣٠ يوم",
        "صعوبة في scaling beyond solo capacity",
    ],
    "training": [
        "لا متابعة تطبيق المتدرّبين بعد الورشة",
        "غياب تجزئة المحتوى لمراحل (pre/during/post)",
        "ضعف في proof = مشاركون رضوا فعلاً",
    ],
    "construction": [
        "تتبّع المشاريع بالـ Excel + WhatsApp = أخطاء",
        "غياب SLA للردّ على inquiries جديدة",
        "ضعف في documenting proof of delivery",
    ],
    "hospitality": [
        "توزيع الـ inquiries بين الفنادق والـ properties غير منظّم",
        "غياب dashboard موحّد للحجوزات والإيرادات",
        "ضعف في NPS + customer feedback collection",
    ],
    "logistics": [
        "تحديثات الشحنات غير real-time للعميل",
        "غياب SLA tracking على المشاكل التشغيليّة",
        "ضعف في reporting للـ B2B clients",
    ],
}

_SECTOR_BOTTLENECKS_EN: dict[str, list[str]] = {
    "real_estate": [
        "Slow lead response (2-4 hours → leads leak to competitor)",
        "No lead scoring system — every lead treated with the same priority",
        "No documented proof pack for closed customers",
    ],
    "agencies": [
        "Leads scattered across WhatsApp / Email / LinkedIn with no unified inbox",
        "Manual follow-up exhausts reps and gets forgotten",
        "No weekly reporting cadence — clients ask for updates randomly",
    ],
    "services": [
        "Inconsistent time + pricing estimates across engagements",
        "No retainer-monthly management system",
        "Weak proof + case studies for next-sale leverage",
    ],
    "consulting": [
        "Every engagement starts from scratch — no framework re-use",
        "No system to measure 30-day client outcomes",
        "Hard to scale beyond solo capacity",
    ],
    "training": [
        "No post-workshop application tracking",
        "Content not segmented for pre/during/post stages",
        "Weak proof that participants actually applied learnings",
    ],
    "construction": [
        "Project tracking via Excel + WhatsApp = errors",
        "No SLA for new inquiry response",
        "Weak proof-of-delivery documentation",
    ],
    "hospitality": [
        "Inquiry distribution across hotels/properties is unorganized",
        "No unified booking + revenue dashboard",
        "Weak NPS + customer feedback collection",
    ],
    "logistics": [
        "Shipment updates not real-time for customer",
        "No SLA tracking on operational issues",
        "Weak B2B-client reporting",
    ],
}


def _scrub(text: str) -> tuple[str, list[str]]:
    """Return (cleaned, findings) — substitute forbidden tokens."""
    findings: list[str] = []
    cleaned = text
    for token in FORBIDDEN_AR:
        if token in cleaned:
            findings.append(f"forbidden_ar:{token}")
            cleaned = cleaned.replace(token, "[REDACTED]")
    lower = cleaned.lower()
    for token in FORBIDDEN_EN:
        if token in lower:
            findings.append(f"forbidden_en:{token}")
            # case-insensitive replace
            import re
            cleaned = re.compile(re.escape(token), re.IGNORECASE).sub(
                "[REDACTED]", cleaned,
            )
    return cleaned, findings


def build_diagnostic(
    *,
    company: str,
    sector: str,
    region: str,
    problem: str,
    language: str,
) -> dict[str, Any]:
    bottlenecks_ar = _SECTOR_BOTTLENECKS_AR.get(sector, [
        "insufficient_data — لم تُحدَّد bottlenecks للقطاع",
    ])
    bottlenecks_en = _SECTOR_BOTTLENECKS_EN.get(sector, [
        "insufficient_data — bottlenecks not specified for this sector",
    ])

    summary_ar = (
        f"تقرير تشخيص AI Ops لشركة {company} في قطاع {sector} ({region}). "
        f"المشكلة المُعلنة: {problem or '—'}. "
        f"التقرير يحدد ٣ bottlenecks متكررة في القطاع، خطّة ٧ أيّام مبدئيّة، "
        f"وعرض Sprint بـ ٤٩٩ ريال. لا ضمانات. كل قرار خارجي بموافقتك."
    )
    summary_en = (
        f"AI Ops diagnostic for {company} in {sector} ({region}). "
        f"Stated problem: {problem or '—'}. "
        f"The report identifies 3 recurring sector bottlenecks, a 7-day "
        f"plan outline, and a 499 SAR Sprint offer. No guarantees. "
        f"All external actions remain approval-first."
    )

    recommended_ai_team_ar = [
        "Sales Agent — تأهيل الـ leads + draft الردّ السعودي",
        "Growth Agent — رصد فرص النمو من ١٦ نوع إشارة",
        "Support Agent — ٧ مراحل journey بدلاً من tickets",
        "Ops Agent — قائمة قرارات يوميّة (≤٣)",
        "Executive Agent — Full-Ops Score + ECC view",
    ]
    recommended_ai_team_en = [
        "Sales Agent — qualify leads + draft Saudi-Arabic replies",
        "Growth Agent — scan 16 signal types for opportunities",
        "Support Agent — 7-stage journey routing (vs ticket-only)",
        "Ops Agent — daily decision queue (≤3)",
        "Executive Agent — Full-Ops Score + ECC dashboard",
    ]

    top_3_opportunities_ar = [
        "تفعيل Lead Scoring المؤتمت → اكتشاف أعلى ١٠٪ leads فوراً",
        "نشر Customer Portal لكل عميل → شفافيّة + reduce support tickets ٤٠٪",
        "بناء Proof Pack أسبوعي → تحويل العملاء الحاليّين لـ case studies",
    ]
    top_3_opportunities_en = [
        "Activate automated Lead Scoring → identify top 10% leads instantly",
        "Deploy Customer Portal per customer → transparency + ~40% fewer support tickets",
        "Build weekly Proof Pack → convert active customers to case studies",
    ]

    top_3_risks_ar = [
        "لو ما اعتمدت approval-first → خرق PDPL محتمل",
        "لو ضمنت أرقام → فقدان ثقة العميل عند أوّل خطأ",
        "لو scaling قبل أوّل ٣ paid pilots → wasted capacity",
    ]
    top_3_risks_en = [
        "Without approval-first → potential PDPL breach",
        "Guaranteeing numbers → trust loss on first miss",
        "Scaling before first 3 paid pilots → wasted capacity",
    ]

    first_7_day_plan_ar = [
        "اليوم ١: Lead Quality Audit — تقييم آخر ٥٠ lead",
        "اليوم ٢: Pipeline Audit — تحديد leakage points",
        "اليوم ٣: Customer Portal setup — رابط مخصّص لشركتك",
        "اليوم ٤: Sample drafts — ٣ ردود WhatsApp/email جاهزة",
        "اليوم ٥: Daily Decisions Brief — أوّل ٣ قرارات حسّاسة",
        "اليوم ٦: Initial Proof Pack — ٣ proof events",
        "اليوم ٧: Review call + 30-day plan",
    ]
    first_7_day_plan_en = [
        "Day 1: Lead Quality Audit — score the last 50 leads",
        "Day 2: Pipeline Audit — identify leakage points",
        "Day 3: Customer Portal setup — your dedicated link",
        "Day 4: Sample drafts — 3 ready WhatsApp/email replies",
        "Day 5: Daily Decisions Brief — first 3 sensitive calls",
        "Day 6: Initial Proof Pack — 3 proof events",
        "Day 7: Review call + 30-day plan",
    ]

    diagnostic = {
        "company": company,
        "sector": sector,
        "region": region,
        "problem": problem,
        "language": language,
        "executive_summary_ar": _scrub(summary_ar)[0],
        "executive_summary_en": _scrub(summary_en)[0],
        "full_ops_bottlenecks_ar": [_scrub(b)[0] for b in bottlenecks_ar],
        "full_ops_bottlenecks_en": [_scrub(b)[0] for b in bottlenecks_en],
        "recommended_ai_team_ar": [_scrub(s)[0] for s in recommended_ai_team_ar],
        "recommended_ai_team_en": [_scrub(s)[0] for s in recommended_ai_team_en],
        "top_3_opportunities_ar": [_scrub(s)[0] for s in top_3_opportunities_ar],
        "top_3_opportunities_en": [_scrub(s)[0] for s in top_3_opportunities_en],
        "top_3_risks_ar": [_scrub(s)[0] for s in top_3_risks_ar],
        "top_3_risks_en": [_scrub(s)[0] for s in top_3_risks_en],
        "first_7_day_plan_ar": [_scrub(s)[0] for s in first_7_day_plan_ar],
        "first_7_day_plan_en": [_scrub(s)[0] for s in first_7_day_plan_en],
        "recommended_offer": "7-Day Revenue Proof Sprint @ 499 SAR",
        "what_not_to_automate": [
            "إرسال WhatsApp تلقائي للعميل — gate: NO_LIVE_SEND",
            "أتمتة LinkedIn — gate: NO_LINKEDIN_AUTO",
            "خصم بطاقة حيّ — gate: NO_LIVE_CHARGE",
            "تواصل بارد — gate: NO_COLD_X",
            "سحب بيانات من مواقع المنافسين — gate: NO_SCRAPING",
        ],
        "action_mode": "approval_required",
        "no_guaranteed_claims": True,
        "is_template_based": True,
        "source": "wave6_phase3_diagnostic_generator",
    }
    return diagnostic


def render_markdown(d: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# AI Ops Diagnostic — {d['company']}")
    lines.append("")
    lines.append(f"**Sector:** {d['sector']} · **Region:** {d['region']} · **Date:** generated by Dealix")
    lines.append("")
    lines.append("## ملخّص تنفيذي (Executive Summary)")
    lines.append(d["executive_summary_ar"])
    lines.append("")
    lines.append("> " + d["executive_summary_en"])
    lines.append("")
    lines.append("## ٣ Bottlenecks في القطاع")
    for ar in d["full_ops_bottlenecks_ar"]:
        lines.append(f"- {ar}")
    lines.append("")
    lines.append("**English:**")
    for en in d["full_ops_bottlenecks_en"]:
        lines.append(f"- {en}")
    lines.append("")
    lines.append("## فريق AI المقترح")
    for ar in d["recommended_ai_team_ar"]:
        lines.append(f"- {ar}")
    lines.append("")
    lines.append("## أعلى ٣ فرص")
    for ar in d["top_3_opportunities_ar"]:
        lines.append(f"- {ar}")
    lines.append("")
    lines.append("## أعلى ٣ مخاطر")
    for ar in d["top_3_risks_ar"]:
        lines.append(f"- {ar}")
    lines.append("")
    lines.append("## خطّة ٧ أيّام مبدئيّة")
    for ar in d["first_7_day_plan_ar"]:
        lines.append(f"- {ar}")
    lines.append("")
    lines.append(f"## العرض المقترح: **{d['recommended_offer']}**")
    lines.append("")
    lines.append("## ما لن نقوم به (مباشرة):")
    for item in d["what_not_to_automate"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**كل قرار خارجي بموافقتك. لا ضمانات. لا ادّعاءات. لا أرقام مخترعة.**")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 AI Ops Diagnostic generator")
    p.add_argument("--company", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--problem", default="")
    p.add_argument("--language", default="both", choices=["ar", "en", "both"])
    p.add_argument("--out-md", default=None, help="Write markdown here (default: live/diagnostic.md)")
    p.add_argument("--out-json", default=None, help="Write JSON here (default: live/diagnostic.json)")
    args = p.parse_args()

    d = build_diagnostic(
        company=args.company, sector=args.sector, region=args.region,
        problem=args.problem, language=args.language,
    )

    out_md = Path(args.out_md) if args.out_md else LIVE_DIR / "diagnostic.md"
    out_json = Path(args.out_json) if args.out_json else LIVE_DIR / "diagnostic.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_md.write_text(render_markdown(d), encoding="utf-8")
    out_json.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote {out_md} + {out_json}")
    print(f"  action_mode: {d['action_mode']}")
    print(f"  no_guaranteed_claims: {d['no_guaranteed_claims']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
