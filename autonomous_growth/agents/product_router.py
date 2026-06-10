"""
Product Router Agent — matches a lead profile to the optimal product tier.
وكيل توجيه المنتجات — يطابق ملف العميل مع المنتج الأنسب.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from autonomous_growth.product_catalog import PRODUCT_CATALOG, Product, ProductTier
from core.agents.base import BaseAgent
from core.logging import get_logger

log = get_logger(__name__)

# Company-size buckets — map from free-text signal to canonical key
_SIZE_LARGE_TOKENS: frozenset[str] = frozenset(
    {"large", "enterprise", "كبيرة", "مؤسسة", "enterprise_large"}
)

# ICP score band boundaries
_BAND_COLD = 0.3
_BAND_WARM = 0.5
_BAND_HOT = 0.7

# Tiers that always require founder approval before a proposal is sent
_APPROVAL_REQUIRED_TIERS: frozenset[ProductTier] = frozenset(
    {ProductTier.MANAGED_OPS, ProductTier.CUSTOM_AI}
)


@dataclass
class ProductRouteDecision:
    """Decision produced by ProductRouterAgent."""

    recommended_tier: ProductTier
    product: Product
    confidence: float                       # 0.0 – 1.0
    reasoning_ar: str
    reasoning_en: str
    upsell_tier: ProductTier | None
    requires_founder_approval: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommended_tier": self.recommended_tier.value,
            "product": self.product.to_dict(),
            "confidence": self.confidence,
            "reasoning_ar": self.reasoning_ar,
            "reasoning_en": self.reasoning_en,
            "upsell_tier": self.upsell_tier.value if self.upsell_tier else None,
            "requires_founder_approval": self.requires_founder_approval,
        }


class ProductRouterAgent(BaseAgent):
    """
    Routes a lead to the most appropriate product tier using ICP score,
    company size, sector, and optional budget signal.

    يوجّه العميل المحتمل إلى المنتج الأنسب بناءً على درجة ICP وحجم الشركة
    والقطاع وإشارة الميزانية.
    """

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
        """
        Determine the best product tier for the lead.

        Routing logic:
          icp_score < 0.3   → Free Diagnostic
          0.3 – 0.5         → Sprint
          0.5 – 0.7         → Data Pack (default) or Managed Ops if budget allows
          0.7+              → Managed Ops (default) or Custom AI if large/enterprise
          Large enterprise  → always consider Custom AI at score 0.7+
        """
        icp_score = max(0.0, min(1.0, icp_score))  # clamp
        size_lower = (company_size or "").lower().strip()
        budget_lower = (budget_signal or "").lower().strip()

        tier, confidence, reasoning_ar, reasoning_en = self._route(
            icp_score=icp_score,
            size_lower=size_lower,
            budget_lower=budget_lower,
            sector=sector,
        )

        upsell_tier = self._upsell(tier)
        product = PRODUCT_CATALOG[tier]
        requires_approval = tier in _APPROVAL_REQUIRED_TIERS

        decision = ProductRouteDecision(
            recommended_tier=tier,
            product=product,
            confidence=confidence,
            reasoning_ar=reasoning_ar,
            reasoning_en=reasoning_en,
            upsell_tier=upsell_tier,
            requires_founder_approval=requires_approval,
        )

        self.log.info(
            "product_routed",
            tier=tier.value,
            confidence=confidence,
            icp_score=icp_score,
            company_size=company_size,
            requires_approval=requires_approval,
        )
        return decision

    # ── Private routing helpers ────────────────────────────────────

    def _route(
        self,
        *,
        icp_score: float,
        size_lower: str,
        budget_lower: str,
        sector: str,
    ) -> tuple[ProductTier, float, str, str]:
        """Return (tier, confidence, reasoning_ar, reasoning_en)."""

        is_large = size_lower in _SIZE_LARGE_TOKENS or any(
            t in size_lower for t in ("enterprise", "large", "+500", ">500")
        )
        has_budget = any(
            kw in budget_lower
            for kw in ("high", "enterprise", "unlimited", "مرتفع", "مفتوح")
        )

        if icp_score < _BAND_COLD:
            return (
                ProductTier.FREE_DIAGNOSTIC,
                0.9,
                "درجة ICP منخفضة — يُنصح بالتشخيص المجاني أولاً لفهم احتياجات الشركة.",
                "Low ICP score — recommend the free diagnostic to understand the company's needs first.",
            )

        if icp_score < _BAND_WARM:
            return (
                ProductTier.SPRINT,
                0.75,
                "درجة ICP متوسطة — سبرينت ذكاء الإيرادات هو الخطوة الأنسب لبناء الأساس.",
                "Moderate ICP score — the Revenue Intelligence Sprint is the right step to build the foundation.",
            )

        if icp_score < _BAND_HOT:
            if has_budget or is_large:
                return (
                    ProductTier.MANAGED_OPS,
                    0.7,
                    "درجة ICP جيدة مع ميزانية مرتفعة — العمليات المُدارة توفر أعلى قيمة.",
                    "Good ICP score with high budget signal — Managed Ops delivers the highest value.",
                )
            return (
                ProductTier.DATA_PACK,
                0.72,
                "درجة ICP جيدة — حزمة البيانات توفر تحليلاً عميقاً للانطلاق بثقة.",
                "Good ICP score — the Data Pack provides deep analysis to move forward confidently.",
            )

        # icp_score >= 0.7
        if is_large:
            return (
                ProductTier.CUSTOM_AI,
                0.8,
                "درجة ICP عالية وشركة كبيرة — حل الذكاء الاصطناعي المخصص هو الأنسب.",
                "High ICP score and large/enterprise company — the Custom AI solution is the best fit.",
            )
        return (
            ProductTier.MANAGED_OPS,
            0.82,
            "درجة ICP عالية — العمليات المُدارة هي الخيار الأمثل لتحقيق نمو مستدام.",
            "High ICP score — Managed Ops is the optimal choice for sustainable growth.",
        )

    @staticmethod
    def _upsell(tier: ProductTier) -> ProductTier | None:
        """Return the next tier up, or None if already at the top."""
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
