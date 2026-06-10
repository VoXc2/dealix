"""Multi-VAT engine for GCC countries — SA 15%, AE 5%, others 0%."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

# Standard VAT rates across GCC countries
VAT_RATES: dict[str, Decimal] = {
    "SA": Decimal("0.15"),  # 15% (KSA — standard since July 2020)
    "AE": Decimal("0.05"),  # 5%  (UAE — standard)
    "QA": Decimal("0.0"),   # 0%  (Qatar — no VAT currently)
    "KW": Decimal("0.0"),   # 0%  (Kuwait — no VAT currently)
    "BH": Decimal("0.0"),   # 0%  (Bahrain — 10% on some, 0% standard)
    "OM": Decimal("0.0"),   # 0%  (Oman — no VAT currently)
}

COUNTRY_NAMES: dict[str, dict[str, str]] = {
    "SA": {"ar": "المملكة العربية السعودية", "en": "Saudi Arabia"},
    "AE": {"ar": "الإمارات العربية المتحدة", "en": "United Arab Emirates"},
    "QA": {"ar": "قطر", "en": "Qatar"},
    "KW": {"ar": "الكويت", "en": "Kuwait"},
    "BH": {"ar": "البحرين", "en": "Bahrain"},
    "OM": {"ar": "عمان", "en": "Oman"},
}

COUNTRY_CURRENCIES: dict[str, str] = {
    "SA": "SAR", "AE": "AED", "QA": "QAR",
    "KW": "KWD", "BH": "BHD", "OM": "OMR",
}


@dataclass
class VATResult:
    """VAT calculation result for an amount."""
    amount: Decimal
    vat_rate: Decimal
    vat_percentage: str
    vat_amount: Decimal
    total_with_vat: Decimal
    country: str
    country_name_ar: str
    country_name_en: str
    currency: str
    formatted_amount: str
    formatted_vat: str
    formatted_total: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "amount": str(self.amount),
            "vat_rate": str(self.vat_rate),
            "vat_percentage": self.vat_percentage,
            "vat_amount": str(self.vat_amount),
            "total_with_vat": str(self.total_with_vat),
            "country": self.country,
            "country_name_ar": self.country_name_ar,
            "country_name_en": self.country_name_en,
            "currency": self.currency,
            "formatted_amount": self.formatted_amount,
            "formatted_vat": self.formatted_vat,
            "formatted_total": self.formatted_total,
        }


@dataclass
class InvoiceLine:
    """A single invoice line item."""
    description: str
    description_ar: str
    quantity: Decimal
    unit_price: Decimal
    vat_rate: Decimal
    discount: Decimal = Decimal("0.0")

    @property
    def net_amount(self) -> Decimal:
        return (self.quantity * self.unit_price - self.discount).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )

    @property
    def vat_amount(self) -> Decimal:
        return (self.net_amount * self.vat_rate).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )

    @property
    def total_amount(self) -> Decimal:
        return (self.net_amount + self.vat_amount).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )


@dataclass
class Invoice:
    """Complete invoice with multi-currency and VAT support."""
    invoice_number: str
    customer_name: str
    customer_vat: str | None
    country: str
    currency: str
    lines: list[InvoiceLine] = field(default_factory=list)
    notes: str = ""
    notes_ar: str = ""

    @property
    def subtotal(self) -> Decimal:
        return sum(line.net_amount for line in self.lines)

    @property
    def vat_total(self) -> Decimal:
        return sum(line.vat_amount for line in self.lines)

    @property
    def grand_total(self) -> Decimal:
        return self.subtotal + self.vat_total

    def to_dict(self) -> dict[str, Any]:
        return {
            "invoice_number": self.invoice_number,
            "customer_name": self.customer_name,
            "customer_vat": self.customer_vat,
            "country": self.country,
            "currency": self.currency,
            "lines": [
                {
                    "description": l.description,
                    "description_ar": l.description_ar,
                    "quantity": str(l.quantity),
                    "unit_price": str(l.unit_price),
                    "vat_rate": str(l.vat_rate),
                    "discount": str(l.discount),
                    "net_amount": str(l.net_amount),
                    "vat_amount": str(l.vat_amount),
                    "total_amount": str(l.total_amount),
                }
                for l in self.lines
            ],
            "subtotal": str(self.subtotal),
            "vat_total": str(self.vat_total),
            "grand_total": str(self.grand_total),
        }


class VATEngine:
    """Multi-VAT engine for GCC countries.

    Handles VAT calculation, invoice generation, and compliance
    for all six GCC countries with different VAT regimes.
    """

    VAT_RATES = VAT_RATES

    def __init__(self) -> None:
        pass

    async def calculate_vat(
        self,
        amount: float,
        country: str,
    ) -> VATResult:
        """Calculate VAT for a given amount and country.

        Args:
            amount: The pre-VAT amount.
            country: ISO country code (SA, AE, QA, KW, BH, OM).

        Returns:
            VATResult with breakdown.
        """
        country = country.upper().strip()
        vat_rate = VAT_RATES.get(country, Decimal("0.0"))
        currency = COUNTRY_CURRENCIES.get(country, "SAR")

        amount_dec = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        vat_amount = (amount_dec * vat_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total = amount_dec + vat_amount

        country_names = COUNTRY_NAMES.get(country, {"ar": "", "en": ""})

        def _fmt(val: Decimal, curr: str) -> str:
            dec_places = 3 if curr in ("KWD", "BHD", "OMR") else 2
            formatted = f"{val:,.{dec_places}f}"
            symbols = {"SAR": "ر.س", "AED": "د.إ", "QAR": "ر.ق",
                       "KWD": "د.ك", "BHD": "د.ب", "OMR": "ر.ع"}
            sym = symbols.get(curr, curr)
            return f"{formatted} {sym}"

        return VATResult(
            amount=amount_dec,
            vat_rate=vat_rate,
            vat_percentage=f"{int(vat_rate * 100)}%",
            vat_amount=vat_amount,
            total_with_vat=total,
            country=country,
            country_name_ar=country_names.get("ar", ""),
            country_name_en=country_names.get("en", ""),
            currency=currency,
            formatted_amount=_fmt(amount_dec, currency),
            formatted_vat=_fmt(vat_amount, currency),
            formatted_total=_fmt(total, currency),
        )

    async def generate_invoice(
        self,
        amount: float,
        country: str,
        customer: dict[str, Any],
        description: str = "خدمات استشارية",
        description_en: str = "Consulting Services",
    ) -> Invoice:
        """Generate a simple invoice for a given amount and country.

        Args:
            amount: Invoice amount (pre-VAT).
            country: ISO country code.
            customer: Customer info dict with name, vat, etc.
            description: Arabic description.
            description_en: English description.

        Returns:
            Invoice with calculated VAT.
        """
        country = country.upper().strip()
        vat_rate = VAT_RATES.get(country, Decimal("0.0"))
        currency = COUNTRY_CURRENCIES.get(country, "SAR")

        line = InvoiceLine(
            description=description_en,
            description_ar=description,
            quantity=Decimal("1"),
            unit_price=Decimal(str(amount)),
            vat_rate=vat_rate,
        )

        return Invoice(
            invoice_number=f"INV-{country}-{id(self)}",
            customer_name=customer.get("name", ""),
            customer_vat=customer.get("vat_number"),
            country=country,
            currency=currency,
            lines=[line],
        )

    @staticmethod
    def get_vat_rate(country: str) -> Decimal:
        """Get the current VAT rate for a GCC country.

        Args:
            country: ISO country code.

        Returns:
            VAT rate as Decimal (e.g., Decimal('0.15')).
        """
        return VAT_RATES.get(country.upper().strip(), Decimal("0.0"))

    @staticmethod
    def get_vat_percentage(country: str) -> str:
        """Get VAT rate as a percentage string.

        Args:
            country: ISO country code.

        Returns:
            Percentage string (e.g., "15%").
        """
        rate = VAT_RATES.get(country.upper().strip(), Decimal("0.0"))
        return f"{int(rate * 100)}%"

    @staticmethod
    def get_country_vat_info(country: str) -> dict[str, Any]:
        """Get comprehensive VAT info for a country.

        Args:
            country: ISO country code.

        Returns:
            Dictionary with VAT rate, names, and currency.
        """
        country = country.upper().strip()
        return {
            "country": country,
            "name_ar": COUNTRY_NAMES.get(country, {}).get("ar", ""),
            "name_en": COUNTRY_NAMES.get(country, {}).get("en", ""),
            "vat_rate": str(VAT_RATES.get(country, Decimal("0.0"))),
            "vat_percentage": f"{int(VAT_RATES.get(country, Decimal('0.0')) * 100)}%",
            "currency": COUNTRY_CURRENCIES.get(country, "SAR"),
        }


__all__ = [
    "COUNTRY_CURRENCIES",
    "COUNTRY_NAMES",
    "Invoice",
    "InvoiceLine",
    "VATResult",
    "VATEngine",
    "VAT_RATES",
]
