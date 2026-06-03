"""
Prohibited-claims detection (Arabic + English).

Dealix must never make guaranteed / exaggerated revenue claims. This module
detects them in any outbound text (email drafts, WhatsApp drafts, proposals,
content, press). It is intentionally conservative: a false positive only
forces a human rewrite, while a false negative could damage trust or breach
advertising/PDPL norms.
"""

from __future__ import annotations

import re
from typing import List

# Exact-substring prohibited phrases (case-insensitive for Latin script).
_PROHIBITED_SUBSTRINGS = [
    # English: guarantees
    "guarantee",
    "guaranteed",
    "results guaranteed",
    "guaranteed results",
    "guaranteed revenue",
    "guaranteed roi",
    "100% guaranteed",
    "money back guarantee",
    "risk free",
    "risk-free",
    "no risk",
    "double your revenue",
    "triple your revenue",
    "double your sales",
    "triple your sales",
    "instant results",
    "overnight success",
    # Arabic: guarantees / exaggeration
    "نضمن",
    "مضمون",
    "مضمونة",
    "نضمن زيادة",
    "ضمان النتائج",
    "نتائج مضمونة",
    "أرباح مضمونة",
    "ربح مضمون",
    "زيادة مضمونة",
    "نضاعف",
    "مضاعفة المبيعات",
    "مضاعفة الأرباح",
    "بدون مخاطرة",
    "بدون أي مخاطرة",
    "نتائج فورية",
    "نجاح مضمون",
    "صفر مخاطرة",
]

# Regex patterns for multiplier-style hype ("10x revenue", "5X your sales",
# "زيادة 300%", "نضاعف مبيعاتك 10 مرات").
_PROHIBITED_PATTERNS = [
    re.compile(r"\b\d+\s*[xX]\b"),                 # 10x, 5 X
    re.compile(r"\b\d{2,}\s*%\s*(more|increase|growth|زيادة|نمو)", re.IGNORECASE),
    re.compile(r"(زيادة|نمو)\s*\d{2,}\s*%"),
    re.compile(r"\b\d+\s*مرات?\b"),                 # "10 مرات"
]


def find_prohibited_claims(text: str) -> List[str]:
    """Return the list of prohibited claim markers found in ``text``.

    Empty list means the text is clear of guaranteed/exaggerated claims.
    """
    if not text:
        return []
    found: List[str] = []
    lowered = text.lower()
    for phrase in _PROHIBITED_SUBSTRINGS:
        # Latin phrases compared lowercased; Arabic has no case so either works.
        needle = phrase.lower()
        if needle in lowered:
            found.append(phrase)
    for pat in _PROHIBITED_PATTERNS:
        m = pat.search(text)
        if m:
            found.append(m.group(0).strip())
    # Deduplicate, preserve order.
    seen = set()
    unique: List[str] = []
    for item in found:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def has_prohibited_claims(text: str) -> bool:
    """True if ``text`` contains any guaranteed/exaggerated claim."""
    return len(find_prohibited_claims(text)) > 0
