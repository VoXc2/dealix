"""Bilingual reporting keys."""

from __future__ import annotations

BILINGUAL_REPORT_KEYS: tuple[str, ...] = ("summary_ar", "summary_en", "governance_notes_ar", "governance_notes_en")


def bilingual_report_complete(fields: dict[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(k for k in BILINGUAL_REPORT_KEYS if not (fields.get(k) or "").strip())
    return not missing, missing


__all__ = ["BILINGUAL_REPORT_KEYS", "bilingual_report_complete"]
