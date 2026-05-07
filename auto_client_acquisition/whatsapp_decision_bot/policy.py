"""Policy — every command that implies external action MUST be
approval_required at minimum. NEVER live_send."""
from __future__ import annotations

import re

# Patterns that indicate unsafe customer outbound intent
_UNSAFE_PATTERNS = [
    re.compile(r"أرسل\s+(واتساب|رسالة|إيميل)\s+(لكل|للجميع|لجميع|لكافة)", re.IGNORECASE),
    re.compile(r"send\s+(whatsapp|message|email|sms)\s+(to\s+)?(all|everyone)", re.IGNORECASE),
    re.compile(r"رسالة\s+جماعيّة|broadcast|blast", re.IGNORECASE),
    re.compile(r"(قائمة|قائمه|القائمة)\s*(مشتراة|مشتراه|المشتراة|المشتراه)|purchased\s+list", re.IGNORECASE),
    re.compile(r"اخدش|اخترق|اسحب\s+جميع\s+الأرقام|harvest", re.IGNORECASE),
    re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
]


def is_unsafe_command(text: str) -> tuple[bool, list[str]]:
    """Returns (is_unsafe, matched_reasons_ar)."""
    matched: list[str] = []
    for p in _UNSAFE_PATTERNS:
        if p.search(text):
            matched.append(p.pattern[:50])
    return (len(matched) > 0, matched)


def can_ever_live_send() -> bool:
    """Hard gate: this layer NEVER does live customer outbound. Period."""
    return False
