"""Ministry of Commerce (MC) integration — CR validation and company info.

وزارة التجارة — التحقق من السجلات التجارية والاستعلام عن المنشآت.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any

import httpx


class CROrganizationType(str, Enum):
    SOLE_ESTABLISHMENT = "sole_establishment"
    LIMITED_LIABILITY = "limited_liability"
    CLOSED_JOINT_STOCK = "closed_joint_stock"
    PUBLIC_JOINT_STOCK = "public_joint_stock"
    FOREIGN_COMPANY = "foreign_company"
    PARTNERSHIP = "partnership"
    HOLDING = "holding"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    UNKNOWN = "unknown"


@dataclass
class CRValidation:
    """Commercial Registration validation result."""

    cr_number: str
    is_valid: bool
    status: str
    expires_at: str | None = None
    organization_name_ar: str | None = None
    organization_name_en: str | None = None
    organization_type: CROrganizationType = CROrganizationType.UNKNOWN
    city: str | None = None
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None

    def is_active(self) -> bool:
        return self.is_valid and self.status.lower() in ("active", "نشط", "ساري")

    def is_expired(self) -> bool:
        if not self.is_valid or not self.expires_at:
            return True
        try:
            expiry = date.fromisoformat(self.expires_at)
            return date.today() > expiry
        except (ValueError, TypeError):
            return False


@dataclass
class CompanyInfo:
    """Comprehensive company information from MC."""
    cr_number: str
    name_ar: str
    name_en: str
    organization_type: CROrganizationType
    status: str
    city: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    capital: float | None = None
    activities: list[str] = field(default_factory=list)
    owners: list[dict[str, Any]] = field(default_factory=list)
    directors: list[dict[str, Any]] = field(default_factory=list)
    branches: list[str] = field(default_factory=list)
    vat_number: str | None = None
    raw_response: dict[str, Any] | None = None


class MCClient:
    """Ministry of Commerce API client for CR validation and company info.

    Base URL: https://api.mc.gov.sa/v1
    Requires a valid API key from the MC developer portal.

    Production: https://api.mc.gov.sa/v1
    Sandbox: https://sandbox.api.mc.gov.sa/v1
    """

    BASE_URL = "https://api.mc.gov.sa/v1"
    SANDBOX_URL = "https://sandbox.api.mc.gov.sa/v1"

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

    async def validate_cr(self, cr_number: str) -> CRValidation:
        """Validate a Saudi Commercial Registration number.

        Args:
            cr_number: 10-digit CR number (e.g., 4030234567).

        Returns:
            CRValidation with status and company details.
        """
        cr_number = cr_number.strip()
        if not cr_number.isdigit() or len(cr_number) != 10:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                status="invalid_format",
                errors=["رقم السجل التجاري يجب أن يكون ١٠ أرقام"],
            )

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/commercial-registrations/{cr_number}",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return CRValidation(
                        cr_number=cr_number,
                        is_valid=False,
                        status="api_error",
                        errors=[f"HTTP {resp.status_code}: {resp.text[:200]}"],
                    )
                data = resp.json()
        except httpx.TimeoutException:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                status="timeout",
                errors=["انتهت مهلة الاتصال بخدمة وزارة التجارة"],
            )
        except Exception as exc:
            return CRValidation(
                cr_number=cr_number,
                is_valid=False,
                status="error",
                errors=[str(exc)],
            )

        # Parse response
        record = data.get("record", data)
        status = record.get("status", "")
        is_valid = status.lower() in ("active", "نشط", "ساري")

        org_type_str = record.get("organizationType", "").lower()
        try:
            org_type = CROrganizationType(org_type_str)
        except ValueError:
            org_type = CROrganizationType.UNKNOWN

        return CRValidation(
            cr_number=cr_number,
            is_valid=is_valid,
            status=record.get("status", "unknown"),
            expires_at=record.get("expiryDate"),
            organization_name_ar=record.get("nameAr"),
            organization_name_en=record.get("nameEn"),
            organization_type=org_type,
            city=record.get("city"),
            raw_response=data,
        )

    async def get_company_info(self, cr_number: str) -> CompanyInfo:
        """Get comprehensive company information by CR number.

        Args:
            cr_number: 10-digit CR number.

        Returns:
            CompanyInfo with all available details.
        """
        cr_number = cr_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/commercial-registrations/{cr_number}/details",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return CompanyInfo(
                        cr_number=cr_number,
                        name_ar="",
                        name_en="",
                        organization_type=CROrganizationType.UNKNOWN,
                        status="error",
                        city="",
                    )
                data = resp.json()
        except (httpx.TimeoutException, Exception) as exc:
            return CompanyInfo(
                cr_number=cr_number,
                name_ar="",
                name_en="",
                organization_type=CROrganizationType.UNKNOWN,
                status="error",
                city="",
            )

        record = data.get("record", data)
        org_type_str = record.get("organizationType", "").lower()
        try:
            org_type = CROrganizationType(org_type_str)
        except ValueError:
            org_type = CROrganizationType.UNKNOWN

        return CompanyInfo(
            cr_number=cr_number,
            name_ar=record.get("nameAr", ""),
            name_en=record.get("nameEn", ""),
            organization_type=org_type,
            status=record.get("status", "unknown"),
            city=record.get("city", ""),
            address=record.get("address"),
            phone=record.get("phone"),
            email=record.get("email"),
            capital=record.get("capital"),
            activities=record.get("activities", []),
            owners=record.get("owners", []),
            directors=record.get("directors", []),
            branches=record.get("branches", []),
            vat_number=record.get("vatNumber"),
            raw_response=data,
        )

    async def search_by_name(self, name: str) -> list[CompanyInfo]:
        """Search for companies by name.

        Args:
            name: Company name (Arabic or English) to search for.

        Returns:
            List of matching CompanyInfo records.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/commercial-registrations/search",
                    headers=self._headers(),
                    params={"name": name, "limit": 20},
                )
                if resp.is_error:
                    return []
                data = resp.json()
        except Exception:
            return []

        records = data.get("records", data if isinstance(data, list) else [])
        results: list[CompanyInfo] = []
        for record in records:
            org_type_str = record.get("organizationType", "").lower()
            try:
                org_type = CROrganizationType(org_type_str)
            except ValueError:
                org_type = CROrganizationType.UNKNOWN
            results.append(CompanyInfo(
                cr_number=record.get("crNumber", ""),
                name_ar=record.get("nameAr", ""),
                name_en=record.get("nameEn", ""),
                organization_type=org_type,
                status=record.get("status", "unknown"),
                city=record.get("city", ""),
            ))
        return results

    @staticmethod
    def format_cr(cr_number: str) -> str:
        """Format a CR number with standard formatting.

        For display: XXXX-XXXX-XX
        """
        clean = cr_number.strip()
        if len(clean) != 10 or not clean.isdigit():
            return cr_number
        return f"{clean[:4]}-{clean[4:8]}-{clean[8:]}"

    @staticmethod
    def validate_cr_format(cr_number: str) -> bool:
        """Validate the format of a CR number.

        Saudi CR: 10 digits, first 2 = city code, last = check digit.
        """
        clean = cr_number.strip()
        if not clean.isdigit() or len(clean) != 10:
            return False
        city_code = int(clean[:2])
        return 1 <= city_code <= 99


__all__ = [
    "CRValidation",
    "CROrganizationType",
    "CompanyInfo",
    "MCClient",
]
