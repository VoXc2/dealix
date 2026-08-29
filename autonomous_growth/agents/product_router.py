"""Legacy capability router — evidence-first compatibility mode.

The router may rank a capability hypothesis from ICP/company signals, but it may
never turn that hypothesis into a current paid offer, price, relationship,
consent, quote, or execution authority. The commercial next step remains the
Free Mini Diagnostic followed by qualified discovery.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from autonomous_growth.product_catalog import PRODUCT_CATALOG, Product, ProductTier
from core.agents.base import BaseAgent
from core.logging import get_logger

log = get_logger(__name__)

_SIZE_LARGE_TOKENS: frozenset[str] = frozenset(
    {"large", "enterprise", "كبيرة", "مؤسسة", "enterprise_large"}
)
_BAND_COLD = 0.3
_BAND_WARM = 0.5
_BAND_HOT = 0.7
_APPROVAL_REQUIRED_TIERS: frozenset[ProductTier] = frozenset(
    {ProductTier.MANAGED_OPS, ProductTier.CUSTOM_AI}
)


@dataclass
class ProductRouteDecision:
    """Internal capability-routing result; not a commercial offer decision."""

    recommended_tier: ProductTier
    product: Product
    confidence: float
    reasoning_ar: str
    reasoning_en: str
    upsell_tier: ProductTier | None
    requires_founder_approval: bool
    route_class: str = "CAPABILITY_HYPOTHESIS_ONLY"
    commercial_next_step: str = "FREE_MINI_DIAGNOSTIC_THEN_QUALIFIED_DISCOVERY"
    relationship_verified: bool = False
    consent_verified: bool = False
    offer_authorized: bool = False
    price_authorized: bool = False
    quote_authorized: bool = False
    execution_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommended_tier": self.recommended_tier.value,
            "product": self.product.to_dict(),
            "confidence": self.confidence,
            "reasoning_ar": self.reasoning_ar,
            "reasoning_en": self.reasoning_en,
            "upsell_tier": self.upsell_tier.value if self.upsell_tier else None,
            "requires_founder_approval": self.requires_founder_approval,
            "route_class": self.route_class,
            "commercial_next_step": self.commercial_next_step,
            "relationship_verified": self.relationship_verified,
            "consent_verified": self.consent_verified,
            "offer_authorized": self.offer_authorized,
            "price_authorized": self.price_authorized,
            "quote_authorized": self.quote_authorized,
            "execution_authorized": self.execution_authorized,
        }


class ProductRouterAgent(BaseAgent):
    """Rank a legacy capability hypothesis without granting commercial authority."""

    name = "product_router"

    async def run(  # type: ignore[override]
        self,
        *,
        lead_profile: dict[str, Any],
        icp_score: float,
        sector: str,
        company_size: str,
        budget_signal: str | None = None,
        **_: Any,
    ) -> ProductRouteDecision:
        del lead_profile
        icp_score = max(0.0, min(1.0, icp_score))
        size_lower = (company_size or "").lower().strip()
        budget_lower = (budget_signal or "").lower().strip()

        tier, confidence, reasoning_ar, reasoning_en = self._route(
            icp_score=icp_score,
            size_lower=size_lower,
            budget_lower=budget_lower,
            sector=sector,
        )
        product = PRODUCT_CATALOG[tier]
        route_class = "ENTRY_MOTION" if tier == ProductTier.FREE_DIAGNOSTIC else "CAPABILITY_HYPOTHESIS_ONLY"
        decision = ProductRouteDecision(
            recommended_tier=tier,
            product=product,
            confidence=confidence,
            reasoning_ar=reasoning_ar,
            reasoning_en=reasoning_en,
            upsell_tier=self._upsell(tier),
            requires_founder_approval=tier in _APPROVAL_REQUIRED_TIERS,
            route_class=route_class,
        )

        self.log.info(
            "capability_routed",
            tier=tier.value,
            confidence=confidence,
            icp_score=icp_score,
            company_size=company_size,
            route_class=route_class,
            offer_authorized=False,
            price_authorized=False,
            execution_authorized=False,
        )
        return decision

    def _route(
        self,
        *,
        icp_score: float,
        size_lower: str,
        budget_lower: str,
        sector: str,
    ) -> tuple[ProductTier, float, str, str]:
        del sector
        is_large = size_lower in _SIZE_LARGE_TOKENS or any(
            token in size_lower for token in ("enterprise", "large", "+500", ">500")
        )
        has_budget_hypothesis = any(
            keyword in budget_lower
            for keyword in ("high", "enterprise", "unlimited", "مرتفع", "مفتوح")
        )

        if icp_score < _BAND_COLD:
            return (
                ProductTier.FREE_DIAGNOSTIC,
                0.9,
                "الخطوة التجارية الوحيدة المسموح بها هنا هي التشخيص المصغر المجاني؛ لا عرض مدفوع قبل الاكتشاف المؤهل.",
                "The only current commercial next step here is the Free Mini Diagnostic; no paid offer is authorized before qualified discovery.",
            )
        if icp_score < _BAND_WARM:
            return (
                ProductTier.SPRINT,
                0.75,
                "فرضية قدرة داخلية قديمة فقط؛ تبدأ الحركة التجارية بالتشخيص المصغر المجاني ثم اكتشاف مؤهل.",
                "Legacy internal capability hypothesis only; the commercial motion still starts with a Free Mini Diagnostic and qualified discovery.",
            )
        if icp_score < _BAND_HOT:
            if has_budget_hypothesis or is_large:
                return (
                    ProductTier.MANAGED_OPS,
                    0.7,
                    "فرضية قدرة داخلية مبنية على إشارات غير سلطوية؛ لا سعر أو عرض أو صلاحية تنفيذ.",
                    "Internal capability hypothesis from non-authoritative signals; no price, offer, or execution authority is created.",
                )
            return (
                ProductTier.DATA_PACK,
                0.72,
                "فرضية قدرة داخلية فقط؛ يجب التحقق من المشكلة عبر التشخيص والاكتشاف قبل أي عرض.",
                "Internal capability hypothesis only; validate the problem through diagnostic and discovery before any offer.",
            )
        if is_large:
            return (
                ProductTier.CUSTOM_AI,
                0.8,
                "فرضية قدرة مخصصة فقط؛ لا تُعد عرضاً ولا تصريحاً سعرياً أو تعاقدياً.",
                "Custom-capability hypothesis only; this is not an offer or pricing/contract authority.",
            )
        return (
            ProductTier.MANAGED_OPS,
            0.82,
            "فرضية قدرة داخلية فقط؛ المسار التجاري الحالي يظل تشخيصاً ثم اكتشافاً ثم عرضاً خاصاً بالعميل.",
            "Internal capability hypothesis only; current commercial path remains diagnostic, discovery, then a customer-specific quote.",
        )

    @staticmethod
    def _upsell(tier: ProductTier) -> ProductTier | None:
        """Legacy capability navigation only; never an upsell authorization."""
        ladder = [
            ProductTier.FREE_DIAGNOSTIC,
            ProductTier.SPRINT,
            ProductTier.DATA_PACK,
            ProductTier.MANAGED_OPS,
            ProductTier.CUSTOM_AI,
        ]
        try:
            idx = ladder.index(tier)
            return ladder[idx + 1] if idx + 1 < len(ladder) else None
        except ValueError:
            return None
