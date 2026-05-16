"""GTM plans and scripts — deterministic artifacts."""

from __future__ import annotations

from typing import Any


def first_10_customers_plan() -> dict[str, Any]:
    return {
        "who": [
            "B2B service firms with messy pipeline + weak follow-up",
            "Fintech/processors needing governed approvals and auditability",
            "VC portfolio teams running AI fast without governance",
        ],
        "how_to_find": [
            "Founder-led warm intros only",
            "Manual shortlist of 5 high-context contacts first",
            "Reply classification loop before scaling outreach",
        ],
        "qualification": [
            "Active revenue workflow pain (pipeline, scoring, follow-up)",
            "AI usage exists but lacks source/approval boundaries",
            "Willing to run diagnostic -> sprint -> retainer path",
        ],
        "pilot_offer_ar": "نبدأ بـ Diagnostic محكوم، ثم Sprint لإثبات القيمة، ثم Retainer للتكرار الشهري.",
        "success_criteria": [
            "First 5 warm messages sent with explicit founder confirmation",
            "At least one L5 or L6 signal captured in evidence ledger",
            "Paid conversion path documented with proof links",
        ],
        "actions": [
            "Select first 5 warm contacts by strategic fit",
            "Send governed outreach draft (no autonomous send)",
            "Classify replies and log proof before building new features",
        ],
    }


def first_100_customers_plan() -> dict[str, Any]:
    return {
        "channel_mix": [
            "Founder content (Arabic case studies)",
            "Partner agencies (15–30% rev share band)",
            "Referrals from pilots",
            "Select webinars (PDPL-safe outreach)",
        ],
        "partnerships": ["Regional CRM implementers", "Supabase consultants", "GTM freelancers"],
        "referral_loop": "Give pilots a structured referral incentive after proof pack month 2.",
        "notes": ["Cold email only with suppression lists + compliance review."],
    }


def channel_strategy() -> dict[str, Any]:
    return {
        "primary": "founder_led_warm_outreach_with_governed_followup",
        "secondary": "community_opt_in_and_partner_intros",
        "avoid": ["cold_whatsapp_broadcasts", "unchecked_scraped_lists"],
    }


def partner_strategy() -> dict[str, Any]:
    return {
        "agency": {"rev_share_pct_range": [15, 30], "setup_fee_sar_range": [3000, 25000]},
        "technology": ["Supabase partners for memory hardening"],
        "positioning_ar": "الشريك يبيع التنفيذ؛ Dealix يبيع المنصة والاشتراك.",
    }


def founder_led_sales_script() -> dict[str, Any]:
    return {
        "discovery_questions": [
            "ما أهم 3 قرارات إيراد تحتاجونها هذا الأسبوع؟",
            "أين يحدث كسر الثقة بين AI output والقرار التنفيذي؟",
            "كيف تثبتون ROI اليوم بمصدر واضح وأدلة قابلة للتدقيق؟",
        ],
        "demo_story_ar": "أعرض: Source clarity → Draft with approval gate → Decision Passport → Proof Pack.",
        "objections": {
            "crm": "Dealix ليس CRM بديلاً؛ هو طبقة تشغيل محكومة فوق CRM والعمليات الحالية.",
            "price": "نبدأ بـ Diagnostic صغير عالي الوضوح، ثم Sprint عند إثبات القيمة، ثم Retainer.",
            "ai_failed_before": "النظام هنا approval-first + evidence-first، وليس agent يرسل تلقائياً.",
        },
        "pilot_framing_ar": "Sprint محكوم: ترتيب أولويات الحسابات + مخاطر الصفقات + Drafts مع موافقة + Proof Pack.",
    }
