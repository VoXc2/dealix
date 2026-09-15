"""Internal commercial catalogue.

The first paid motion is quote-only after discovery. Other numeric entries are
internal experiments and cannot authorize a quote, invoice, or checkout.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PricingTier:
    tier_id: str
    name_ar: str
    name_en: str
    price_sar: float | None
    pricing_basis: str  # "free" | "quote_only" | "recurring_monthly" | "project" | "custom"
    description_ar: str
    description_en: str
    includes: list[str]
    excludes: list[str]
    upgrade_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "tier_id": self.tier_id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "price_sar": self.price_sar,
            "pricing_basis": self.pricing_basis,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "includes": list(self.includes),
            "excludes": list(self.excludes),
            "upgrade_path": self.upgrade_path,
        }


_CATALOG: tuple[PricingTier, ...] = (
    PricingTier(
        tier_id="diagnostic",
        name_ar="Diagnostic مجاني",
        name_en="Free Growth Diagnostic",
        price_sar=0.0,
        pricing_basis="free",
        description_ar="جلسة 30-60 دقيقة لتقييم قمع المبيعات وتقديم 3 توصيات.",
        description_en="30-60 min session — pipeline assessment + 3 recommendations.",
        includes=[
            "founder_review_of_inputs",
            "3_specific_recommendations",
            "best_first_offer_recommendation",
        ],
        excludes=[
            "external_outreach",
            "data_processing_at_scale",
        ],
        upgrade_path="revenue_command_pilot_30d",
    ),
    PricingTier(
        tier_id="revenue_command_pilot_30d",
        name_ar="تجربة مركز قيادة الإيرادات — مدة مخصصة للحالة",
        name_en="Revenue Command Pilot — customer-specific duration",
        price_sar=None,
        pricing_basis="quote_only",
        description_ar="نطاق واحد بعد discovery: ICP واحد، مسار إيراد واحد، baseline وProof Pack أسبوعي.",
        description_en="One post-discovery scope: one ICP, one revenue workflow, a baseline, and weekly proof packs.",
        includes=[
            "one_icp",
            "one_revenue_workflow",
            "one_operational_baseline",
            "one_approval_queue",
            "arabic_outreach_drafts",
            "weekly_proof_pack",
        ],
        excludes=[
            "live_external_send",
            "scraped_data_sources",
        ],
        upgrade_path="monthly_revenue_governance",
    ),
    PricingTier(
        tier_id="data_to_revenue",
        name_ar="من البيانات إلى الإيراد",
        name_en="Data to Revenue",
        price_sar=1500.0,
        pricing_basis="project",
        description_ar="تنظيف قائمة + ترتيب أفضل العملاء + درجة contactability + رسائل مقسّمة.",
        description_en="List cleanup + top-customer ranking + contactability score + segmented drafts.",
        includes=[
            "list_dedup_and_normalize",
            "contactability_score",
            "segmented_message_drafts",
            "risk_report",
        ],
        excludes=[
            "live_external_send",
            "purchased_lead_lists",
        ],
        upgrade_path="executive_growth_os",
    ),
    PricingTier(
        tier_id="executive_growth_os",
        name_ar="نظام تشغيل القيادة التنفيذية",
        name_en="Executive Growth OS",
        price_sar=2999.0,
        pricing_basis="recurring_monthly",
        description_ar="حزمة أسبوعية: قرارات معلّقة، عوائق، مخاطر، فعلي مقابل التوقّع، Proof Pack شهري.",
        description_en="Weekly pack: pending decisions, blockers, risks, actual-vs-forecast + monthly Proof Pack.",
        includes=[
            "weekly_executive_brief",
            "monthly_proof_pack",
            "founder_office_hour_each_week",
            "all_lower_tier_features",
        ],
        excludes=[
            "guaranteed_revenue_promises",
            "live_external_charge",
        ],
        upgrade_path="full_control_tower_custom",
    ),
    PricingTier(
        tier_id="partnership_growth",
        name_ar="نمو الشراكات",
        name_en="Partnership Growth",
        price_sar=3000.0,  # min of the documented 3,000-7,500 range
        pricing_basis="project",
        description_ar="اكتشاف 8 فئات شراكة، fit-score، مسوّدات تواصل دافئة، Proof Pack مشترك.",
        description_en="8-category partner discovery, fit-score, warm-intro drafts, co-branded Proof Pack.",
        includes=[
            "partner_category_radar",
            "fit_score_per_partner_class",
            "warm_intro_drafts_ar_en",
            "cobranded_proof_pack_template",
        ],
        excludes=[
            "linkedin_automation",
            "scraping_partner_directories",
            "exclusivity_offers_until_3_proofs",
        ],
        upgrade_path="full_control_tower_custom",
    ),
)


def pricing_catalog() -> list[dict[str, Any]]:
    return [tier.to_dict() for tier in _CATALOG]


def get_pricing_tier(tier_id: str) -> dict[str, Any]:
    for t in _CATALOG:
        if t.tier_id == tier_id:
            return t.to_dict()
    raise KeyError(f"unknown pricing tier: {tier_id}")
