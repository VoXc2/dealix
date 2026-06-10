"""Mudad (WPS) integration — Wage Protection System verification.

مُدد — نظام حماية الأجور: التحقق من امتثال المنشآت لصرف الرواتب عبر النظام.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

import httpx


@dataclass
class WPSStatus:
    """Wage Protection System (WPS) status for a company."""
    company_id: str
    is_compliant: bool
    compliance_rate: float = 0.0
    total_employees: int = 0
    paid_employees: int = 0
    unpaid_employees: int = 0
    total_wages: float = 0.0
    paid_wages: float = 0.0
    unpaid_wages: float = 0.0
    last_submission_date: str = ""
    submission_month: str = ""
    status: str = ""
    errors: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None

    def is_wps_ok(self) -> bool:
        return self.is_compliant and self.compliance_rate >= 90.0


@dataclass
class WPSSubmission:
    """A single WPS salary submission record."""
    submission_id: str
    month: str
    year: int
    total_salaries: float
    paid_salaries: float
    employee_count: int
    status: str
    submission_date: str
    bank_name: str | None = None


class MudadClient:
    """Mudad (WPS) API client.

    Mudad manages the Wage Protection System on behalf of the
    Ministry of Human Resources and Social Development (MHRSD).

    Production: https://api.mudad.sa/v1
    Sandbox: https://sandbox.api.mudad.sa/v1
    """

    BASE_URL = "https://api.mudad.sa/v1"
    SANDBOX_URL = "https://sandbox.api.mudad.sa/v1"

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

    async def verify_wps(self, company_id: str) -> WPSStatus:
        """Verify WPS compliance for a company.

        Args:
            company_id: CR number or establishment ID.

        Returns:
            WPSStatus with compliance details.
        """
        company_id = company_id.strip()
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/establishments/{company_id}/wps-status",
                    headers=self._headers(),
                )
                if resp.is_error:
                    return WPSStatus(
                        company_id=company_id,
                        is_compliant=False,
                        errors=[f"HTTP {resp.status_code}: {resp.text[:200]}"],
                    )
                data = resp.json()
        except httpx.TimeoutException:
            return WPSStatus(
                company_id=company_id,
                is_compliant=False,
                errors=["انتهت مهلة الاتصال بنظام مدد"],
            )
        except Exception as exc:
            return WPSStatus(
                company_id=company_id,
                is_compliant=False,
                errors=[str(exc)],
            )

        record = data.get("record", data)
        status = record.get("status", "")
        paid = int(record.get("paidEmployees", 0))
        total = int(record.get("totalEmployees", 0))
        compliance_rate = (paid / total * 100) if total > 0 else 0.0

        return WPSStatus(
            company_id=company_id,
            is_compliant=status.lower() in ("compliant", "متوافق"),
            compliance_rate=compliance_rate,
            total_employees=total,
            paid_employees=paid,
            unpaid_employees=total - paid,
            total_wages=float(record.get("totalWages", 0)),
            paid_wages=float(record.get("paidWages", 0)),
            unpaid_wages=float(record.get("unpaidWages", 0)),
            last_submission_date=record.get("lastSubmissionDate", ""),
            submission_month=record.get("submissionMonth", ""),
            status=record.get("status", "unknown"),
            raw_response=data,
        )

    async def get_submission_history(
        self,
        company_id: str,
        year: int | None = None,
        month: int | None = None,
    ) -> list[WPSSubmission]:
        """Get WPS submission history for a company.

        Args:
            company_id: CR number or establishment ID.
            year: Filter by year.
            month: Filter by month.

        Returns:
            List of WPSSubmission records.
        """
        params: dict[str, Any] = {}
        if year:
            params["year"] = year
        if month:
            params["month"] = month

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(
                    f"{self._base}/establishments/{company_id}/wps-submissions",
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
            WPSSubmission(
                submission_id=r.get("submissionId", ""),
                month=r.get("month", ""),
                year=int(r.get("year", 0)),
                total_salaries=float(r.get("totalSalaries", 0)),
                paid_salaries=float(r.get("paidSalaries", 0)),
                employee_count=int(r.get("employeeCount", 0)),
                status=r.get("status", ""),
                submission_date=r.get("submissionDate", ""),
                bank_name=r.get("bankName"),
            )
            for r in records
        ]


__all__ = ["MudadClient", "WPSStatus", "WPSSubmission"]
