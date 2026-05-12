"""
Pan-GCC currency formatting + minor-unit conversion.

The six GCC currencies use either 2-decimal (SAR/AED/QAR) or 3-decimal
(KWD/BHD/OMR) minor units. Hand-rolled formatting is a recurring source
of bugs (rendering 1.500 KWD as 150 fils etc.); this module is the single
source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencyInfo:
    code: str
    decimals: int
    symbol_ar: str
    symbol_en: str
    country: str
    weekend_days: tuple[int, ...]  # 0 = Monday, 6 = Sunday


# Keyed by ISO 4217 alpha code.
GCC_CURRENCIES: dict[str, CurrencyInfo] = {
    "SAR": CurrencyInfo("SAR", 2, "ر.س", "SAR", "SA", (4, 5)),  # Fri+Sat weekend
    "AED": CurrencyInfo("AED", 2, "د.إ", "AED", "AE", (5, 6)),  # Sat+Sun (post-2022)
    "QAR": CurrencyInfo("QAR", 2, "ر.ق", "QAR", "QA", (4, 5)),
    "KWD": CurrencyInfo("KWD", 3, "د.ك", "KWD", "KW", (4, 5)),
    "BHD": CurrencyInfo("BHD", 3, "د.ب", "BHD", "BH", (4, 5)),
    "OMR": CurrencyInfo("OMR", 3, "ر.ع", "OMR", "OM", (4, 5)),
}


def to_minor(amount: float | Decimal, currency: str) -> int:
    """Convert a major-unit amount (e.g. 12.50 SAR) into minor units (1250)."""
    info = GCC_CURRENCIES.get(currency.upper())
    if info is None:
        raise ValueError(f"unknown_gcc_currency:{currency}")
    multiplier = Decimal(10) ** info.decimals
    return int((Decimal(str(amount)) * multiplier).to_integral_value())


def from_minor(amount_minor: int, currency: str) -> Decimal:
    info = GCC_CURRENCIES.get(currency.upper())
    if info is None:
        raise ValueError(f"unknown_gcc_currency:{currency}")
    return Decimal(amount_minor) / (Decimal(10) ** info.decimals)


def format_amount(
    amount_minor: int, currency: str, *, locale: str = "en"
) -> str:
    """Format `amount_minor` as e.g. '12.50 SAR' (en) or '12.50 ر.س' (ar)."""
    info = GCC_CURRENCIES.get(currency.upper())
    if info is None:
        raise ValueError(f"unknown_gcc_currency:{currency}")
    major = from_minor(amount_minor, currency)
    symbol = info.symbol_ar if locale.startswith("ar") else info.symbol_en
    fmt = f"{{:,.{info.decimals}f}} {symbol}"
    return fmt.format(major)


def is_weekend(currency_country: str, weekday: int) -> bool:
    """`weekday` is `datetime.weekday()` (Mon=0)."""
    for info in GCC_CURRENCIES.values():
        if info.country == currency_country.upper():
            return weekday in info.weekend_days
    return False
