"""Kuwait localization layer — licensing, VAT, and regulations.

دولة الكويت — التوطين والتكامل التنظيمي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

VAT_PERCENTAGE = 0.0  # 0% (no VAT currently in Kuwait)

REGULATORS: dict[str, str] = {
    "moci": "وزارة التجارة والصناعة",
    "moci_en": "Ministry of Commerce and Industry",
    "cbk": "بنك الكويت المركزي",
    "cbk_en": "Central Bank of Kuwait",
    "cma": "هيئة أسواق المال",
    "cma_en": "Capital Markets Authority",
    "citra": "الهيئة العامة للاتصالات",
    "citra_en": "Communications and IT Regulatory Authority",
    "pai": "الهيئة العامة للاستثمار",
    "pai_en": "Public Authority for Investment",
}

FREE_ZONES: list[str] = ["KFZ", "KAZ"]


@dataclass
class LicenseValidation:
    """Kuwait business license validation result."""
    license_number: str
    is_valid: bool
    company_name_ar: str = ""
    company_name_en: str = ""
    license_type: str = ""
    status: str = ""
    expiry_date: str = ""
    activity: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


class KuwaitLayer:
    """Kuwait localization and business integration layer."""

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

    async def validate_license(self, license_number: str) -> LicenseValidation:
        """Validate a Kuwait business license via MOCI.

        Args:
            license_number: Kuwait MOCI license number.

        Returns:
            LicenseValidation with status.
        """
        license_number = license_number.strip()
        if not self._api_key:
            return LicenseValidation(
                license_number=license_number,
                is_valid=False,
                errors=["Kuwait API key not configured"],
            )

        base = "https://sandbox.api.kuwait.gov.kw" if self._sandbox else "https://api.kuwait.gov.kw"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{base}/licenses/{license_number}",
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Accept": "application/json",
                    },
                )
                if resp.is_error:
                    return LicenseValidation(
                        license_number=license_number,
                        is_valid=False,
                        errors=[f"HTTP {resp.status_code}"],
                    )
                data = resp.json()
        except Exception as exc:
            return LicenseValidation(
                license_number=license_number,
                is_valid=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        return LicenseValidation(
            license_number=license_number,
            is_valid=record.get("isValid", False),
            company_name_ar=record.get("nameAr", ""),
            company_name_en=record.get("nameEn", ""),
            license_type=record.get("licenseType", ""),
            status=record.get("status", ""),
            expiry_date=record.get("expiryDate", ""),
            activity=record.get("activity", ""),
            raw_response=data,
        )


__all__ = ["KuwaitLayer", "LicenseValidation", "REGULATORS", "VAT_PERCENTAGE"]
