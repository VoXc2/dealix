"""V12 Support OS — rule-based bilingual classifier.

Categories per V12 plan: onboarding, billing, payment, technical_issue,
connector_setup, diagnostic_question, proof_pack_question,
privacy_pdpl, refund, angry_customer, upgrade_question, unknown.

NO LLM call. Pure regex/keyword match. Arabic Saudi tone primary.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

SupportCategory = Literal[
    "onboarding",
    "billing",
    "payment",
    "technical_issue",
    "connector_setup",
    "diagnostic_question",
    "proof_pack_question",
    "privacy_pdpl",
    "refund",
    "angry_customer",
    "upgrade_question",
    "unknown",
]


@dataclass
class ClassificationResult:
    category: SupportCategory
    confidence: float  # 0.0 – 1.0
    matched_terms: list[str]
    is_arabic: bool
    needs_human_immediately: bool


# (category, list of (regex, weight)) — regex is case-insensitive, Arabic-aware
_PATTERNS: list[tuple[SupportCategory, list[tuple[str, float]]]] = [
    ("refund", [
        (r"\brefund\b|\brefunded\b|\bmoney\s*back\b", 1.0),
        (r"استرجاع|استرداد|إرجاع\s+المبلغ|أبغى\s+فلوسي", 1.0),
    ]),
    ("payment", [
        (r"\bpayment\b|\binvoice\b|\bcharge(d)?\b|\bbilled\b|\bmoyasar\b", 0.9),
        (r"دفع|فاتورة|سحب|خصم|ميسر", 0.9),
    ]),
    ("billing", [
        (r"\bbilling\b|\breceipt\b|\bsubscription\b|\bplan\b", 0.7),
        (r"اشتراك|خطّة|إيصال|سعر", 0.7),
    ]),
    ("privacy_pdpl", [
        (r"\bprivacy\b|\bpdpl\b|\bdelete\s+(my\s+)?data\b|\bgdpr\b|\bopt[-\s]*out\b", 1.0),
        (r"خصوصيّة|خصوصية|بيان(ا|اتي|اتنا)|احذف|حذف\s+بيانات|إلغاء\s+الموافقة", 1.0),
    ]),
    ("angry_customer", [
        (r"\b(angry|terrible|awful|worst|garbage|scam|fraud)\b", 1.0),
        (r"\b(complain|complaint|frustrat|upset)\b", 0.8),
        (r"زفت|قرف|محتال|نصب|كذّاب|نصابين|سيء|أسوأ", 1.0),
        (r"شكوى|تظلّم", 0.8),
    ]),
    ("technical_issue", [
        (r"\b(error|bug|crash|broken|not\s+working|fail(ed|ing)?|500|404|timeout)\b", 0.9),
        (r"خطأ|عطل|ما\s+يشتغل|ما\s+يفتح|توقّف|تعليق|مشكلة\s+تقنيّة", 0.9),
    ]),
    ("connector_setup", [
        (r"\b(connect(or|ing)?|integration|webhook|api\s+key|setup|configure|configur)\b", 0.8),
        (r"ربط|تكامل|إعداد|مفتاح\s+API|تكوين", 0.8),
    ]),
    ("onboarding", [
        (r"\b(get(ting)?\s+started|onboard|first\s+time|new\s+customer|how\s+do\s+i\s+start)\b", 0.9),
        (r"كيف\s+أبدأ|أوّل\s+مرّة|مبتدئ|مقدّمة", 0.9),
    ]),
    ("diagnostic_question", [
        (r"\b(diagnostic|mini[\s-]?diagnostic|تشخيص)\b", 0.9),
    ]),
    ("proof_pack_question", [
        (r"\b(proof\s*pack|case\s+study|results)\b", 0.8),
        (r"دليل|إثبات|نتائج", 0.8),
    ]),
    ("upgrade_question", [
        (r"\b(upgrade|enterprise|custom\s+plan|tier|extend\s+pilot)\b", 0.8),
        (r"ترقية|باقة\s+أعلى|تمديد|اشتراك\s+أكبر", 0.8),
    ]),
]


_ARABIC_RE = re.compile(r"[؀-ۿ]")


def classify_message(text: str) -> ClassificationResult:
    """Classify a support message into one of 12 categories.

    Pure-local; never calls an LLM. Returns ``unknown`` with low
    confidence if no pattern matches.
    """
    if not text or not text.strip():
        return ClassificationResult(
            category="unknown",
            confidence=0.0,
            matched_terms=[],
            is_arabic=False,
            needs_human_immediately=False,
        )

    is_arabic = bool(_ARABIC_RE.search(text))
    scores: dict[SupportCategory, float] = {}
    matched: dict[SupportCategory, list[str]] = {}
    for cat, patterns in _PATTERNS:
        for pat, weight in patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                scores[cat] = scores.get(cat, 0.0) + weight
                matched.setdefault(cat, []).append(m.group(0))

    if not scores:
        return ClassificationResult(
            category="unknown",
            confidence=0.0,
            matched_terms=[],
            is_arabic=is_arabic,
            needs_human_immediately=False,
        )

    # Pick highest score; tiebreak by category list order
    top = max(scores.items(), key=lambda kv: kv[1])
    category, score = top
    # Confidence saturates at 1.0 once score ≥ 1.0
    confidence = min(1.0, score)
    needs_human = category in {"refund", "privacy_pdpl", "angry_customer", "payment"}
    return ClassificationResult(
        category=category,
        confidence=confidence,
        matched_terms=matched.get(category, []),
        is_arabic=is_arabic,
        needs_human_immediately=needs_human,
    )
