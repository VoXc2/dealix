"""Trust-plane PII detector — bridges Data OS scans into the Trust gate.

كاشف PII على مستوى Trust — يربط فحوصات Data OS ببوابة Governance.

Imports from `auto_client_acquisition.customer_data_plane.pii_detection`
rather than re-implementing patterns. Adds policy-shaped decisions used
by Governance OS pre-action checks.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.customer_data_plane.pii_detection import (
    PIIScan,
    scan_batch,
    scan_record,
)


class PIIVerdict(StrEnum):
    CLEAN = "clean"
    REDACTED = "redacted"
    BLOCKED = "blocked"


class PIIPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    allow_pii_in_outputs: bool = False
    allow_pii_in_logs: bool = False
    redact_in_messages: bool = True
    block_card_iban: bool = True


class PIIDecision(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")
    verdict: PIIVerdict
    reason_ar: str
    reason_en: str
    scan: PIIScan


_DEFAULT_POLICY = PIIPolicy()


def decide_for_record(record: dict, *, policy: PIIPolicy | None = None) -> PIIDecision:
    pol = policy or _DEFAULT_POLICY
    scan = scan_record(record)
    if not scan.has_pii:
        return PIIDecision(
            verdict=PIIVerdict.CLEAN,
            reason_ar="لا توجد بيانات شخصية مكتشفة.",
            reason_en="No PII detected.",
            scan=scan,
        )

    if pol.block_card_iban and any(h.kind in ("card", "iban") for h in scan.hits):
        return PIIDecision(
            verdict=PIIVerdict.BLOCKED,
            reason_ar="بيانات مالية حساسة (بطاقة/IBAN) ممنوع تمريرها.",
            reason_en="Sensitive financial data (card/IBAN) is blocked from downstream actions.",
            scan=scan,
        )

    if pol.allow_pii_in_outputs:
        return PIIDecision(
            verdict=PIIVerdict.CLEAN,
            reason_ar="السياسة تسمح بـ PII (لوحة Trust / عرض داخلي).",
            reason_en="Policy permits PII in outputs (internal Trust view).",
            scan=scan,
        )

    return PIIDecision(
        verdict=PIIVerdict.REDACTED,
        reason_ar="تطبّق سياسة الإخفاء قبل التمرير.",
        reason_en="Redaction policy applied before downstream pass-through.",
        scan=scan,
    )


def decide_for_batch(
    records: list[dict], *, policy: PIIPolicy | None = None
) -> PIIDecision:
    pol = policy or _DEFAULT_POLICY
    scan = scan_batch(records)
    if not scan.has_pii:
        return PIIDecision(
            verdict=PIIVerdict.CLEAN,
            reason_ar="الدفعة نظيفة من PII.",
            reason_en="Batch is PII-clean.",
            scan=scan,
        )
    if pol.block_card_iban and any(h.kind in ("card", "iban") for h in scan.hits):
        return PIIDecision(
            verdict=PIIVerdict.BLOCKED,
            reason_ar="الدفعة تحتوي بيانات مالية حساسة.",
            reason_en="Batch contains sensitive financial PII; blocked.",
            scan=scan,
        )
    return PIIDecision(
        verdict=PIIVerdict.REDACTED,
        reason_ar="سيتم إخفاء PII قبل تمرير الدفعة.",
        reason_en="PII redaction will be applied before pass-through.",
        scan=scan,
    )
