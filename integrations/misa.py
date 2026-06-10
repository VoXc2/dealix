"""Ministry of Investment of Saudi Arabia (MISA) integration.

وزارة الاستثمار السعودية — التحقق من تراخيص الاستثمار الأجنبي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class LicenseValidation:
    """MISA investment license validation result."""
    license_number: str
    is_valid: bool
    license_type: str = ""
    license_type_ar: str = ""
    status: str = ""
    company_name_en: str = ""
    company_name_ar: str = ""
    investor_nationality: str = ""
    sector: str = ""
    issued_date: str = ""
    expiry_date: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None

    def is_active(self) -> bool:
        return self.is_valid and self.status.lower() in ("active", "نشط", "ساري")


class MISAClient:
    """MISA API client — investment license validation.

    Base URL: https://api.misa.gov.sa/v1
    Requires a valid API key from MISA.

    Production: https://api.misa.gov.sa/v1
    Sandbox: https://sandbox.api.misa.gov.sa/v1
    """

    BASE_URL = "https://api.misa.gov.sa/v1"
    SANDBOX_URL = "https://sandbox.api.misa.gov.sa/v1"

    LICENSE_TYPES_AR: dict[str, str] = {
        "new_investment": "ترخيص استثماري جديد",
        "branch": "فرع شركة أجنبية",
        "renewal": "تجديد ترخيص",
        "extension": "توسعة نشاط",
    }

    def __init__(
        self,
        api_key: str,
        sandbox: bool = False,
        timeout: float = 15.0,
    ) -> None:
        self._api_key = api_key
        self._base = self.SANDBOX_URL if sandbox else self.BASE_URL
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "Accept-Language": "ar-SA",
            "Content-Type": "application/json",
        }

    async def validate_license(self, license_number: str) -> LicenseValidation:
        """Validate a MISA investment license.

        Args:
            license_number: MISA license ID.

        Returns:
            LicenseValidation with status and details.
        """
        license_number = license_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/licenses/{license_number}",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return LicenseValidation(
                        license_number=license_number,
                        is_valid=False,
                        errors=[f"HTTP {resp.status_code}: {resp.text[:200]}"],
                    )
                data = resp.json()
        except httpx.TimeoutException:
            return LicenseValidation(
                license_number=license_number,
                is_valid=False,
                errors=["انتهت مهلة الاتصال بخدمة وزارة الاستثمار"],
            )
        except Exception as exc:
            return LicenseValidation(
                license_number=license_number,
                is_valid=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        status = record.get("status", "")
        is_valid = status.lower() in ("active", "نشط", "ساري")

        return LicenseValidation(
            license_number=license_number,
            is_valid=is_valid,
            license_type=record.get("licenseType", ""),
            license_type_ar=self.LICENSE_TYPES_AR.get(
                record.get("licenseType", ""), record.get("licenseType", "")
            ),
            status=record.get("status", ""),
            company_name_en=record.get("companyNameEn", ""),
            company_name_ar=record.get("companyNameAr", ""),
            investor_nationality=record.get("investorNationality", ""),
            sector=record.get("sector", ""),
            issued_date=record.get("issuedDate", ""),
            expiry_date=record.get("expiryDate", ""),
            raw_response=data,
        )

    async def get_license_types(self) -> list[dict[str, str]]:
        """Get available license types from MISA."""
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/licenses/types",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return []
                data = resp.json()
        except Exception:
            return []
        return data.get("types", [])


__all__ = ["LicenseValidation", "MISAClient"]
