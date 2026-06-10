"""Qiwa (Ministry of Labor) integration — Nitaqat and Saudization checks.

وزارة الموارد البشرية والتنمية الاجتماعية عبر منصة قوى.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class NitaqatStatus:
    """Nitaqat (nationalization) status for a company."""
    cr_number: str
    nitaqat_level: str
    nitaqat_level_ar: str
    description: str = ""
    total_employees: int = 0
    saudi_employees: int = 0
    non_saudi_employees: int = 0
    saudization_rate: float = 0.0
    is_compliant: bool = False
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None

    NITAQAT_LEVELS: dict[str, tuple[str, bool]] = {
        "platinum": ("بلاتيني", True),
        "green": ("أخضر", True),
        "green_low": ("أخضر منخفض", True),
        "yellow": ("أصفر", False),
        "red": ("أحمر", False),
        "red_high": ("أحمر عالي", False),
    }

    def __post_init__(self) -> None:
        level_info = self.NITAQAT_LEVELS.get(self.nitaqat_level.lower(), ("", False))
        if not self.nitaqat_level_ar:
            self.nitaqat_level_ar = level_info[0]
        self.is_compliant = level_info[1]


@dataclass
class SaudizationRate:
    """Saudization (Saudi Nationalization) rate details."""
    cr_number: str
    total_positions: int = 0
    saudi_positions: int = 0
    saudization_rate: float = 0.0
    target_rate: float = 0.0
    gap: int = 0
    sector: str = ""
    errors: list[str] = field(default_factory=list)

    def meets_target(self) -> bool:
        return self.saudization_rate >= self.target_rate


@dataclass
class EmployeeRecord:
    """Individual employee record from Qiwa."""
    employee_id: str
    name: str
    nationality: str
    is_saudi: bool
    job_title: str
    contract_type: str
    wage: float
    insurance_status: str


class QiwaClient:
    """Qiwa (Ministry of Labor) API client.

    Base URL: https://api.qiwa.sa/v1
    Requires a valid API key from Qiwa developer portal.

    Production: https://api.qiwa.sa/v1
    Sandbox: https://sandbox.api.qiwa.sa/v1
    """

    BASE_URL = "https://api.qiwa.sa/v1"
    SANDBOX_URL = "https://sandbox.api.qiwa.sa/v1"

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

    async def check_nitaqat(self, cr_number: str) -> NitaqatStatus:
        """Check the Nitaqat level for a company.

        Args:
            cr_number: 10-digit CR number.

        Returns:
            NitaqatStatus with level and compliance info.
        """
        cr_number = cr_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/establishments/{cr_number}/nitaqat",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return NitaqatStatus(
                        cr_number=cr_number,
                        nitaqat_level="unknown",
                        errors=[f"HTTP {resp.status_code}"],
                    )
                data = resp.json()
        except (httpx.TimeoutException, Exception) as exc:
            return NitaqatStatus(
                cr_number=cr_number,
                nitaqat_level="unknown",
                errors=[str(exc)],
            )

        record = data.get("record", data)
        return NitaqatStatus(
            cr_number=cr_number,
            nitaqat_level=record.get("nitaqatLevel", "unknown"),
            description=record.get("description", ""),
            total_employees=record.get("totalEmployees", 0),
            saudi_employees=record.get("saudiEmployees", 0),
            non_saudi_employees=record.get("nonSaudiEmployees", 0),
            saudization_rate=float(record.get("saudizationRate", 0)),
            raw_response=data,
        )

    async def check_saudization(self, cr_number: str) -> SaudizationRate:
        """Check Saudization rate for a company.

        Args:
            cr_number: 10-digit CR number.

        Returns:
            SaudizationRate with detailed breakdown.
        """
        cr_number = cr_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/establishments/{cr_number}/saudization",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return SaudizationRate(
                        cr_number=cr_number,
                        errors=[f"HTTP {resp.status_code}"],
                    )
                data = resp.json()
        except (httpx.TimeoutException, Exception) as exc:
            return SaudizationRate(
                cr_number=cr_number,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        total = record.get("totalPositions", 0)
        saudi = record.get("saudiPositions", 0)
        rate = float(record.get("saudizationRate", 0))
        target = float(record.get("targetRate", 0))

        return SaudizationRate(
            cr_number=cr_number,
            total_positions=total,
            saudi_positions=saudi,
            saudization_rate=rate,
            target_rate=target,
            gap=max(0, int((target / 100 * total) - saudi)),
            sector=record.get("sector", ""),
        )

    async def list_employees(
        self,
        cr_number: str,
        page: int = 1,
        per_page: int = 50,
    ) -> list[EmployeeRecord]:
        """List employees registered with Qiwa for a CR.

        Args:
            cr_number: 10-digit CR number.
            page: Page number.
            per_page: Results per page.

        Returns:
            List of EmployeeRecord.
        """
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/establishments/{cr_number}/employees",
                    headers=self._headers(),
                    params={"page": page, "perPage": per_page},
                )
                if resp.is_error:
                    return []
                data = resp.json()
        except Exception:
            return []

        records = data.get("records", data if isinstance(data, list) else [])
        return [
            EmployeeRecord(
                employee_id=r.get("employeeId", ""),
                name=r.get("name", ""),
                nationality=r.get("nationality", ""),
                is_saudi=r.get("isSaudi", False),
                job_title=r.get("jobTitle", ""),
                contract_type=r.get("contractType", ""),
                wage=float(r.get("wage", 0)),
                insurance_status=r.get("insuranceStatus", ""),
            )
            for r in records
        ]

    @staticmethod
    def nitaqat_color(nitaqat_level: str) -> str:
        """Return the color associated with a Nitaqat level."""
        colors = {
            "platinum": "#E5E4E2",
            "green": "#28A745",
            "green_low": "#5CB85C",
            "yellow": "#FFC107",
            "red": "#DC3545",
            "red_high": "#8B0000",
        }
        return colors.get(nitaqat_level.lower(), "#6C757D")


__all__ = [
    "EmployeeRecord",
    "NitaqatStatus",
    "QiwaClient",
    "SaudizationRate",
]
