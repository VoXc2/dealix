"""GOSI (General Organization for Social Insurance) integration.

المؤسسة العامة للتأمينات الاجتماعية — التحقق من اشتراك المنشآت.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class EmployerStatus:
    """GOSI employer subscription status."""
    gosi_number: str
    is_registered: bool
    is_active: bool = False
    status: str = ""
    status_ar: str = ""
    company_name: str = ""
    subscription_date: str = ""
    total_employees: int = 0
    total_saudi_employees: int = 0
    total_non_saudi_employees: int = 0
    subscription_type: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None


@dataclass
class ContributionRecord:
    """A single GOSI contribution record."""
    month: str
    year: int
    total_wages: float
    contribution_amount: float
    employee_count: int
    is_paid: bool
    payment_date: str | None = None


class GOSIClient:
    """GOSI API client — employer verification and contribution lookup.

    Production: https://api.gosi.gov.sa/v1
    Sandbox: https://sandbox.api.gosi.gov.sa/v1
    """

    BASE_URL = "https://api.gosi.gov.sa/v1"
    SANDBOX_URL = "https://sandbox.api.gosi.gov.sa/v1"

    STATUS_MAP_AR: dict[str, str] = {
        "active": "نشط",
        "suspended": "موقوف",
        "cancelled": "ملغي",
        "pending": "قيد التفعيل",
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
        }

    async def verify_employer(self, gosi_number: str) -> EmployerStatus:
        """Verify GOSI employer registration and status.

        Args:
            gosi_number: GOSI employer registration number.

        Returns:
            EmployerStatus with registration and activity info.
        """
        gosi_number = gosi_number.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/employers/{gosi_number}",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return EmployerStatus(
                        gosi_number=gosi_number,
                        is_registered=False,
                        errors=[f"HTTP {resp.status_code}: {resp.text[:200]}"],
                    )
                data = resp.json()
        except httpx.TimeoutException:
            return EmployerStatus(
                gosi_number=gosi_number,
                is_registered=False,
                errors=["انتهت مهلة الاتصال بالتأمينات الاجتماعية"],
            )
        except Exception as exc:
            return EmployerStatus(
                gosi_number=gosi_number,
                is_registered=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        status = record.get("status", "")
        is_active = status.lower() in ("active", "نشط")

        return EmployerStatus(
            gosi_number=gosi_number,
            is_registered=True,
            is_active=is_active,
            status=status,
            status_ar=self.STATUS_MAP_AR.get(status.lower(), status),
            company_name=record.get("companyName", ""),
            subscription_date=record.get("subscriptionDate", ""),
            total_employees=int(record.get("totalEmployees", 0)),
            total_saudi_employees=int(record.get("saudiEmployees", 0)),
            total_non_saudi_employees=int(record.get("nonSaudiEmployees", 0)),
            subscription_type=record.get("subscriptionType", ""),
            raw_response=data,
        )

    async def get_contribution_history(
        self,
        gosi_number: str,
        year: int | None = None,
    ) -> list[ContributionRecord]:
        """Get contribution history for an employer.

        Args:
            gosi_number: GOSI employer number.
            year: Filter by year.

        Returns:
            List of ContributionRecord.
        """
        params: dict[str, Any] = {}
        if year:
            params["year"] = year

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/employers/{gosi_number}/contributions",
                    headers=self._headers(),
                    params=params,
                )
                if resp.is_error:
                    return []
                data = resp.json()
        except Exception:
            return []

        records = data.get("records", data if isinstance(data, list) else [])
        return [
            ContributionRecord(
                month=r.get("month", ""),
                year=int(r.get("year", 0)),
                total_wages=float(r.get("totalWages", 0)),
                contribution_amount=float(r.get("contributionAmount", 0)),
                employee_count=int(r.get("employeeCount", 0)),
                is_paid=r.get("isPaid", False),
                payment_date=r.get("paymentDate"),
            )
            for r in records
        ]


__all__ = ["ContributionRecord", "EmployerStatus", "GOSIClient"]
