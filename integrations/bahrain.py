"""Bahrain localization layer — licensing, VAT, and regulations.

مملكة البحرين — التوطين والتكامل التنظيمي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

VAT_PERCENTAGE = 0.0  # 0% (standard rate 0%, 10% on some services)

REGULATORS: dict[str, str] = {
    "moict": "وزارة الصناعة والتجارة",
    "moict_en": "Ministry of Industry and Commerce",
    "cbb": "مصرف البحرين المركزي",
    "cbb_en": "Central Bank of Bahrain",
    "tra": "هيئة تنظيم الاتصالات",
    "tra_en": "Telecommunications Regulatory Authority",
    "nbr": "الهيئة العامة للضرائب",
    "nbr_en": "National Bureau for Revenue",
    "edb": "مجلس التنمية الاقتصادية",
    "edb_en": "Economic Development Board",
}

FREE_ZONES: list[str] = [
    "BHIFZ", "BIBF", "BAHRAIN FINANCIAL HARBOUR",
    "BAHRAIN INVESTMENT WHARF",
]


@dataclass
class CRValidation:
    """Bahrain Commercial Registration validation result."""
    cr_number: str
    is_valid: bool
    company_name_ar: str = ""
    company_name_en: str = ""
    status: str = ""
    cr_type: str = ""
    expiry_date: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


class BahrainLayer:
    """Bahrain localization and business integration layer."""

    VAT_PERCENTAGE = VAT_PERCENTAGE

    def __init__(
        self,
        api_key: str | None = None,
        sandbox: bool = True,
        timeout: float = 15.0,
    ) -> None:
        self._api_key = api_key
        self._sandbox = sandbox
        self._timeout = timeout

    async def validate_cr(self, cr_number: str) -> CRValidation:
        """Validate a Bahrain Commercial Registration via MOICT.

        Args:
            cr_number: Bahrain CR number.

        Returns:
            CRValidation with status.
        """
        cr_number = cr_number.strip()
        if not self._api_key:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                errors=["Bahrain API key not configured"],
            )

        base = "https://sandbox.api.bahrain.bh" if self._sandbox else "https://api.bahrain.bh"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{base}/commercial-registrations/{cr_number}",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Accept": "application/json",
                    },
                )
                if resp.is_error:
                    return CRValidation(
                        cr_number=cr_number,
                        is_valid=False,
                        errors=[f"HTTP {resp.status_code}"],
                    )
                data = resp.json()
        except Exception as exc:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        return CRValidation(
            cr_number=cr_number,
            is_valid=record.get("isValid", False),
            company_name_ar=record.get("nameAr", ""),
            company_name_en=record.get("nameEn", ""),
            status=record.get("status", ""),
            cr_type=record.get("type", ""),
            expiry_date=record.get("expiryDate", ""),
            raw_response=data,
        )


__all__ = ["BahrainLayer", "CRValidation", "REGULATORS", "VAT_PERCENTAGE"]
