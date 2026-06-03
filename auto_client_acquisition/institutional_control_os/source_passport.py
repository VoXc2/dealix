"""Institutional Source Passport — gate before AI use (wraps sovereignty standard)."""

from __future__ import annotations

from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_allows_task,
    source_passport_valid_for_ai,
)

__all__ = (
    "SourcePassport",
    "institutional_source_ai_allowed",
    "source_passport_allows_task",
    "source_passport_valid_for_ai",
)


def institutional_source_ai_allowed(passport: SourcePassport) -> tuple[bool, tuple[str, ...]]:
    """Institutional rule: no valid passport path → no AI use."""
    return source_passport_valid_for_ai(passport)
