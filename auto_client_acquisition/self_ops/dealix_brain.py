"""
Dealix's own Company Brain — used by self_ops runner so Dealix runs
its own daily-ops on itself (eat-our-own-dogfood pattern).
"""

from __future__ import annotations

from typing import Any


DEALIX_BRAIN: dict[str, Any] = {
    "company_name": "Dealix",
    "website": "https://dealix.me",
    "sector": "Saudi B2B SaaS",
    "city": "Riyadh",
    "offer_ar": (
        "Saudi Revenue Operating System — يجلب فرص B2B، يؤهلها، يحميها "
        "قانونياً (PDPL)، ويسلم Proof Pack موقَّع HMAC خلال 7 أيام."
    ),
    "ideal_customer_ar": (
        "وكالات تسويق B2B سعودية / شركات SaaS / شركات استشارية، 10-50 موظف، "
        "تبيع بـ 3,000+ SAR per deal، عندها LinkedIn presence، pipeline فوضوي، "
        "بدون RevOps قوي."
    ),
    "average_deal_value_sar": 3499.0,  # Pilot 499 + Growth OS 2999/month
    "approved_channels": ["linkedin_manual", "email_draft", "referral_intro"],
    "blocked_channels": ["cold_whatsapp", "linkedin_auto_dm", "purchased_list_blast"],
    "tone_ar": "professional_saudi_arabic",
    "forbidden_claims": ["نضمن", "ضمان نتائج", "guaranteed", "guaranteed results"],
    "current_service_id": "executive_growth_os",
}


# A starter list of 30 ICP-fit prospect templates (no real names) so the
# runner can simulate prospect creation when no real data exists yet.
DEALIX_ICP_SEED_PROSPECTS: tuple[dict[str, Any], ...] = (
    {"name_template": "وكالة B2B في الرياض #{n}", "city": "Riyadh", "sector": "B2B Marketing"},
    {"name_template": "شركة SaaS صاعدة في الرياض #{n}", "city": "Riyadh", "sector": "SaaS"},
    {"name_template": "وكالة تدريب احترافي #{n}", "city": "Riyadh", "sector": "Training"},
    {"name_template": "شركة استشارات إدارية #{n}", "city": "Jeddah", "sector": "Consulting"},
    {"name_template": "وكالة logistics B2B #{n}", "city": "Dammam", "sector": "Logistics"},
    {"name_template": "شركة fintech صاعدة #{n}", "city": "Riyadh", "sector": "Fintech"},
    {"name_template": "شركة cybersecurity #{n}", "city": "Riyadh", "sector": "Cybersecurity"},
    {"name_template": "شركة HR/recruitment #{n}", "city": "Jeddah", "sector": "HR"},
)


def expand_seed_prospects(start_n: int = 1, count: int = 6) -> list[dict[str, Any]]:
    """Expand the seed templates into N concrete prospect entries."""
    out: list[dict[str, Any]] = []
    for i in range(count):
        tpl = DEALIX_ICP_SEED_PROSPECTS[i % len(DEALIX_ICP_SEED_PROSPECTS)]
        n = start_n + i
        out.append({
            "name": tpl["name_template"].format(n=n),
            "company": tpl["name_template"].format(n=n),
            "sector": tpl["sector"],
            "city": tpl["city"],
            "relationship_type": "warm_2nd_degree",
            "source_type": "self_ops_seed",
            "expected_value_sar": 3499.0,
            "next_step_ar": "Dealix self-ops: ابحث عن decision-maker → warm intro",
        })
    return out
