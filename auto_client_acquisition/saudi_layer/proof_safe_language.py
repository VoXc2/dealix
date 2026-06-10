"""Proof-safe Arabic language — L0-L5 evidence-based communication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any

PROOF_SAFE_PHRASE_AR = "ما يُذكر هنا مبني على أدلة المشروع والحدود المعلنة؛ لا وعود مبيعات."


class ProofLevel(IntEnum):
    """Evidence levels L0-L5 for proof-safe claims."""

    L0 = 0  # No evidence — cannot make any claim
    L1 = 1  # Anecdotal — "our client said"
    L2 = 2  # Self-reported — "client reported 20% increase"
    L3 = 3  # Observed — "we measured 20% increase in data"
    L4 = 4  # Verified — independently verified by third party
    L5 = 5  # Certified — formally certified (e.g., ISO, G-Mark)


LEVEL_LABELS: dict[ProofLevel, str] = {
    ProofLevel.L0: "بدون دليل — لا يجوز الادعاء",
    ProofLevel.L1: "حكائي — قال العميل",
    ProofLevel.L2: "تبليغي — أبلغ العميل",
    ProofLevel.L3: "ملاحظ — قمنا بقياس",
    ProofLevel.L4: "موثّق — تحقق طرف ثالث",
    ProofLevel.L5: "معتمد — شهادة رسمية",
}

LEVEL_LABELS_EN: dict[ProofLevel, str] = {
    ProofLevel.L0: "No evidence — no claim allowed",
    ProofLevel.L1: "Anecdotal — client said",
    ProofLevel.L2: "Self-reported — client reported",
    ProofLevel.L3: "Observed — we measured",
    ProofLevel.L4: "Verified — third-party verified",
    ProofLevel.L5: "Certified — formally certified",
}

# Allowed phrases per proof level
ALLOWED_PHRASES_L3: list[str] = [
    "بناءً على قياساتنا",
    "أظهرت نتائجنا",
    "لاحظنا تحسناً بنسبة",
    "سجلنا زيادة",
    "بياناتنا تشير إلى",
]

ALLOWED_PHRASES_L4: list[str] = [
    "وفقاً لتقرير التدقيق المستقل",
    "أكدت جهة خارجية",
    "حصلنا على شهادة من",
    "تم التحقق من قبل",
]

ALLOWED_PHRASES_L5: list[str] = [
    "حاصل على شهادة",
    "معتمد من",
    "حائز على جائزة",
    "مطابق للمعيار",
]

# Phrases not tied to evidence (always safe)
GENERIC_SAFE_PHRASES: list[str] = [
    "نسعى لتحقيق",
    "نعمل على",
    "هدفنا",
    "من أولوياتنا",
    "نلتزم بـ",
]


@dataclass
class ClaimAssessment:
    """Assessment of whether a claim is proof-safe."""

    claim: str
    min_proof_level: ProofLevel
    actual_proof_level: ProofLevel
    is_safe: bool
    risk: str  # low, medium, high
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim": self.claim,
            "min_proof_level": int(self.min_proof_level),
            "min_proof_level_label": LEVEL_LABELS[self.min_proof_level],
            "actual_proof_level": int(self.actual_proof_level),
            "actual_proof_level_label": LEVEL_LABELS[self.actual_proof_level],
            "is_safe": self.is_safe,
            "risk": self.risk,
            "reason": self.reason,
        }


# Claim patterns mapped to minimum required proof level
CLAIM_PATTERNS: list[tuple[str, int, str]] = [
    # (pattern, min_level, description)
    ("نسبة", 3, "Percentage claims require measurement"),
    ("زيادة", 3, "Increase claims require measurement"),
    ("تحسن", 3, "Improvement claims require measurement"),
    ("توفير", 3, "Savings claims require measurement"),
    ("خفض", 3, "Reduction claims require measurement"),
    ("ارتفاع", 3, "Rise claims require measurement"),
    ("انخفاض", 3, "Decline claims require measurement"),
    ("%", 3, "Percentage sign requires evidence"),
    ("الأول", 4, "First/best claims need verification"),
    ("الأفضل", 4, "Best claims need third-party verification"),
    ("معتمد", 5, "Certified claims need formal certification"),
    ("حاصل على", 5, "Award claims need formal certification"),
    ("جائزة", 5, "Award claims need formal certification"),
    ("حائز", 5, "Award claims need formal certification"),
    ("شهادة", 5, "Certification claims need formal certification"),
    ("مطابق", 5, "Conformity claims need formal certification"),
]


def assess_claim_safety(claim_text: str, evidence_level: ProofLevel) -> ClaimAssessment:
    """Assess whether a claim is safe given the available evidence level.

    Args:
        claim_text: The Arabic claim text.
        evidence_level: The level of evidence available.

    Returns:
        ClaimAssessment with safety determination.
    """
    blob = claim_text.lower()
    required_level = ProofLevel.L0
    matched_pattern = ""

    for pattern, min_level, _desc in CLAIM_PATTERNS:
        if pattern in blob:
            if min_level > required_level:
                required_level = ProofLevel(min_level)
                matched_pattern = pattern

    if required_level == ProofLevel.L0:
        return ClaimAssessment(
            claim=claim_text,
            min_proof_level=ProofLevel.L0,
            actual_proof_level=evidence_level,
            is_safe=True,
            risk="low",
            reason="لا يوجد نمط ادعاء يتطلب دليلاً",
        )

    is_safe = evidence_level >= required_level

    if is_safe:
        risk = "low"
        reason = f"مستوى الدليل ({int(evidence_level)}) كافٍ لهذا الادعاء"
    else:
        gap = required_level - evidence_level
        if gap >= 2:
            risk = "high"
        else:
            risk = "medium"
        reason = (
            f"هذا الادعاء يتطلب مستوى دليل {int(required_level)} "
            f"( {LEVEL_LABELS[required_level]} ) "
            f"ولكن المتاح هو {int(evidence_level)} "
            f"( {LEVEL_LABELS[evidence_level]} )"
        )

    return ClaimAssessment(
        claim=claim_text,
        min_proof_level=required_level,
        actual_proof_level=evidence_level,
        is_safe=is_safe,
        risk=risk,
        reason=reason,
    )


def safe_phrase_for_level(level: ProofLevel) -> list[str]:
    """Get allowed phrasing templates for a given proof level.

    Args:
        level: The evidence level.

    Returns:
        List of safe Arabic phrases appropriate for the level.
    """
    phrases: list[str] = list(GENERIC_SAFE_PHRASES)

    if level >= ProofLevel.L3:
        phrases.extend(ALLOWED_PHRASES_L3)
    if level >= ProofLevel.L4:
        phrases.extend(ALLOWED_PHRASES_L4)
    if level >= ProofLevel.L5:
        phrases.extend(ALLOWED_PHRASES_L5)

    return phrases


def get_proof_safe_footer(level: ProofLevel) -> str:
    """Get a proof-safe footer text based on evidence level.

    Args:
        level: The maximum available evidence level.

    Returns:
        Arabic footer string.
    """
    if level == ProofLevel.L0:
        return "هذا العرض للأغراض التوضيحية فقط ولا يمثل نتائج مضمونة."
    elif level <= ProofLevel.L2:
        return "المعلومات المذكورة مبنية على تقارير العملاء. النتائج الفعلية قد تختلف."
    elif level <= ProofLevel.L3:
        return "النتائج المذكورة مبنية على قياساتنا. قد تختلف النتائج حسب الحالة."
    elif level <= ProofLevel.L4:
        return "النتائج تم التحقق منها من قبل جهة مستقلة. جميع الادعاءات مدعومة بأدلة."
    else:
        return "جميع الادعاءات معتمدة رسمياً ومدعومة بشهادات موثقة."


__all__ = [
    "ALLOWED_PHRASES_L3",
    "ALLOWED_PHRASES_L4",
    "ALLOWED_PHRASES_L5",
    "CLAIM_PATTERNS",
    "ClaimAssessment",
    "GENERIC_SAFE_PHRASES",
    "LEVEL_LABELS",
    "LEVEL_LABELS_EN",
    "PROOF_SAFE_PHRASE_AR",
    "ProofLevel",
    "assess_claim_safety",
    "get_proof_safe_footer",
    "safe_phrase_for_level",
]
