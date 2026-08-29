"""Legacy capability catalog adapter for the Revenue Execution OS.

This adapter intentionally does not expose paid price authority. The historical
five-rung taxonomy is compatibility metadata only. Current paid commercial terms
must come from qualified discovery + a customer-specific approved quote.
"""

from __future__ import annotations

from autonomous_growth.product_catalog import (
    CURRENT_PAID_MOTION,
    PRODUCT_CATALOG,
    Product,
    ProductTier,
)

LADDER: tuple[ProductTier, ...] = (
    ProductTier.FREE_DIAGNOSTIC,
    ProductTier.SPRINT,
    ProductTier.DATA_PACK,
    ProductTier.MANAGED_OPS,
    ProductTier.CUSTOM_AI,
)


def all_products() -> list[Product]:
    return [PRODUCT_CATALOG[tier] for tier in LADDER]


def product_by_id(product_id: str) -> Product | None:
    for product in PRODUCT_CATALOG.values():
        if product.id == product_id:
            return product
    return None


def product_by_tier(tier: ProductTier | str) -> Product | None:
    if isinstance(tier, str):
        try:
            tier = ProductTier(tier)
        except ValueError:
            return None
    return PRODUCT_CATALOG.get(tier)


def is_valid_product_id(product_id: str) -> bool:
    return product_by_id(product_id) is not None


def price_band(product_id: str) -> tuple[int, int]:
    """Expose only the zero-price Free Mini Diagnostic entry motion."""
    product = product_by_id(product_id)
    if product is None:
        raise KeyError(f"unknown_product_id:{product_id}")
    if product.tier != ProductTier.FREE_DIAGNOSTIC:
        raise PermissionError("CUSTOMER_SPECIFIC_QUOTE_REQUIRED")
    return (0, 0)


def next_rung(product_id: str) -> Product | None:
    """Compatibility taxonomy navigation only; never a commercial recommendation."""
    product = product_by_id(product_id)
    if product is None:
        return None
    idx = LADDER.index(product.tier)
    if idx + 1 >= len(LADDER):
        return None
    return PRODUCT_CATALOG[LADDER[idx + 1]]


def ladder_summary() -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for rung, tier in enumerate(LADDER):
        product = PRODUCT_CATALOG[tier]
        summary.append(
            {
                "rung": rung,
                "id": product.id,
                "tier": tier.value,
                "name_ar": product.name_ar,
                "name_en": product.name_en,
                "price_min_sar": 0 if tier == ProductTier.FREE_DIAGNOSTIC else None,
                "price_max_sar": 0 if tier == ProductTier.FREE_DIAGNOSTIC else None,
                "delivery_days": product.delivery_days if product.delivery_authorized else None,
                "min_icp_score": product.min_icp_score,
                "active_offer": product.active_offer,
                "commercial_authority": product.commercial_authority,
                "quote_required": product.quote_required,
            }
        )
    return summary


def current_paid_motion() -> dict[str, object]:
    return dict(CURRENT_PAID_MOTION)


__all__ = [
    "LADDER",
    "Product",
    "ProductTier",
    "all_products",
    "current_paid_motion",
    "is_valid_product_id",
    "ladder_summary",
    "next_rung",
    "price_band",
    "product_by_id",
    "product_by_tier",
]
