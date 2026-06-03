"""Dedupe helpers — re-export Revenue OS pure functions."""

from __future__ import annotations

from auto_client_acquisition.revenue_os.dedupe import (
    DedupeHint,
    normalize_company_name,
    normalize_domain,
    normalize_phone_e164_hint,
    suggest_dedupe_fingerprint,
)

__all__ = [
    "DedupeHint",
    "normalize_company_name",
    "normalize_domain",
    "normalize_phone_e164_hint",
    "suggest_dedupe_fingerprint",
]
