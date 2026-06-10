"""Saudi Post (SPL) address validation — national address verification.

البريد السعودي — التحقق من العنوان الوطني.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class AddressValidation:
    """Saudi National Address validation result."""
    address: str
    is_valid: bool
    building_number: str = ""
    street: str = ""
    district: str = ""
    city: str = ""
    region: str = ""
    postal_code: str = ""
    additional_number: str = ""
    unit_number: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


@dataclass
class BuildingInfo:
    """Detailed building information from Saudi Post."""
    building_number: str
    postal_code: str
    additional_number: str
    street_name_ar: str = ""
    street_name_en: str = ""
    district_ar: str = ""
    district_en: str = ""
    city_ar: str = ""
    city_en: str = ""
    region_ar: str = ""
    region_en: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    is_valid: bool = False


class SaudiPostClient:
    """Saudi Post (SPL) API client — national address validation.

    Production: https://api.address.gov.sa/v1
    Sandbox: https://sandbox.api.address.gov.sa/v1
    """

    BASE_URL = "https://api.address.gov.sa/v1"
    SANDBOX_URL = "https://sandbox.api.address.gov.sa/v1"

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
            "api_key": self._api_key,
            "Accept": "application/json",
            "Accept-Language": "ar-SA",
        }

    async def validate_address(self, address: str) -> AddressValidation:
        """Validate a Saudi National Address.

        Args:
            address: Full address string or building number.

        Returns:
            AddressValidation with parsed components.
        """
        address = address.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/addresses/validate",
                    headers=self._headers(),
                    params={"address": address},
                )
                if resp.is_error:
                    return AddressValidation(
                        address=address,
                        is_valid=False,
                        errors=[f"HTTP {resp.status_code}: {resp.text[:200]}"],
                    )
                data = resp.json()
        except httpx.TimeoutException:
            return AddressValidation(
                address=address,
                is_valid=False,
                errors=["انتهت مهلة الاتصال بخدمة العنوان الوطني"],
            )
        except Exception as exc:
            return AddressValidation(
                address=address,
                is_valid=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        is_valid = record.get("isValid", False)

        return AddressValidation(
            address=address,
            is_valid=is_valid,
            building_number=record.get("buildingNumber", ""),
            street=record.get("street", ""),
            district=record.get("district", ""),
            city=record.get("city", ""),
            region=record.get("region", ""),
            postal_code=record.get("postalCode", ""),
            additional_number=record.get("additionalNumber", ""),
            unit_number=record.get("unitNumber", ""),
            latitude=float(record.get("latitude", 0)),
            longitude=float(record.get("longitude", 0)),
            raw_response=data,
        )

    async def get_building_info(self, building_number: str) -> BuildingInfo:
        """Get detailed info for a specific building number.

        Args:
            building_number: Saudi building number (4-5 digits).

        Returns:
            BuildingInfo with full address details.
        """
        building_number = building_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/buildings/{building_number}",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return BuildingInfo(
                        building_number=building_number,
                        postal_code="",
                        additional_number="",
                        is_valid=False,
                    )
                data = resp.json()
        except Exception as exc:
            return BuildingInfo(
                building_number=building_number,
                postal_code="",
                additional_number="",
                is_valid=False,
            )

        record = data.get("record", data)
        return BuildingInfo(
            building_number=building_number,
            postal_code=record.get("postalCode", ""),
            additional_number=record.get("additionalNumber", ""),
            street_name_ar=record.get("streetNameAr", ""),
            street_name_en=record.get("streetNameEn", ""),
            district_ar=record.get("districtAr", ""),
            district_en=record.get("districtEn", ""),
            city_ar=record.get("cityAr", ""),
            city_en=record.get("cityEn", ""),
            region_ar=record.get("regionAr", ""),
            region_en=record.get("regionEn", ""),
            latitude=float(record.get("latitude", 0)),
            longitude=float(record.get("longitude", 0)),
            is_valid=True,
        )

    async def search_address(
        self,
        keyword: str,
        limit: int = 10,
    ) -> list[AddressValidation]:
        """Search for addresses by keyword.

        Args:
            keyword: Arabic or English address keyword.
            limit: Max results.

        Returns:
            List of matching AddressValidation records.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/addresses/search",
                    headers=self._headers(),
                    params={"keyword": keyword, "limit": limit},
                )
                if resp.is_error:
                    return []
                data = resp.json()
        except Exception:
            return []

        records = data.get("records", data if isinstance(data, list) else [])
        results: list[AddressValidation] = []
        for r in records:
            results.append(AddressValidation(
                address="",
                is_valid=True,
                building_number=r.get("buildingNumber", ""),
                street=r.get("street", ""),
                district=r.get("district", ""),
                city=r.get("city", ""),
                region=r.get("region", ""),
                postal_code=r.get("postalCode", ""),
                additional_number=r.get("additionalNumber", ""),
            ))
        return results

    @staticmethod
    def format_national_address(
        building_number: str,
        street: str,
        district: str,
        city: str,
        postal_code: str,
        additional_number: str = "",
    ) -> str:
        """Format a Saudi National Address in standard format.

        Format: Building Number | Street | District | City | Postal Code
        """
        parts = [building_number, street, district, city, postal_code]
        if additional_number:
            parts.append(additional_number)
        return " | ".join(parts)


__all__ = [
    "AddressValidation",
    "BuildingInfo",
    "SaudiPostClient",
]
