"""Heuristic PII column / cell flags (deterministic, no ML)."""

from __future__ import annotations

import re
from typing import Any

from auto_client_acquisition.data_os.schemas import PIIFlag

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE = re.compile(r"^\+?\d[\d\s\-]{7,}\d$")


def pii_flags_for_row(row: dict[str, Any]) -> list[PIIFlag]:
    flags: list[PIIFlag] = []
    for key, val in row.items():
        if val is None:
            continue
        s = str(val).strip()
        if not s:
            continue
        lk = str(key).lower()
        if "email" in lk and _EMAIL.search(s):
            flags.append(PIIFlag(field=key, reason="email_pattern"))
        if lk in {"phone", "mobile", "tel"} and _PHONE.search(s.replace(" ", "")):
            flags.append(PIIFlag(field=key, reason="phone_pattern"))
        if lk in {"national_id", "iqama", "passport"}:
            flags.append(PIIFlag(field=key, reason="identifier_field_name"))
    return flags


def column_name_suggests_pii(name: str) -> bool:
    n = name.lower()
    return any(
        x in n
        for x in (
            "email",
            "phone",
            "mobile",
            "national",
            "iqama",
            "passport",
            "iban",
        )
    )
