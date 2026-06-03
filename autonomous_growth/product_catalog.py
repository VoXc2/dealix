"""
Product Catalog — Dealix five-rung product ladder.
كتالوج المنتجات — السلم الخماسي لمنتجات Dealix.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProductTier(str, Enum):
    """Product tiers corresponding to the five rungs of the Dealix ladder."""

    FREE_DIAGNOSTIC = "free_diagnostic"
    SPRINT = "sprint"
    DATA_PACK = "data_pack"
    MANAGED_OPS = "managed_ops"
    CUSTOM_AI = "custom_ai"


@dataclass
class Product:
    """A single product on the Dealix ladder."""

    id: str
    name_ar: str
    name_en: str
    tier: ProductTier
    price_sar: int                             # minimum / one-time price
    price_max_sar: int                         # 0 if same as price_sar (fixed price)
    description_ar: str
    description_en: str
    target_company_size: list[str]             # e.g. ["small", "medium", "large", "enterprise"]
    target_sectors: list[str]                  # [] means all sectors
    min_icp_score: float                       # minimum ICP score to recommend this product
    delivery_days: int                         # typical delivery / onboarding duration
    key_outcomes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "tier": self.tier.value,
            "price_sar": self.price_sar,
            "price_max_sar": self.price_max_sar,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "target_company_size": self.target_company_size,
            "target_sectors": self.target_sectors,
            "min_icp_score": self.min_icp_score,
            "delivery_days": self.delivery_days,
            "key_outcomes": self.key_outcomes,
        }


# ---------------------------------------------------------------------------
# Canonical catalog — one entry per tier
# ---------------------------------------------------------------------------

PRODUCT_CATALOG: dict[ProductTier, Product] = {
    ProductTier.FREE_DIAGNOSTIC: Product(
        id="prod_diagnostic_v1",
        name_ar="تشخيص مجاني",
        name_en="Free Diagnostic",
        tier=ProductTier.FREE_DIAGNOSTIC,
        price_sar=0,
        price_max_sar=0,
        description_ar=(
            "جلسة تشخيص مجانية مدتها 30 دقيقة لتحديد أكبر فرص الإيرادات وأبرز نقاط الألم "
            "في العمليات التجارية. لا التزام، لا تكلفة."
        ),
        description_en=(
            "A free 30-minute diagnostic session to identify the top revenue opportunities "
            "and operational pain points. No commitment, no cost."
        ),
        target_company_size=["small", "medium", "large", "enterprise"],
        target_sectors=[],
        min_icp_score=0.0,
        delivery_days=1,
        key_outcomes=[
            "خريطة نقاط الألم الرئيسية",
            "توصية أولية بالمنتج المناسب",
            "Top pain-point map",
            "Initial product recommendation",
        ],
    ),
    ProductTier.SPRINT: Product(
        id="prod_sprint_v1",
        name_ar="سبرينت ذكاء الإيرادات",
        name_en="Revenue Intelligence Sprint",
        tier=ProductTier.SPRINT,
        price_sar=499,
        price_max_sar=499,
        description_ar=(
            "سبرينت لمدة أسبوع يُنتج خريطة إيرادات مفصّلة مع 3 فرص قابلة للتطبيق فوراً "
            "باستخدام بيانات السوق السعودي."
        ),
        description_en=(
            "A one-week sprint delivering a detailed revenue map with 3 immediately "
            "actionable opportunities, grounded in Saudi market data."
        ),
        target_company_size=["small", "medium"],
        target_sectors=[],
        min_icp_score=0.3,
        delivery_days=7,
        key_outcomes=[
            "خريطة إيرادات مفصّلة",
            "3 فرص نمو قابلة للتطبيق",
            "Detailed revenue map",
            "3 actionable growth opportunities",
        ],
    ),
    ProductTier.DATA_PACK: Product(
        id="prod_data_pack_v1",
        name_ar="حزمة البيانات",
        name_en="Data Pack",
        tier=ProductTier.DATA_PACK,
        price_sar=1500,
        price_max_sar=1500,
        description_ar=(
            "حزمة بيانات شاملة تتضمن تحليل قطاعي عميق وملفات ICP ومعيارة الأداء مقارنةً "
            "بالمنافسين في السوق السعودي."
        ),
        description_en=(
            "A comprehensive data package including deep sector analysis, ICP profiles, "
            "and performance benchmarking against Saudi market competitors."
        ),
        target_company_size=["small", "medium", "large"],
        target_sectors=[],
        min_icp_score=0.5,
        delivery_days=14,
        key_outcomes=[
            "تحليل قطاعي عميق",
            "ملفات ICP للعملاء المحتملين",
            "معيارة الأداء مقارنةً بالمنافسين",
            "Deep sector analysis",
            "ICP profiles for target prospects",
            "Competitor performance benchmarking",
        ],
    ),
    ProductTier.MANAGED_OPS: Product(
        id="prod_managed_ops_v1",
        name_ar="العمليات المُدارة",
        name_en="Managed Ops",
        tier=ProductTier.MANAGED_OPS,
        price_sar=2999,
        price_max_sar=4999,
        description_ar=(
            "إدارة كاملة للعمليات التسويقية والمبيعات بواسطة فريق Dealix مع تقارير شهرية "
            "ومؤشرات أداء واضحة. اشتراك شهري."
        ),
        description_en=(
            "Full management of marketing and sales operations by the Dealix team, "
            "with monthly reports and clear KPIs. Monthly retainer."
        ),
        target_company_size=["medium", "large"],
        target_sectors=[],
        min_icp_score=0.5,
        delivery_days=30,
        key_outcomes=[
            "إدارة كاملة للعمليات",
            "تقارير أداء شهرية",
            "مؤشرات نمو واضحة",
            "Full operations management",
            "Monthly performance reports",
            "Clear growth KPIs",
        ],
    ),
    ProductTier.CUSTOM_AI: Product(
        id="prod_custom_ai_v1",
        name_ar="حل ذكاء اصطناعي مخصص",
        name_en="Custom AI",
        tier=ProductTier.CUSTOM_AI,
        price_sar=5000,
        price_max_sar=25000,
        description_ar=(
            "بناء حل ذكاء اصطناعي مخصص بالكامل لاحتياجات الشركة — من التصميم إلى "
            "النشر والتدريب والتكامل مع الأنظمة الحالية."
        ),
        description_en=(
            "A fully bespoke AI solution built for the company's specific needs — "
            "from design to deployment, training, and integration with existing systems."
        ),
        target_company_size=["large", "enterprise"],
        target_sectors=[],
        min_icp_score=0.7,
        delivery_days=90,
        key_outcomes=[
            "حل ذكاء اصطناعي مخصص",
            "تكامل مع الأنظمة الحالية",
            "تدريب الفريق",
            "Bespoke AI solution",
            "Integration with existing systems",
            "Team training and handover",
        ],
    ),
}
