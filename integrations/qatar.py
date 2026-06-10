"""Qatar localization layer — licensing, VAT, and regulations.

دولة قطر — التوطين والتكامل التنظيمي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

VAT_PERCENTAGE = 0.0  # 0% (no VAT currently in Qatar)

REGULATORS: dict[str, str] = {
    "qfc": "مركز قطر للمال",
    "qfc_en": "Qatar Financial Centre",
    "cra": "هيئة تنظيم الاتصالات",
    "cra_en": "Communications Regulatory Authority",
    "moci": "وزارة التجارة والصناعة",
    "moci_en": "Ministry of Commerce and Industry",
    "qcb": "مصرف قطر المركزي",
    "qcb_en": "Qatar Central Bank",
    "qfma": "هيئة قطر للأسواق المالية",
    "qfma_en": "Qatar Financial Markets Authority",
}

FREE_ZONES: list[str] = ["QFC", "QSTP", "RFZC", "UM ALHOU", "RAS BUFONTAS"]


@dataclass
class CRValidation:
    """Qatar Commercial Registration validation result."""
    cr_number: str
    is_valid: bool
    company_name_ar: str = ""
    company_name_en: str = ""
    status: str = ""
    cr_type: str = ""
    expiry_date: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


class QatarLayer:
    """Qatar localization and business integration layer."""

    VAT_PERCENTAGE = VAT_PERCENTAGE
    REGULATORS = list(REGULATORS.keys())

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
        """Validate a Qatar Commercial Registration number.

        Args:
            cr_number: Qatar CR number.

        Returns:
            CRValidation with status.
        """
        cr_number = cr_number.strip()
        if not self._api_key:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                errors=["Qatar API key not configured"],
            )

        base = "https://sandbox.api.qatar.gov.qa" if self._sandbox else "https://api.qatar.gov.qa"
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


__all__ = ["CRValidation", "QatarLayer", "REGULATORS", "VAT_PERCENTAGE"]
