"""PII Detection — wrapper around existing pii_redactor with batch scoring.

كاشف البيانات الشخصية — يُستخدم كبوابة قبل إثراء/ تصدير أي سجلات.
"""
from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict


_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_SA_MOBILE = re.compile(r"(?:\+?966|0)5\d{8}")
_NATIONAL_ID = re.compile(r"\b[12]\d{9}\b")  # Saudi National ID / Iqama heuristic
_IBAN = re.compile(r"\bSA\d{22}\b")
_CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")


class PIIHit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field: str
    kind: str
    snippet: str


class PIIScan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    has_pii: bool
    hits: list[PIIHit]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _scan_value(field: str, value: str) -> list[PIIHit]:
    hits: list[PIIHit] = []
    for kind, pattern in (
        ("email", _EMAIL),
        ("phone_sa", _SA_MOBILE),
        ("national_id", _NATIONAL_ID),
        ("iban", _IBAN),
        ("card", _CARD),
    ):
        for m in pattern.findall(value):
            hits.append(
                PIIHit(field=field, kind=kind, snippet=str(m)[:24])
            )
    return hits


def scan_record(record: dict[str, Any]) -> PIIScan:
    hits: list[PIIHit] = []
    for k, v in record.items():
        if isinstance(v, str):
            hits.extend(_scan_value(k, v))
    return PIIScan(has_pii=bool(hits), hits=hits)


def scan_batch(records: list[dict[str, Any]]) -> PIIScan:
    all_hits: list[PIIHit] = []
    for r in records:
        all_hits.extend(scan_record(r).hits)
    return PIIScan(has_pii=bool(all_hits), hits=all_hits)


def mask(value: str) -> str:
    """Mask a value by keeping first 2 + last 2 chars, replacing middle with *."""
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]
