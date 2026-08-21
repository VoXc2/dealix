#!/usr/bin/env python3
"""Upsert current-authority Dealix social drafts for weeks 9-28.

This script mutates only the internal draft queue. It never publishes or sends.
Historical published rows are preserved; stale draft/approved rows in canonical
week/day slots are replaced and their approval is reset to ``draft``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dealix/config/social_content_queue.yaml"
DEFAULT_CYCLE_WEEKS = 28
LAUNCH_AUTHORITY = "revenue_command_pilot_30d"
CTA_AR = (
    "Free Mini Diagnostic → qualified discovery → customer-specific quote. "
    "لا Checkout تلقائي ولا إرسال خارجي تلقائي."
)

# Educational themes under one product. These are capability/operating themes,
# not separate offers or claims that every capability is production-ready for
# every customer today.
WEEK_THEMES: tuple[tuple[int, str, str], ...] = (
    (9, "رؤية الواقع", "Company Brain + Business Graph يجمعان السياق المطلوب لاتخاذ قرار أفضل دون استبدال كل أنظمة الشركة."),
    (10, "Daily Executive Command", "الهدف ليس Dashboard إضافيًا؛ بل معرفة أهم فرصة وقرار وبلوكِر وخطوة تالية."),
    (11, "Approval-first", "الذكاء الاصطناعي يجهز العمل، والإجراءات الحساسة تبقى خلف موافقة وحدود واضحة."),
    (12, "Proof-backed", "Activity ليست Customer Value؛ كل Claim يحتاج baseline ومصدرًا وطريقة قياس ودليلًا مناسبًا."),
    (13, "Revenue leakage", "نبحث عن فرص بلا owner أو next action أو evidence بدل إضافة حجم رسائل عشوائي."),
    (14, "Buying committee", "الصفقة B2B تحتاج فهم من يقرر ومن يراجع ومن يستطيع إيقافها، لا Contact واحدًا فقط."),
    (15, "Proposal + business case", "العرض الجيد يربط المشكلة والنطاق والقبول والدليل بدل وعود عامة."),
    (16, "Negotiation guardrails", "أي concession يجب أن يقابله give-get واضح، مع حماية النطاق والاقتصاديات."),
    (17, "Commercial finance", "قبل الالتزام نراجع القدرة والنطاق والهامش والمتطلبات بدل إغلاق صفقة غير قابلة للتسليم."),
    (18, "Minimum-data Pilot", "ابدأ بأقل بيانات وصلاحيات ممكنة، ووسّع فقط إذا احتاج النطاق وبعد إغلاق البوابات المناسبة."),
    (19, "Saudi bilingual context", "السياق العربي/الإنجليزي مهم في القرار التجاري، لكن اللغة لا تعني ادعاء امتثال أو نتيجة."),
    (20, "Partner intelligence", "الشراكات تُبنى على fit ودور وقيمة مشتركة ودليل، لا على قوائم اتصالات جماعية."),
    (21, "Customer-to-Value", "التسليم لا ينتهي عند النشاط؛ نربط onboarding والاستخدام والنتيجة والـProof."),
    (22, "Decision Passport", "القرار الجيد يحمل source وconfidence وowner وexpiry وapproval بدل أن يصبح رأيًا مجهول المصدر."),
    (23, "Proof Ledger", "Payment وRevenue وDelivery وCustomer Value وPublication Permission حالات منفصلة."),
    (24, "Learning loop", "التعلم الحقيقي يأتي من النتائج والرفض والبلوكِرات والأدلة، مع مراجعة بشرية قبل تغيير playbooks."),
    (25, "Model routing", "اختيار النموذج يعتمد على الحساسية والجودة والتكلفة والسياسة؛ ليس كل سياق مناسبًا لنفس المسار."),
    (26, "Production trust", "Health endpoint وحده لا يثبت جاهزية المنتج؛ نحتاج release identity وfrontend ownership وبوابات تشغيل قابلة للتحقق."),
    (27, "Tenant + privacy boundaries", "بيانات العميل لا تدخل لأن التكامل متاح تقنيًا؛ يلزم scope وغرض وصلاحيات وعزل وحدود احتفاظ مناسبة."),
    (28, "Stop / expand / redesign", "نهاية الـPilot ليست Upsell تلقائيًا؛ القرار يأتي من الدليل: نتوقف أو نتوسع أو نعيد التصميم."),
)

PILLARS = ("founder_media", "proof", "objection", "trust", "proof")


def _drafts_for_theme(week: int, theme: str, angle: str) -> list[dict[str, Any]]:
    rows = (
        (
            f"Dealix: {theme}",
            f"Dealix منتج واحد: Saudi-first AI Business Operating System. {angle}",
            f"week-{week}-dealix-{theme.lower().replace(' ', '-')}",
        ),
        (
            f"كيف نثبت {theme}؟",
            "نبدأ بـ baseline ومصدر ونفصل النشاط عن التسليم والقيمة والإيراد. Missing evidence يبقى Unknown، وليس نجاحًا.",
            f"week-{week}-proof-method",
        ),
        (
            "لماذا لا أتمتة بلا حدود؟",
            "Approval-first يعني أن Dealix يستطيع التحليل والتجهيز داخليًا، بينما الإرسال والنشر والدفع وتغييرات الإنتاج تبقى خلف بوابات مستقلة.",
            f"week-{week}-governed-automation",
        ),
        (
            f"حدود الثقة: {theme}",
            "لا guaranteed revenue أو ROI، لا cold WhatsApp، لا LinkedIn automation جماعي، ولا Customer Proof بلا دليل وإذن نشر مناسب.",
            f"week-{week}-trust-boundary",
        ),
        (
            "من التشخيص إلى Pilot",
            "Free Mini Diagnostic → qualified discovery → customer-specific quote → 30-day Revenue Command Pilot → weekly/final Proof → stop / expand / redesign.",
            f"week-{week}-pilot-path",
        ),
    )

    posts: list[dict[str, Any]] = []
    for day, (title_ar, body_ar, slug) in enumerate(rows):
        posts.append(
            {
                "week": week,
                "day": day,
                "pillar": PILLARS[day],
                "title_ar": title_ar,
                "body_ar": f"{body_ar}\n\n#Dealix #BusinessOS #SaudiArabia",
                "cta_ar": CTA_AR,
                "aeo_slug": slug,
                "status": "draft",
                "launch_authority": LAUNCH_AUTHORITY,
            }
        )
    return posts


def _canonical_posts(cycle_weeks: int) -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    for week, theme, angle in WEEK_THEMES:
        if week <= cycle_weeks:
            posts.extend(_drafts_for_theme(week, theme, angle))
    return posts


def _content_signature(post: dict[str, Any]) -> tuple[str, ...]:
    keys = ("pillar", "title_ar", "body_ar", "cta_ar", "aeo_slug", "launch_authority")
    return tuple(str(post.get(key) or "") for key in keys)


def _upsert_current_drafts(
    existing_posts: list[dict[str, Any]],
    canonical_posts: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, int, int]:
    """Return posts plus added/updated/preserved-published counters."""
    posts = [dict(row) for row in existing_posts if isinstance(row, dict)]
    added = 0
    updated = 0
    preserved_published = 0

    for canonical in canonical_posts:
        week = int(canonical["week"])
        day = int(canonical["day"])
        matches = [
            idx
            for idx, row in enumerate(posts)
            if int(row.get("week", 0)) == week and int(row.get("day", -1)) == day
        ]
        editable = next(
            (idx for idx in matches if (posts[idx].get("status") or "draft") != "published"),
            None,
        )

        if editable is None:
            if matches:
                # Keep historical published content as evidence; add a fresh
                # current-authority draft for future use.
                preserved_published += len(matches)
            posts.append(dict(canonical))
            added += 1
            continue

        old = posts[editable]
        if _content_signature(old) != _content_signature(canonical) or (
            old.get("status") or "draft"
        ) != "draft":
            posts[editable] = dict(canonical)
            updated += 1
        else:
            posts[editable]["launch_authority"] = LAUNCH_AUTHORITY

    return posts, added, updated, preserved_published


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cycle-weeks",
        type=int,
        default=DEFAULT_CYCLE_WEEKS,
        help=f"Set cycle_weeks in YAML (default {DEFAULT_CYCLE_WEEKS})",
    )
    args = parser.parse_args()
    if args.cycle_weeks < 9 or args.cycle_weeks > DEFAULT_CYCLE_WEEKS:
        parser.error(f"--cycle-weeks must be between 9 and {DEFAULT_CYCLE_WEEKS}")

    data = yaml.safe_load(QUEUE.read_text(encoding="utf-8")) or {}
    existing_posts = list(data.get("posts") or [])
    canonical_posts = _canonical_posts(args.cycle_weeks)
    posts, added, updated, preserved_published = _upsert_current_drafts(
        existing_posts,
        canonical_posts,
    )

    data["posts"] = posts
    data["cycle_weeks"] = args.cycle_weeks
    data["launch_authority"] = LAUNCH_AUTHORITY
    data["external_publish_allowed"] = False
    QUEUE.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(
        "EXPAND_SOCIAL_QUEUE: "
        f"added={added} updated={updated} "
        f"preserved_published={preserved_published} total={len(posts)} "
        f"cycle_weeks={args.cycle_weeks} authority={LAUNCH_AUTHORITY}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
