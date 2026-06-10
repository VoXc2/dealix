"""Oman localization layer — licensing, VAT, and regulations.

سلطنة عمان — التوطين والتكامل التنظيمي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

VAT_PERCENTAGE = 0.0  # 0% (currently 0%, 5% being discussed)

REGULATORS: dict[str, str] = {
    "moci": "وزارة التجارة والصناعة",
    "moci_en": "Ministry of Commerce and Industry",
    "cbo": "البنك المركزي العماني",
    "cbo_en": "Central Bank of Oman",
    "tra": "هيئة تنظيم الاتصالات",
    "tra_en": "Telecommunications Regulatory Authority",
    "tax": "الهيئة العامة للضرائب",
    "tax_en": "Tax Authority",
    "cma": "هيئة الخدمات المالية",
    "cma_en": "Capital Market Authority",
}

FREE_ZONES: list[str] = ["SEZAD", "OMAN FREE ZONE", "SOHAR FTZ", "AL MAZONAH", "RUSAYL"]


@dataclass
class CRValidation:
    """Oman Commercial Registration validation result."""
    cr_number: str
    is_valid: bool
    company_name_ar: str = ""
    company_name_en: str = ""
    status: str = ""
    cr_type: str = ""
    expiry_date: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


class OmanLayer:
    """Oman localization and business integration layer."""

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
        """Validate an Oman Commercial Registration via MOCI.

        Args:
            cr_number: Oman CR number.

        Returns:
            CRValidation with status.
        """
        cr_number = cr_number.strip()
        if not self._api_key:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                errors=["Oman API key not configured"],
            )

        base = "https://sandbox.api.oman.om" if self._sandbox else "https://api.oman.om"
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


__all__ = ["CRValidation", "OmanLayer", "REGULATORS", "VAT_PERCENTAGE"]
