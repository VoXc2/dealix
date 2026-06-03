#!/usr/bin/env python3
"""Append missing weeks to social_content_queue.yaml from AEO calendar slugs (up to 28 weeks)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dealix/config/social_content_queue.yaml"
DEFAULT_CYCLE_WEEKS = 28

WEEKS_9_12 = [
    (9, 0, "founder_media", "معيار SOAEN", "soaen-standard", "Signal · Offer · Action · Evidence · Narrative — خمس فجوات قبل أي upsell."),
    (9, 1, "proof", "لماذا 10 leads؟", "10-lead-audit", "نبدأ بـ pilot صغير — أدلة حقيقية قبل التوسع."),
    (9, 2, "objection", "حوكمة AI قبل التوسع", "govern-ai-before-scale", "لا أتمتة إرسال — موافقة بشرية على كل لمسة خارجية."),
    (9, 3, "trust", "أين يضيع الإيراد؟", "revenue-leakage-after-ads", "بعد الإعلان: لا owner · لا evidence · لا next action."),
    (9, 4, "proof", "كرّر الإيقاع", "repeat-the-rhythm", "War Room · أدلة · مسودات · منشور SOAEN — يومياً."),
    (10, 0, "founder_media", "وكالة تبيع النتيجة", "agency-proof-for-clients", "Proof Pack أسبوعي لعميل الوكالة — ليس تقريراً عاماً."),
    (10, 1, "proof", "قائمة متابعة سعودية", "saudi-agency-follow-up-checklist", "15 دقيقة owner · موافقة · evidence · تاريخ."),
    (10, 2, "objection", "موافقة AI للمبيعات", "ai-approval-sales", "مسودة → موافقة → إرسال يدوي — PDPL وثقة."),
    (10, 3, "trust", "لا CRM جديد", "not-another-crm", "طبقة فوق CRM الحالي — قرار إيراد موثّق."),
    (10, 4, "proof", "من إعلان إلى قرار", "ad-to-decision", "الحملة تجيب lead — Revenue Ops يثبت المتابعة."),
    (11, 0, "founder_media", "تشغيل 95% / موافقة 5%", "sovereign-gtm-95-5", "النظام يجهّز اليوم — أنت توافق وتُرسل."),
    (11, 1, "proof", "أول Diagnostic مدفوع", "first-paid-diagnostic", "هدف تجاري: Diagnostic + Proof قبل ميزات."),
    (11, 2, "objection", "LinkedIn يدوي", "linkedin-manual-by-design", "لا DM آلي — مسودة + أنت ترسل."),
    (11, 3, "trust", "لا واتساب بارد", "no-cold-whatsapp-policy", "قوائم warm فقط — امتثال وثقة."),
    (11, 4, "proof", "Risk Score مجاني", "post-lead-revenue-ops", "ابدأ بقياس الجاهزية — ثم Proof Pack."),
    (12, 0, "founder_media", "Unified Revenue Atlas", "crm-vs-revenue-ops", "خريطة واحدة: استراتيجية + تكتيك + أدلة."),
    (12, 1, "proof", "Sample Proof Pack", "what-is-proof-pack", "عينة عامة قبل الشراء — أقسام وحالة."),
    (12, 2, "objection", "سعر مرتفع؟", "10-lead-audit", "ابدأ بـ 499 ر.س — pilot وليس عقد سنوي."),
    (12, 3, "trust", "شريك co-sell", "partner-intro", "Motion شركاء — عميل واحد مشترك."),
    (12, 4, "proof", "جاهز للتدشين", "governed-max-launch", "صفحة /ar · funnel · آلة يومية — Soft Launch."),
]

WEEKS_13_16 = [
    (13, 0, "founder_media", "توسعة Wave 2", "abm-wave2-warm", "100–150 حساب warm فقط — بعد 3 discovery حقيقية."),
    (13, 1, "proof", "حزمة عميل قبل الاجتماع", "client-pack-sop", "War Room → client pack → Discovery سبعة أسئلة."),
    (13, 2, "objection", "لماذا لا أتمتة كاملة؟", "governed-automation-95-5", "95% تجهيز · 5% موافقة — امتثال وثقة."),
    (13, 3, "trust", "أدلة قابلة للتدقيق", "evidence-events-close", "كل إيراد مربوط بحدث في CSV."),
    (13, 4, "proof", "Motion A يومياً", "motion-a-pipeline", "10 P0 وكالات — مسودة ثم إرسال يدوي."),
    (14, 0, "founder_media", "قيمة Diagnostic", "first-paid-diagnostic-value", "4,999–15,000 ر.س — مدخل محادثة وليس CRM جديد."),
    (14, 1, "proof", "Sprint 499", "lead-intelligence-sprint", "بعد القبول — pilot صغير بأدلة."),
    (14, 2, "objection", "Growth بعد Proof", "growth-after-proof-only", "لا upsell قبل proof_pack_delivered."),
    (14, 3, "trust", "KPI من CRM فقط", "no-invented-crm-kpi", "kpi_founder_commercial_import.yaml — لا أرقام مخترعة."),
    (14, 4, "proof", "غرفة الحرب", "revenue-war-room-daily", "أعلى 10 + متابعات + أحداث اليوم."),
    (15, 0, "founder_media", "شركاء co-sell", "partner-motion-c", "Motion C — عميل مشترك · intro موثّق."),
    (15, 1, "proof", "تنفيذي AI", "executive-diagnostic-motion-d", "Motion D — حوكمة قبل توسع AI."),
    (15, 2, "objection", "PDPL والاتصال", "pdpl-contactability", "قوائم warm · موافقة · لا scraping."),
    (15, 3, "trust", "Risk Score عام", "public-risk-score-funnel", "/ar/risk-score — قياس قبل البيع."),
    (15, 4, "proof", "Learn AEO", "learn-hub-six-articles", "/ar/learn — 6+ مقالات إجابة."),
    (16, 0, "founder_media", "إطلاق مدفوع لاحقاً", "paid-launch-after-soft", "Moyasar + HubSpot — بعد أول Diagnostic."),
    (16, 1, "proof", "تتبع أول مدفوع", "first-paid-diagnostic-tracker", "invoice → payment → proof pack."),
    (16, 2, "objection", "لا إعلان قبل Proof", "no-ads-before-proof", "3–5 اجتماعات discovery قبل paid ads."),
    (16, 3, "trust", "Dealix Cloud", "dealix-cloud-founder", "Business NOW + Operator — قرار يومي."),
    (16, 4, "proof", "توسع مستدام", "sustainable-revenue-expansion", "كرّر Motion A · أدلة · شريك · retainer."),
]

WEEKS_17_20 = [
    (17, 0, "founder_media", "قيمة يومية 90 دقيقة", "founder-90min-cockpit", "brief · war-room · approvals — لا بناء ميزات قبل scope."),
    (17, 1, "proof", "حزمة عميل SOP", "client-pack-sop-daily", "generate_client_pack قبل كل Discovery."),
    (17, 2, "objection", "لماذا Soft Launch؟", "soft-launch-governed", "بيع + قمع عام بدون Moyasar حتى 3–5 اجتماعات."),
    (17, 3, "trust", "Value Plan JSON", "value-plan-json-daily", "لقطة واحدة: Motion A + KPI + gates."),
    (17, 4, "proof", "توسعة 150 حساب", "abm-150-target-pool", "Wave 2 — warm فقط · لا scraping."),
    (18, 0, "founder_media", "مسار Motion B", "motion-b-after-a", "B مباشر فقط بعد أول Proof من Motion A."),
    (18, 1, "proof", "Data Pack 1500", "data-pack-offer", "بعد قبول Diagnostic — لا upsell مبكر."),
    (18, 2, "objection", "تكامل HubSpot", "hubspot-when-ready", "Truth Matrix: أخضر فقط عند المفتاح."),
    (18, 3, "trust", "أدلة مساءً", "founder-evening-evidence", "founder_evening.ps1 — سطر واحد يومياً."),
    (18, 4, "proof", "Weekly scorecard", "weekly-scorecard-friday", "أدلة · Proof · conversion — كل جمعة."),
    (19, 0, "founder_media", "شركاء /ar/partners", "partners-funnel", "Motion D · co-sell · intro موثّق."),
    (19, 1, "proof", "Learn hub SEO", "learn-hub-aeo", "6+ مقالات — إجابة مباشرة للسوق."),
    (19, 2, "objection", "سعر Growth", "growth-2999-after-proof", "2,999 SAR/mo — بعد Proof Pack فقط."),
    (19, 3, "trust", "PDPL contactability", "pdpl-warm-lists", "قوائم opt-in · لا بارد."),
    (19, 4, "proof", "Commercial expansion", "commercial-expansion-stack", "expand_commercial_ops_all — idempotent."),
    (20, 0, "founder_media", "من 120 إلى 150", "scale-targeting-wave2", "توسعة استهداف — تدوير P0 يومي."),
    (20, 1, "proof", "20 أسبوع محتوى", "social-20-week-queue", "80–100 منشور — مسودة وموافقة."),
    (20, 2, "objection", "لا fake revenue", "no-fake-revenue-article-8", "كل رقم من CRM أو evidence."),
    (20, 3, "trust", "Paid launch gate", "paid-launch-readiness", "verify_paid_launch_readiness بعد Soft."),
    (20, 4, "proof", "أول عميل مدفوع", "first-customer-closed-loop", "Diagnostic → Proof → Sprint — حلقة واحدة."),
]

WEEKS_21_24 = [
    (21, 0, "founder_media", "من 150 إلى 200", "wave3-200-pool", "توسعة استراتيجية — inbound/AEO لا بث بارد."),
    (21, 1, "proof", "15 لمسة يومية", "fifteen-touches-quota", "موافقة ثم إرسال يدوي — حوكمة PDPL."),
    (21, 2, "objection", "لماذا لا 500 حساب؟", "wave3-gate-inbound", "Wave 3 بعد أول Proof مدفوع — ليس scraping."),
    (21, 3, "trust", "Commercial value map", "commercial-value-map", "خريطة قيمة — Diagnostic → Sprint → Growth."),
    (21, 4, "proof", "Motion C/D بعد A", "motion-cd-after-proof", "شريك وتنفيذي — بعد إثبات Motion A."),
    (22, 0, "founder_media", "تشغيل مساءً", "founder-evening-evidence", "سطر evidence واحد — يغلق اليوم."),
    (22, 1, "proof", "حزم 12 اجتماع", "twelve-meeting-packs", "prepare_soft_launch_meetings — top-12."),
    (22, 2, "objection", "Moyasar لاحقاً", "moyasar-after-soft-pass", "دفع يدوي أولاً — ثم live keys."),
    (22, 3, "trust", "Railway bootstrap", "railway-prod-bootstrap", "Alembic + War Room seed عند الإنتاج."),
    (22, 4, "proof", "Official launch verify", "official-launch-verify", "company + GTM + FE build."),
    (23, 0, "founder_media", "Unified Revenue Atlas", "unified-revenue-atlas-daily", "استراتيجية + تكتيك + أدلة — مرجع واحد."),
    (23, 1, "proof", "Full Ops Close", "full-ops-close-engine", "Champion · Procurement · زوايا إغلاق."),
    (23, 2, "objection", "لا بناء قبل scope", "no-build-before-scope", "لا ميزات قبل scope_requested."),
    (23, 3, "trust", "Article 13", "article-13-three-paid", "3 عملاء مدفوعين — بوابة توسع."),
    (23, 4, "proof", "Retainer بعد Proof", "retainer-after-proof-pack", "Managed Ops — بعد تسليم Proof."),
    (24, 0, "founder_media", "24 أسبوع محتوى", "social-24-week-cycle", "120 منشور مسودة — SOAEN أسبوعياً."),
    (24, 1, "proof", "200 هدف warm", "targeting-200-warm", "ABM wave-3 seed — تدوير P0."),
    (24, 2, "objection", "لا LinkedIn آلي", "linkedin-manual-only", "مسودة في النظام — أنت ترسل."),
    (24, 3, "trust", "Dealix Revenue OS", "dealix-revenue-os-catalog", "catalog · anti-waste · signals."),
    (24, 4, "proof", "إيراد حقيقي", "real-revenue-closed-loop", "لمسة → أدلة → دفع → Proof Pack."),
]

WEEKS_25_28 = [
    (25, 0, "founder_media", "Motions B/C/D", "motions-bcd-pipelines", "أنابيب Motions — B بعد Proof · C شريك · D تنفيذي."),
    (25, 1, "proof", "Motion B مباشر", "motion-b-direct", "B2B — governed_diagnostic بعد Motion A."),
    (25, 2, "objection", "لا فتح B مبكراً", "gate-motion-b", "أول Proof Pack قبل توسعة B2B."),
    (25, 3, "trust", "شريك Motion C", "motion-c-partner-intro", "partner_intro موثّق — لا cold."),
    (25, 4, "proof", "تنفيذي Motion D", "motion-d-executive", "executive_diagnostic — حوكمة AI."),
    (26, 0, "founder_media", "250 هدف تحضير", "wave4-250-pool", "wave4 — inbound/AEO بعد إثبات إيراد."),
    (26, 1, "proof", "أنابيب يومية", "founder-all-motions", "founder_all_motions_pipeline.py كل صباح."),
    (26, 2, "objection", "لا wave4 بارد", "wave4-warm-only", "500+ لاحقاً — محتوى + inbound فقط."),
    (26, 3, "trust", "توسعة أسبوعية CI", "weekly-expand-workflow", "GitHub Actions — expand idempotent."),
    (26, 4, "proof", "Value map API", "commercial-value-map", "خريطة قيمة + expansion status."),
    (27, 0, "founder_media", "28 أسبوع محتوى", "social-28-weeks", "140 منشور — مسودة وموافقة."),
    (27, 1, "proof", "حزم 10 اجتماعات", "ten-meeting-packs", "prepare_soft_launch_meetings --top-n 10."),
    (27, 2, "objection", "CRM حقيقي", "crm-kpi-only", "لا أرقام مخترعة في الأتمتة."),
    (27, 3, "trust", "Dual track A/B", "gtm-dual-track", "مسار A للترويج · B للops حتى Proof."),
    (27, 4, "proof", "TTV metrics", "ttv-evidence-metrics", "من evidence CSV — شركات حقيقية."),
    (28, 0, "founder_media", "إغلاق الحلقة", "close-revenue-loop", "Diagnostic → Proof → Sprint — شركة واحدة."),
    (28, 1, "proof", "Retainer لاحق", "retainer-after-proof", "Growth 2999 بعد Proof فقط."),
    (28, 2, "objection", "لا بناء قبل إيراد", "no-build-article", "بوابة القيمة مفتوحة = Motion A."),
    (28, 3, "trust", "حوكمة كاملة", "full-soaen-stack", "SOAEN في كل لمسة ومنشور."),
    (28, 4, "proof", "Dealix جاهز", "dealix-expansion-ready", "200–250 pool · 28w · 4 Motions."),
]

_ALL_WEEKS = WEEKS_9_12 + WEEKS_13_16 + WEEKS_17_20 + WEEKS_21_24 + WEEKS_25_28


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--cycle-weeks",
        type=int,
        default=DEFAULT_CYCLE_WEEKS,
        help=f"Set cycle_weeks in YAML (default {DEFAULT_CYCLE_WEEKS})",
    )
    args = ap.parse_args()

    data = yaml.safe_load(QUEUE.read_text(encoding="utf-8")) or {}
    posts = list(data.get("posts") or [])
    existing = {(int(p["week"]), int(p["day"])) for p in posts if "week" in p and "day" in p}
    added = 0
    week_defs = [w for w in _ALL_WEEKS if w[0] <= args.cycle_weeks]
    for week, day, pillar, title_ar, slug, body_hint in week_defs:
        if (week, day) in existing:
            continue
        posts.append(
            {
                "week": week,
                "day": day,
                "pillar": pillar,
                "title_ar": title_ar,
                "body_ar": f"{body_hint}\n\n#Dealix #RevenueOps #السعودية",
                "cta_ar": "Risk Score · Sample Proof · ديمو 10 دقائق",
                "aeo_slug": slug,
                "status": "draft",
            }
        )
        added += 1
    data["posts"] = posts
    data["cycle_weeks"] = args.cycle_weeks
    QUEUE.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(
        f"EXPAND_SOCIAL_QUEUE: added={added} total={len(posts)} "
        f"cycle_weeks={args.cycle_weeks}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
