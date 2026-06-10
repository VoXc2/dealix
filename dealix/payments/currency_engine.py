"""Multi-currency engine for GCC payments — SAR, AED, QAR, KWD, BHD, OMR."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

import httpx

CURRENCIES: dict[str, dict[str, str]] = {
    "SAR": {
        "name": "ريال سعودي",
        "name_en": "Saudi Riyal",
        "symbol": "ر.س",
        "symbol_en": "SR",
        "code": "SAR",
        "subunit": "هللة",
        "subunit_en": "Halala",
        "decimal_places": "2",
    },
    "AED": {
        "name": "درهم إماراتي",
        "name_en": "UAE Dirham",
        "symbol": "د.إ",
        "symbol_en": "AED",
        "code": "AED",
        "subunit": "فلس",
        "subunit_en": "Fils",
        "decimal_places": "2",
    },
    "QAR": {
        "name": "ريال قطري",
        "name_en": "Qatari Riyal",
        "symbol": "ر.ق",
        "symbol_en": "QR",
        "code": "QAR",
        "subunit": "درهم",
        "subunit_en": "Dirham",
        "decimal_places": "2",
    },
    "KWD": {
        "name": "دينار كويتي",
        "name_en": "Kuwaiti Dinar",
        "symbol": "د.ك",
        "symbol_en": "KD",
        "code": "KWD",
        "subunit": "فلس",
        "subunit_en": "Fils",
        "decimal_places": "3",
    },
    "BHD": {
        "name": "دينار بحريني",
        "name_en": "Bahraini Dinar",
        "symbol": "د.ب",
        "symbol_en": "BD",
        "code": "BHD",
        "subunit": "فلس",
        "subunit_en": "Fils",
        "decimal_places": "3",
    },
    "OMR": {
        "name": "ريال عماني",
        "name_en": "Omani Riyal",
        "symbol": "ر.ع",
        "symbol_en": "OMR",
        "code": "OMR",
        "subunit": "بيسة",
        "subunit_en": "Baisa",
        "decimal_places": "3",
    },
}

# Fixed exchange rates (SAR as base, approximate pegs — updated periodically)
# SAR is pegged to USD at 3.75, other GCC currencies are also USD-pegged
_PEGGED_RATES: dict[str, dict[str, float]] = {
    "SAR": {"AED": 0.98, "QAR": 0.97, "KWD": 0.081, "BHD": 0.10, "OMR": 0.10, "USD": 0.27},
    "AED": {"SAR": 1.02, "QAR": 0.99, "KWD": 0.083, "BHD": 0.10, "OMR": 0.10, "USD": 0.27},
    "QAR": {"SAR": 1.03, "AED": 1.01, "KWD": 0.084, "BHD": 0.10, "OMR": 0.10, "USD": 0.27},
    "KWD": {"SAR": 12.35, "AED": 12.05, "QAR": 11.90, "BHD": 1.23, "OMR": 1.23, "USD": 3.29},
    "BHD": {"SAR": 10.00, "AED": 9.76, "QAR": 9.64, "KWD": 0.81, "OMR": 1.00, "USD": 2.66},
    "OMR": {"SAR": 9.84, "AED": 9.60, "QAR": 9.48, "KWD": 0.81, "BHD": 1.00, "USD": 2.60},
}


@dataclass
class ConversionResult:
    """Result of a currency conversion."""
    amount: Decimal
    from_currency: str
    to_currency: str
    converted_amount: Decimal
    rate: Decimal
    formatted_from: str
    formatted_to: str
    use_live_rate: bool = False


class CurrencyEngine:
    """Multi-currency engine for GCC region payments.

    Supports SAR, AED, QAR, KWD, BHD, OMR with pegged rates and
    optional live rate fetching.
    """

    CURRENCIES = CURRENCIES

    def __init__(self, use_live_rates: bool = False, api_key: str | None = None) -> None:
        self._use_live = use_live_rates
        self._api_key = api_key

    def _get_live_rate(self, from_curr: str, to_curr: str) -> float | None:
        """Try to fetch a live exchange rate.

        Falls back to pegged rates if live rates fail.
        """
        # Try free exchangerate API
        if self._api_key:
            return None  # Placeholder for actual API call
        return None

    async def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between two GCC currencies.

        Args:
            from_currency: Source currency code (e.g., "SAR").
            to_currency: Target currency code (e.g., "AED").

        Returns:
            Exchange rate as float.
        """
        from_curr = from_currency.upper().strip()
        to_curr = to_currency.upper().strip()

        if from_curr == to_curr:
            return 1.0

        # Try live rates first
        if self._use_live:
            live = self._get_live_rate(from_curr, to_curr)
            if live is not None:
                return live

        # Fall back to pegged rates
        if from_curr in _PEGGED_RATES and to_curr in _PEGGED_RATES[from_curr]:
            return _PEGGED_RATES[from_curr][to_curr]

        # Try reverse rate
        if to_curr in _PEGGED_RATES and from_curr in _PEGGED_RATES[to_curr]:
            return 1.0 / _PEGGED_RATES[to_curr][from_curr]

        msg = f"No rate available for {from_curr} -> {to_curr}"
        raise ValueError(msg)

    async def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> ConversionResult:
        """Convert an amount between GCC currencies.

        Args:
            amount: Amount to convert.
            from_currency: Source currency code.
            to_currency: Target currency code.

        Returns:
            ConversionResult with formatted values.
        """
        from_curr = from_currency.upper().strip()
        to_curr = to_currency.upper().strip()

        if from_curr == to_curr:
            rate = Decimal("1.0")
            converted = Decimal(str(amount))
        else:
            rate = Decimal(str(await self.get_rate(from_curr, to_curr)))
            converted = (Decimal(str(amount)) * rate).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )

        return ConversionResult(
            amount=Decimal(str(amount)),
            from_currency=from_curr,
            to_currency=to_curr,
            converted_amount=converted,
            rate=rate,
            formatted_from=self.format_amount(amount, from_curr),
            formatted_to=self.format_amount(float(converted), to_curr),
        )

    def format_amount(self, amount: float, currency: str) -> str:
        """Format a monetary amount for a GCC currency.

        Args:
            amount: The numeric amount.
            currency: Currency code (SAR, AED, etc.).

        Returns:
            Formatted string with currency symbol.
        """
        curr = currency.upper().strip()
        currency_info = CURRENCIES.get(curr)
        if not currency_info:
            return f"{amount:.2f} {curr}"

        decimal_places = int(currency_info.get("decimal_places", "2"))
        formatted = f"{amount:,.{decimal_places}f}"

        if curr == "KWD":
            return f"{formatted} {currency_info['symbol']}"
        return f"{formatted} {currency_info['symbol']}"

    def format_amount_en(self, amount: float, currency: str) -> str:
        """Format amount in English style (symbol before amount).

        Args:
            amount: The numeric amount.
            currency: Currency code.

        Returns:
            Formatted string (e.g., "SR 1,000.00").
        """
        curr = currency.upper().strip()
        currency_info = CURRENCIES.get(curr)
        if not currency_info:
            return f"{curr} {amount:.2f}"

        decimal_places = int(currency_info.get("decimal_places", "2"))
        formatted = f"{amount:,.{decimal_places}f}"
        symbol_en = currency_info.get("symbol_en", curr)

        return f"{symbol_en} {formatted}"

    @staticmethod
    def parse_amount(amount_str: str) -> Decimal | None:
        """Parse a currency string into a Decimal amount.

        Handles Arabic and English formatted amounts.
        """
        # Remove common symbols and non-digit chars (except . , -)
        cleaned = amount_str.strip()
        arabic_digits = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
        cleaned = cleaned.translate(arabic_digits)

        for sym in ["ر.س", "د.إ", "ر.ق", "د.ك", "د.ب", "ر.ع", "SR", "AED", "QR", "KD", "BD", "OMR", "$", ","]:
            cleaned = cleaned.replace(sym, "")

        cleaned = cleaned.strip()

        try:
            return Decimal(cleaned)
        except Exception:
            return None

    @staticmethod
    def get_currency_info(currency: str) -> dict[str, str] | None:
        """Get detailed info about a GCC currency."""
        return CURRENCIES.get(currency.upper().strip())


__all__ = [
    "CURRENCIES",
    "ConversionResult",
    "CurrencyEngine",
]
