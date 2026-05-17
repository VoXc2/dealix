"""GTM plans and scripts — deterministic artifacts."""

from __future__ import annotations

from typing import Any


def first_10_customers_plan() -> dict[str, Any]:
    return {
        "who": [
            "B2B service firms with messy pipeline and weak follow-up",
            "Clinic operators needing governed patient acquisition workflows",
            "Regulated teams (fintech / compliance-heavy) needing approval-first automation",
        ],
        "how_to_find": [
            "Founder-led warm intros and manual outreach",
            "Proof-led LinkedIn conversations using sample proof packs",
            "Partner intros from CRM/AI/GRC implementers",
        ],
        "qualification": [
            "Willing to run a paid 7-day diagnostic",
            "Has at least one revenue workflow with decision ambiguity",
            "Accepts approval-first policy for external actions",
        ],
        "pilot_offer_ar": "تشخيص محكوم لمدة 7 أيام مع Proof Pack و3 قرارات تشغيلية قابلة للتنفيذ.",
        "success_criteria": [
            ">=1 paid diagnostic invoice",
            ">=1 proof pack delivered with source-backed findings",
            ">=1 sprint-qualified opportunity",
        ],
        "actions": [
            "Build list of 50 target accounts and run trust-first outreach",
            "Push sample proof pack + risk score CTA in every qualified conversation",
            "Book meetings only after qualification around source/approval/evidence gaps",
        ],
    }


def first_100_customers_plan() -> dict[str, Any]:
    return {
        "channel_mix": [
            "Founder-led trust motion (LinkedIn + warm network)",
            "Proof-led funnel (sample pack -> risk score -> scope call)",
            "Partner-led growth from implementers and consultants",
            "Authority content on governance failures and evidence trails",
        ],
        "partnerships": [
            "CRM implementers",
            "AI consultants",
            "GRC/security consultants",
            "ERP/accounting consultants",
        ],
        "referral_loop": "No discount without exchange (testimonial/referral/faster payment/partner intro).",
        "notes": ["Never run external autonomous messaging; keep human approval for every outbound action."],
    }


def channel_strategy() -> dict[str, Any]:
    return {
        "primary": "founder_led_trust_density",
        "secondary": "proof_led_funnel_with_sample_pack",
        "tertiary": "partner_led_distribution",
        "avoid": ["cold_whatsapp_broadcasts", "unchecked_scraped_lists", "volume-first-automation"],
    }


def partner_strategy() -> dict[str, Any]:
    return {
        "referral": {"fee_pct_range": [10, 20]},
        "delivery_models": [
            "joint_diagnostic",
            "white_label_diagnostic",
            "implementation_handoff",
            "portfolio_package",
        ],
        "positioning_ar": "الشريك يجلب العميل؛ Dealix تقدم التشخيص والـproof والحوكمة قبل/مع التنفيذ.",
    }


def founder_led_sales_script() -> dict[str, Any]:
    return {
        "discovery_questions": [
            "أين يضيع الإيراد اليوم تحديداً؟",
            "هل CRM موثوق كمصدر قرار أم فيه فجوات جودة؟",
            "من يوافق على الأفعال الخارجية المرتبطة بالذكاء الاصطناعي؟",
            "ما الدليل الذي تستخدمونه لإثبات قيمة الـworkflow الحالي؟",
        ],
        "positioning_opening_ar": (
            "نحن لا نبيع chatbot ولا automation عامة؛ نحول AI وتجارب الإيراد "
            "إلى تشغيل محكوم: مصدر واضح، موافقة واضحة، دليل واضح، وقيمة قابلة للقياس."
        ),
        "demo_story_ar": (
            "أعرض workflow واحداً: source clarity -> approval boundary -> evidence trail "
            "-> governed decision -> proof pack."
        ),
        "objections": {
            "crm": "Dealix ليست CRM بديلة؛ هي طبقة تشغيل حاكمة فوق CRM والـworkflows.",
            "price": "السعر يعكس تقليل مخاطر القرارات الخاطئة وإنتاج proof قابل للتدقيق.",
            "ai_failed_before": "نشتغل approval-first وevidence-first، بدون أي إرسال خارجي تلقائي.",
        },
        "diagnostic_framing_ar": "7 أيام: Workflow map + quality + approvals + evidence + Top 3 decisions + Proof Pack.",
    }
