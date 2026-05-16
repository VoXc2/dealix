"""Value-based pricing engine (rules + mock; no live charge)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PricingQuote:
    offer_tier: str
    base_sar: float
    value_multiplier: float
    quoted_sar: float
    rationale_ar: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "offer_tier": self.offer_tier,
            "base_sar": self.base_sar,
            "value_multiplier": self.value_multiplier,
            "quoted_sar": self.quoted_sar,
            "rationale_ar": self.rationale_ar,
        }


_TIER_BASE: dict[str, float] = {
    "diagnostic": 0.0,
    "pilot_499": 499.0,
    "data_pack_1500": 1500.0,
    "managed_ops_monthly": 2999.0,
    "enterprise_custom": 25000.0,
}


def quote_value_based(
    *,
    offer_tier: str,
    measured_value_sar: float,
    evidence_level: str = "L2",
) -> PricingQuote:
    """Compute a quote from delivered value signals — deterministic mock."""
    base = _TIER_BASE.get(offer_tier.strip().lower(), 1500.0)
    level = evidence_level.strip().upper()
    multiplier = 1.0
    if level in ("L4", "L5"):
        multiplier = min(1.5, 1.0 + measured_value_sar / 100_000.0)
    elif level in ("L0", "L1"):
        multiplier = 0.85
    quoted = round(base * multiplier, 2)
    rationale = (
        f"تسعير مبني على قيمة موثقة ({measured_value_sar:.0f} ر.س) ومستوى دليل {level}"
    )
    return PricingQuote(
        offer_tier=offer_tier,
        base_sar=base,
        value_multiplier=multiplier,
        quoted_sar=quoted,
        rationale_ar=rationale,
    )
