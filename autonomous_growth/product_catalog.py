"""Legacy autonomous-growth capability catalog.

This module is retained for compatibility with older routing code. It is NOT the
current commercial pricing/offer authority. The current Dealix motion is:

Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote ->
30-Day Revenue Command Pilot -> Proof -> Stop/Expand/Recurring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProductTier(str, Enum):
    """Legacy capability taxonomy retained for compatibility only."""

    FREE_DIAGNOSTIC = "free_diagnostic"
    SPRINT = "sprint"
    DATA_PACK = "data_pack"
    MANAGED_OPS = "managed_ops"
    CUSTOM_AI = "custom_ai"


@dataclass
class Product:
    """Compatibility capability record; not a customer-specific quote."""

    id: str
    name_ar: str
    name_en: str
    tier: ProductTier
    price_sar: int
    price_max_sar: int
    description_ar: str
    description_en: str
    target_company_size: list[str]
    target_sectors: list[str]
    min_icp_score: float
    delivery_days: int
    key_outcomes: list[str] = field(default_factory=list)
    commercial_authority: str = "RETIRED_COMPATIBILITY_NOT_OFFER_AUTHORITY"
    active_offer: bool = False
    quote_required: bool = True
    price_authorized: bool = False
    delivery_authorized: bool = False

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
            "commercial_authority": self.commercial_authority,
            "active_offer": self.active_offer,
            "quote_required": self.quote_required,
            "price_authorized": self.price_authorized,
            "delivery_authorized": self.delivery_authorized,
        }


_RETIRED_AR = "تصنيف قدرات قديم للتوافق فقط؛ ليس عرضاً أو سعراً أو التزام تسليم حالياً."
_RETIRED_EN = "Legacy capability classification retained for compatibility only; not a current offer, price, or delivery commitment."

PRODUCT_CATALOG: dict[ProductTier, Product] = {
    ProductTier.FREE_DIAGNOSTIC: Product(
        id="prod_diagnostic_v1",
        name_ar="التشخيص المصغر المجاني",
        name_en="Free Mini Diagnostic",
        tier=ProductTier.FREE_DIAGNOSTIC,
        price_sar=0,
        price_max_sar=0,
        description_ar="تشخيص أولي مجاني لتحديد المشكلة، الأدلة المطلوبة، والخطوة التالية المناسبة.",
        description_en="A free initial diagnostic to clarify the problem, evidence needed, and the right next step.",
        target_company_size=["small", "medium", "large", "enterprise"],
        target_sectors=[],
        min_icp_score=0.0,
        delivery_days=1,
        key_outcomes=["Problem clarification", "Evidence gaps", "Qualified next step"],
        commercial_authority="CURRENT_ENTRY_MOTION",
        active_offer=True,
        quote_required=False,
        price_authorized=True,
        delivery_authorized=False,
    ),
    ProductTier.SPRINT: Product(
        id="prod_sprint_v1",
        name_ar="سبرينت قديم — للتوافق فقط",
        name_en="Legacy Sprint — compatibility only",
        tier=ProductTier.SPRINT,
        price_sar=0,
        price_max_sar=0,
        description_ar=_RETIRED_AR,
        description_en=_RETIRED_EN,
        target_company_size=["small", "medium"],
        target_sectors=[],
        min_icp_score=0.3,
        delivery_days=7,
        key_outcomes=[],
    ),
    ProductTier.DATA_PACK: Product(
        id="prod_data_pack_v1",
        name_ar="حزمة بيانات قديمة — للتوافق فقط",
        name_en="Legacy Data Pack — compatibility only",
        tier=ProductTier.DATA_PACK,
        price_sar=0,
        price_max_sar=0,
        description_ar=_RETIRED_AR,
        description_en=_RETIRED_EN,
        target_company_size=["small", "medium", "large"],
        target_sectors=[],
        min_icp_score=0.5,
        delivery_days=14,
        key_outcomes=[],
    ),
    ProductTier.MANAGED_OPS: Product(
        id="prod_managed_ops_v1",
        name_ar="عمليات مُدارة قديمة — للتوافق فقط",
        name_en="Legacy Managed Ops — compatibility only",
        tier=ProductTier.MANAGED_OPS,
        price_sar=0,
        price_max_sar=0,
        description_ar=_RETIRED_AR,
        description_en=_RETIRED_EN,
        target_company_size=["medium", "large"],
        target_sectors=[],
        min_icp_score=0.5,
        delivery_days=30,
        key_outcomes=[],
    ),
    ProductTier.CUSTOM_AI: Product(
        id="prod_custom_ai_v1",
        name_ar="حل مخصص قديم — للتوافق فقط",
        name_en="Legacy Custom AI — compatibility only",
        tier=ProductTier.CUSTOM_AI,
        price_sar=0,
        price_max_sar=0,
        description_ar=_RETIRED_AR,
        description_en=_RETIRED_EN,
        target_company_size=["large", "enterprise"],
        target_sectors=[],
        min_icp_score=0.7,
        delivery_days=90,
        key_outcomes=[],
    ),
}

CURRENT_PAID_MOTION: dict[str, Any] = {
    "name": "Revenue Command Pilot — 30 days",
    "price_sar": None,
    "quote_required": True,
    "requires_qualified_discovery": True,
    "commercial_authority": "CUSTOMER_SPECIFIC_QUOTE_ONLY",
    "execution_authority": False,
}
