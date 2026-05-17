"""Affiliate messaging compliance — Full Ops spec §8.

Affiliates promote Dealix in their own words, but every promotional
message must carry a referral disclosure and must never use cold
WhatsApp, guarantee language, or spam patterns. This enforces the
non-negotiables (no cold WhatsApp, no guaranteed outcomes, no
un-sourced claims) on affiliate-authored copy.

Pure logic; no I/O.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

DISCLOSURE_AR = (
    "تنويه: قد أحصل على عمولة إحالة إذا اشتركت عبر هذا الرابط. أوصي بـDealix "
    "فقط للفرق التي تحتاج تشغيل الإيراد والذكاء الاصطناعي بشكل محكوم وقابل للقياس."
)
DISCLOSURE_EN = (
    "Disclosure: I may earn a referral commission if you sign up via this "
    "link. I only recommend Dealix to teams that need governed, measurable "
    "revenue and AI operations."
)

# Markers that indicate a disclosure is present.
_DISCLOSURE_MARKERS = (
    "تنويه",
    "عمولة إحالة",
    "disclosure",
    "referral commission",
    "affiliate",
    "#ad",
    "#affiliate",
)

# Guarantee language — forbidden (non-negotiable: no guaranteed outcomes).
_GUARANTEE_MARKERS = (
    "نضمن",
    "مضمون",
    "ضمان النتائج",
    "guarantee",
    "guaranteed",
    "guaranteed roi",
)

# Cold-WhatsApp / mass-broadcast intent — forbidden.
_COLD_WHATSAPP_MARKERS = (
    "cold whatsapp",
    "whatsapp blast",
    "mass whatsapp",
    "واتساب بارد",
    "رسائل جماعية",
    "broadcast list",
)

# Spam patterns.
_SPAM_MARKERS = (
    "act now",
    "limited time only",
    "100% free money",
    "اربح الآن",
    "عرض لن يتكرر",
)


@dataclass
class ComplianceResult:
    compliant: bool
    has_disclosure: bool
    violations: list[str] = field(default_factory=list)
    notes_ar: str = ""
    notes_en: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _contains_any(haystack: str, needles: tuple[str, ...]) -> bool:
    return any(n in haystack for n in needles)


def check_affiliate_message(text: str, *, channel: str = "") -> ComplianceResult:
    """Check an affiliate-authored promotional message for compliance.

    Every message is treated as promotional, so a referral disclosure is
    always required. Returns a structured result; callers should block
    any non-compliant message before it is shared.
    """
    lowered = (text or "").lower()
    violations: list[str] = []

    has_disclosure = _contains_any(lowered, _DISCLOSURE_MARKERS)
    if not has_disclosure:
        violations.append("missing_disclosure")

    if _contains_any(lowered, _GUARANTEE_MARKERS):
        violations.append("guaranteed_outcome_language")

    if _contains_any(lowered, _COLD_WHATSAPP_MARKERS) or (
        channel or ""
    ).lower() == "cold_whatsapp":
        violations.append("cold_whatsapp")

    if _contains_any(lowered, _SPAM_MARKERS):
        violations.append("spam_pattern")

    # Shouting / excessive punctuation is a spam signal.
    if re.search(r"[!]{3,}", text or ""):
        violations.append("spam_pattern")

    violations = sorted(set(violations))
    compliant = not violations

    if compliant:
        notes_ar = "الرسالة متوافقة. أضف رابط الإحالة الخاص بك قبل النشر."
        notes_en = "Message is compliant. Add your referral link before posting."
    else:
        notes_ar = "الرسالة غير متوافقة — صحّح المخالفات قبل النشر."
        notes_en = "Message is not compliant — fix the violations before posting."

    return ComplianceResult(
        compliant=compliant,
        has_disclosure=has_disclosure,
        violations=violations,
        notes_ar=notes_ar,
        notes_en=notes_en,
    )


__all__ = [
    "DISCLOSURE_AR",
    "DISCLOSURE_EN",
    "ComplianceResult",
    "check_affiliate_message",
]
