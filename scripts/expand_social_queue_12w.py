#!/usr/bin/env python3
"""Upsert current Dealix corporate social drafts for weeks 1-28.

This script mutates only the internal draft queue. It never publishes or sends.
Historical published rows are preserved; stale draft/approved rows in canonical
week/day slots are replaced and approval resets to ``draft``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dealix/config/social_content_queue.yaml"
DEFAULT_CYCLE_WEEKS = 28
MIN_CYCLE_WEEKS = 8
LAUNCH_AUTHORITY = "corporate_brand_gtm_v1"
CTA_AR = (
    "Execution Diagnostic → qualified discovery → customer-specific quote. "
    "لا Checkout تلقائي ولا نشر أو إرسال خارجي تلقائي."
)

# Parent-company themes. Dealix OS remains the flagship product, not the entire
# definition of Dealix. Themes are educational/strategic; they do not claim
# production readiness, customer results, consent, certification, or revenue.
WEEK_THEMES: tuple[tuple[int, str, str, str], ...] = (
    (1, "Execution Gap", "الفجوة بين القرار والتنفيذ أهم من عدد أدوات AI.", "executive_signal"),
    (2, "Dealix Company", "Strategy + Systems + Intelligence + Products تحت شركة واحدة؛ Dealix OS منتج رئيسي داخلها.", "strategic_pov"),
    (3, "Governed AI", "Owner + authority + evidence + rollback قبل توسيع أي Agent.", "governed_ai"),
    (4, "Revenue Systems", "تسرب المتابعة والقرار يحتاج operating system لا مزيدًا من volume.", "revenue_systems"),
    (5, "Saudi Opportunity", "الإشارة الرسمية تتحول إلى فرضية تجارية قابلة للاختبار، لا buyer intent.", "saudi_opportunity"),
    (6, "Proof Before Claim", "Capability evidence وdelivery وoutcome وCustomer Proof حالات مختلفة.", "build_proof"),
    (7, "Saudi Market Access", "Market entry يبدأ evidence + route + partner fit + bounded validation.", "saudi_opportunity"),
    (8, "Service to Product", "نحوّل المشكلة المتكررة المثبتة إلى product فقط عندما يبرر الدليل ذلك.", "strategic_pov"),
    (9, "Strategy to Operating Model", "الاستراتيجية التي بلا owner وcadence وacceptance لا تتحول إلى تنفيذ.", "strategic_pov"),
    (10, "Executive Command", "أفضل command room يقلل القرارات الضائعة بدل إضافة dashboard جديدة.", "executive_signal"),
    (11, "Company Brain", "المعرفة تصبح مفيدة عندما ترتبط بقرار وsource وexpiry وnext action.", "systems_automation"),
    (12, "Opportunity Graph", "الفرصة ليست lead؛ تحتاج evidence وstage وowner وprobability وnext action.", "revenue_systems"),
    (13, "Follow-up Recovery", "قبل زيادة leads، افحص أين تسقط المتابعة الحالية ومن يملكها.", "revenue_systems"),
    (14, "Buying Committee", "B2B enterprise قرار جماعي؛ contact واحد لا يساوي buying authority.", "revenue_systems"),
    (15, "Proposal Architecture", "العرض الأقوى يربط problem → scope → acceptance → economics → proof.", "revenue_systems"),
    (16, "Negotiation Guardrails", "أي concession يحتاج give-get واضحًا ويحمي النطاق والهامش.", "revenue_systems"),
    (17, "AI Governance Readiness", "الحوكمة طبقة تشغيل يومية وليست policy PDF فقط.", "governed_ai"),
    (18, "Agent Reliability", "Agent جيد يعني evals وtool authority وfallback وreceipts، لا prompt جميل فقط.", "governed_ai"),
    (19, "Privacy by Workflow", "الغرض والصلاحية والاحتفاظ والعزل يجب أن تعيش داخل workflow.", "governed_ai"),
    (20, "Partner Route", "الشراكة تحتاج buyer fit ودورًا اقتصاديًا وإثباتًا، لا قائمة logos.", "saudi_opportunity"),
    (21, "Tender Intelligence", "Tender signal دليل طلب فقط؛ لا يعني qualification أو invitation أو award.", "saudi_opportunity"),
    (22, "Customer Value", "التسليم لا ينتهي عند النشاط؛ يجب ربطه بالـbaseline والنتيجة والقبول.", "build_proof"),
    (23, "Proof Ledger", "Payment وDelivery وOutcome وPublication Permission سجلات مستقلة.", "build_proof"),
    (24, "Content as Distribution", "المحتوى الجيد يخلق perspective ومحادثة مؤهلة، لا مجرد impressions.", "strategic_pov"),
    (25, "AI Model Economics", "اختيار النموذج قرار جودة/حساسية/تكلفة/سياسة وليس سباق benchmark فقط.", "systems_automation"),
    (26, "Production Trust", "Build success أو HTTP 200 وحدهما لا يثبتان release صحيحًا.", "build_proof"),
    (27, "Private SaaS Readiness", "Multi-tenant productization يأتي بعد proof متكرر وحدود tenant واضحة.", "systems_automation"),
    (28, "Stop / Expand / Redesign", "نهاية أي Sprint ليست upsell تلقائيًا؛ الدليل يقرر الخطوة التالية.", "build_proof"),
)

DAY_FORMATS: tuple[tuple[str, str], ...] = (
    ("founder_linkedin", "founder_pov"),
    ("company_linkedin", "company_architecture"),
    ("linkedin", "operator_playbook"),
    ("linkedin", "truth_firewall"),
    ("linkedin", "conversion_cta"),
)


def _drafts_for_theme(week: int, theme: str, angle: str, pillar: str) -> list[dict[str, Any]]:
    rows = (
        (
            f"{theme}: الفكرة التي يجب أن تتغير قبل أي أتمتة",
            f"{angle}\n\nفي Dealix نبدأ من المشكلة الاقتصادية أو التشغيلية، ثم نحدد signal وowner وnext action وproof قبل اختيار التقنية.",
        ),
        (
            f"{theme} داخل نموذج Dealix",
            f"{angle}\n\nDealix تعمل عبر Strategy & Transformation، Systems & Automation، Intelligence & Market Access، وTrust/Governance/Proof. Dealix OS يدخل فقط عندما تكون طبقة تشغيل مستمرة هي الحل المناسب.",
        ),
        (
            f"5 أسئلة لتشخيص {theme}",
            f"{angle}\n\n1) ما الـsignal الحقيقي؟ 2) من يملك القرار؟ 3) ما الـnext action؟ 4) ما الـauthority؟ 5) ما الـproof الذي يثبت الحركة؟",
        ),
        (
            f"Truth Firewall: {theme}",
            "Research ≠ Relationship · Public contact ≠ Consent · Draft ≠ Sent · Quote ≠ Payment · Demo ≠ Customer Proof.\n\nالسرعة الحقيقية تأتي من معرفة الدليل المطلوب للانتقال بين الحالات.",
        ),
        (
            f"من {theme} إلى Execution Diagnostic",
            f"{angle}\n\nلا تبدأ بشراء منصة جديدة. ابدأ بـworkflow واحد: baseline، owner، signal، action، authority، proof. إذا لم نجد حالة قابلة للقياس نتوقف؛ وإذا وجدناها ننتقل إلى Qualified Discovery ثم customer-specific scope.",
        ),
    )

    posts: list[dict[str, Any]] = []
    for day, ((surface, content_format), (title_ar, body_ar)) in enumerate(zip(DAY_FORMATS, rows, strict=True)):
        posts.append(
            {
                "week": week,
                "day": day,
                "surface": surface,
                "pillar": pillar,
                "format": content_format,
                "title_ar": title_ar,
                "body_ar": body_ar,
                "cta_ar": CTA_AR,
                "aeo_slug": f"w{week}-{theme.lower().replace(' ', '-').replace('/', '-').replace('&', 'and')}-{day + 1}",
                "status": "draft",
                "launch_authority": LAUNCH_AUTHORITY,
                "external_publish_allowed": False,
            }
        )
    return posts


def _canonical_posts(cycle_weeks: int) -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    for week, theme, angle, pillar in WEEK_THEMES:
        if week <= cycle_weeks:
            posts.extend(_drafts_for_theme(week, theme, angle, pillar))
    return posts


def _content_signature(post: dict[str, Any]) -> tuple[str, ...]:
    keys = (
        "surface",
        "pillar",
        "format",
        "title_ar",
        "body_ar",
        "cta_ar",
        "aeo_slug",
        "launch_authority",
        "external_publish_allowed",
    )
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
            posts[editable]["external_publish_allowed"] = False

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
    if args.cycle_weeks < MIN_CYCLE_WEEKS or args.cycle_weeks > DEFAULT_CYCLE_WEEKS:
        parser.error(
            f"--cycle-weeks must be between {MIN_CYCLE_WEEKS} and {DEFAULT_CYCLE_WEEKS}"
        )

    data = yaml.safe_load(QUEUE.read_text(encoding="utf-8")) or {}
    existing_posts = list(data.get("posts") or [])
    canonical_posts = _canonical_posts(args.cycle_weeks)
    posts, added, updated, preserved_published = _upsert_current_drafts(
        existing_posts,
        canonical_posts,
    )

    data["posts"] = posts
    data["anchor_date"] = "2026-09-13"
    data["cycle_weeks"] = args.cycle_weeks
    data["launch_authority"] = LAUNCH_AUTHORITY
    data["content_model"] = "verified_signal_to_channel_native_draft"
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
