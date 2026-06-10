"""UAE localization layer — licensing, VAT, free zones, and regulations.

الإمارات العربية المتحدة — التوطين والتكامل التنظيمي.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

VAT_PERCENTAGE = 0.05  # 5% VAT (standard rate in UAE)

REGULATORS: dict[str, str] = {
    "tdra": "هيئة تنظيم الاتصالات والحكومة الرقمية",
    "tdra_en": "Telecommunications and Digital Government Regulatory Authority",
    "moec": "وزارة الاقتصاد",
    "moec_en": "Ministry of Economy",
    "dib": "دائرة التنمية الاقتصادية - دبي",
    "dib_en": "Dubai Economic Development Department",
    "add": "دائرة التنمية الاقتصادية - أبوظبي",
    "add_en": "Abu Dhabi Economic Development Department",
    "federal_tax": "الهيئة الاتحادية للضرائب",
    "federal_tax_en": "Federal Tax Authority",
    "sca": "هيئة الأوراق المالية والسلع",
    "sca_en": "Securities and Commodities Authority",
    "central_bank": "مصرف الإمارات العربية المتحدة المركزي",
    "central_bank_en": "Central Bank of the UAE",
}

FREE_ZONES: list[str] = [
    "DIFC", "ADGM", "DMCC", "JAFZA", "DSO",
    "MASDAR", "SHAMS", "RAK FTZ", "AJMAN FTZ",
    "FUJAIRAH FTZ", "UMM AL QUWAIN FTZ", "KEZAD",
    "TECOM", "MBR CITY", "DUBAI SOUTH", "ABU DHABI AIRPORT FTZ",
]

EMIRATES: dict[str, dict[str, str]] = {
    "dxb": {"name_ar": "إمارة دبي", "name_en": "Dubai", "code": "DXB"},
    "auh": {"name_ar": "إمارة أبوظبي", "name_en": "Abu Dhabi", "code": "AUH"},
    "shj": {"name_ar": "إمارة الشارقة", "name_en": "Sharjah", "code": "SHJ"},
    "ajm": {"name_ar": "إمارة عجمان", "name_en": "Ajman", "code": "AJM"},
    "rak": {"name_ar": "إمارة رأس الخيمة", "name_en": "Ras Al Khaimah", "code": "RAK"},
    "fuq": {"name_ar": "إمارة الفجيرة", "name_en": "Fujairah", "code": "FUQ"},
    "uaq": {"name_ar": "إمارة أم القيوين", "name_en": "Umm Al Quwain", "code": "UAQ"},
}


@dataclass
class LicenseValidation:
    """UAE business license validation result."""
    license_number: str
    is_valid: bool
    emirate: str = ""
    license_type: str = ""
    company_name: str = ""
    status: str = ""
    expiry_date: str = ""
    free_zone: str | None = None
    activity: str = ""
    errors: list[str] = field(default_factory=list)


class UAELayer:
    """UAE localization and business integration layer."""

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
        """Validate a UAE business license.

        Args:
            license_number: UAE license number from DED or free zone.

        Returns:
            LicenseValidation with status.
        """
        license_number = license_number.strip()
        if not self._api_key:
            return LicenseValidation(
                license_number=license_number,
                is_valid=False,
                errors=["UAE API key not configured"],
            )

        base = "https://sandbox.api.uae.gov.ae" if self._sandbox else "https://api.uae.gov.ae"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{base}/business-licenses/{license_number}",
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
            emirate=record.get("emirate", ""),
            license_type=record.get("licenseType", ""),
            company_name=record.get("companyName", ""),
            status=record.get("status", ""),
            expiry_date=record.get("expiryDate", ""),
            free_zone=record.get("freeZone"),
            activity=record.get("activity", ""),
        )

    @staticmethod
    def is_free_zone_entity(license_number: str) -> bool:
        """Check if a license belongs to a free zone entity."""
        # Free zone licenses often have specific prefixes
        fz_prefixes = ["DIFC", "ADGM", "DMCC", "JAFZA"]
        return any(license_number.upper().startswith(p) for p in fz_prefixes)

    @staticmethod
    def get_federal_tax_registration_format(trn: str) -> str:
        """Format a UAE Tax Registration Number (TRN).

        Format: 15 digits
        """
        clean = trn.strip()
        if clean.isdigit() and len(clean) == 15:
            return clean
        return clean

    @staticmethod
    def is_valid_trn(trn: str) -> bool:
        """Validate a UAE Tax Registration Number format.

        TRN: 15 digits, starts with 3.
        """
        clean = trn.strip()
        return clean.isdigit() and len(clean) == 15 and clean.startswith("3")


__all__ = [
    "EMIRATES",
    "FREE_ZONES",
    "LICENSE_VALIDATION_URL",
    "REGULATORS",
    "UAELayer",
    "VAT_PERCENTAGE",
]
