"""Validation Rules — Data OS field-level validators for Saudi B2B records.

قواعد التحقق على مستوى الحقول للسجلات السعودية B2B.

Pure functions; safe to use in batch (pandas apply) or online (per-record).
"""
from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict


_CR_RE = re.compile(r"^\d{10}$")  # Saudi CR is 10 digits
_VAT_RE = re.compile(r"^3\d{14}$")  # ZATCA VAT: 15 digits, starts with 3
_PHONE_SA_RE = re.compile(r"^(?:\+?966|0)?5\d{8}$")
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_DOMAIN_RE = re.compile(r"^(?!-)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")


class FieldIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field: str
    code: str
    message_ar: str
    message_en: str


class ValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    valid: bool
    issues: list[FieldIssue]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def validate_cr(value: str | None) -> FieldIssue | None:
    if value and not _CR_RE.match(value):
        return FieldIssue(
            field="commercial_registration",
            code="cr_format",
            message_ar="السجل التجاري يجب أن يكون 10 أرقام.",
            message_en="Commercial Registration must be 10 digits.",
        )
    return None


def validate_vat(value: str | None) -> FieldIssue | None:
    if value and not _VAT_RE.match(value):
        return FieldIssue(
            field="vat_number",
            code="vat_format",
            message_ar="الرقم الضريبي يجب أن يكون 15 رقمًا ويبدأ بـ 3.",
            message_en="VAT must be 15 digits and start with 3.",
        )
    return None


def validate_phone_sa(value: str | None) -> FieldIssue | None:
    if value and not _PHONE_SA_RE.match(value.replace(" ", "").replace("-", "")):
        return FieldIssue(
            field="phone",
            code="phone_sa_format",
            message_ar="رقم الجوّال يجب أن يكون 9665xxxxxxxx أو 05xxxxxxxx.",
            message_en="Saudi mobile must be +9665xxxxxxxx or 05xxxxxxxx.",
        )
    return None


def validate_email(value: str | None) -> FieldIssue | None:
    if value and not _EMAIL_RE.match(value):
        return FieldIssue(
            field="email",
            code="email_format",
            message_ar="صيغة البريد الإلكتروني غير صحيحة.",
            message_en="Email format invalid.",
        )
    return None


def validate_domain(value: str | None) -> FieldIssue | None:
    if value and not _DOMAIN_RE.match(value):
        return FieldIssue(
            field="domain",
            code="domain_format",
            message_ar="صيغة النطاق غير صحيحة.",
            message_en="Domain format invalid.",
        )
    return None


def validate_record(record: dict[str, Any]) -> ValidationResult:
    """Validate one Saudi B2B record. Returns ValidationResult."""
    issues: list[FieldIssue] = []
    for fn, key in (
        (validate_cr, "commercial_registration"),
        (validate_vat, "vat_number"),
        (validate_phone_sa, "phone"),
        (validate_email, "email"),
        (validate_domain, "domain"),
    ):
        value = record.get(key)
        issue = fn(str(value) if value is not None else None)
        if issue is not None:
            issues.append(issue)
    return ValidationResult(valid=len(issues) == 0, issues=issues)
