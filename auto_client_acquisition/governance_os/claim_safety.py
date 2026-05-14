"""Claim safety — detect guaranteed-outcome or unsupported claims in text.

Bilingual (AR + EN). Reuses safety_v10.output_validator where applicable
but adds an explicit non-negotiable list of "guarantee" phrases that ALWAYS
trigger a REDACT/BLOCK decision in governance_os.runtime_decision.
"""
from __future__ import annotations

import re

# Each pattern is a regex (case-insensitive). Use word boundaries where
# possible to avoid catching innocent substrings.
FORBIDDEN_CLAIM_PATTERNS: tuple[tuple[str, str], ...] = (
    # English
    (r"\bguarantee[ds]?\b", "guarantee language"),
    (r"\bguaranteed\s+(sales|revenue|leads|deals)\b", "guaranteed business outcome"),
    (r"\b100\s*%\s*(success|guaranteed|certain)\b", "100% outcome claim"),
    (r"\brisk[- ]free\s+(sales|revenue|outcome)\b", "risk-free outcome claim"),
    (r"\bzero[- ]?risk\b", "zero-risk claim"),
    # Arabic
    (r"نضمن", "ضمان عربي"),
    (r"مضمون(ة|ون)?\s*(المبيعات|الإيراد|العملاء)?", "ضمان نتيجة عربي"),
    (r"١٠٠\s*%\s*(ضمان|نجاح|مؤكد)", "ادعاء ١٠٠٪"),
    (r"بدون\s+مخاطر", "ادعاء بدون مخاطر"),
)


def contains_unsafe_claim(text: str) -> tuple[bool, list[str]]:
    """Returns (has_unsafe, reasons). Empty reasons list iff clean."""
    if not text:
        return False, []
    reasons: list[str] = []
    for pattern, label in FORBIDDEN_CLAIM_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            reasons.append(label)
    return bool(reasons), reasons


__all__ = ["FORBIDDEN_CLAIM_PATTERNS", "contains_unsafe_claim"]
