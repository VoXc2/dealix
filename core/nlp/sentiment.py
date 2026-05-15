"""
Arabic sentiment analyzer — rule-based lexicon + LLM fallback.
محلّل المشاعر العربية.

Outputs: positive / negative / neutral with a confidence score [0.0–1.0].

Two modes:
  1. Fast lexicon-based: uses an embedded Arabic sentiment lexicon
     (AraSenti word lists). O(n) time, no API cost.
  2. LLM-based: more accurate for complex / sarcastic texts.
     Triggered when lexicon confidence < 0.6 OR force_llm=True.

Usage:
    analyzer = ArabicSentimentAnalyzer()
    result = analyzer.analyze("الخدمة ممتازة وسريعة")
    # → {"label": "positive", "score": 0.87, "method": "lexicon"}

    result = await analyzer.analyze_async("...", force_llm=True, task=task)
    # → {"label": "positive", "score": 0.92, "method": "llm"}
"""

from __future__ import annotations

from typing import Any

from core.logging import get_logger
from core.nlp.normalizer import normalize_arabic, tokenize_arabic

logger = get_logger(__name__)


# ── Embedded mini lexicon (curated, not exhaustive) ───────────────
# Format: word → score in [-1.0, +1.0]
# Sourced from: AraSenti, ASTD, and manually curated Saudi business vocabulary

_POSITIVE_WORDS: dict[str, float] = {
    # Superlatives
    "ممتاز": 0.9, "رائع": 0.85, "مذهل": 0.9, "عظيم": 0.85,
    "جيد": 0.6, "جميل": 0.7, "مفيد": 0.65, "ايجابي": 0.7,
    "إيجابي": 0.7, "مميز": 0.75, "متميز": 0.75, "احترافي": 0.8,
    "محترف": 0.8, "سريع": 0.6, "دقيق": 0.65, "موثوق": 0.75,
    "ثقة": 0.7, "نجاح": 0.8, "ربح": 0.75, "نمو": 0.7,
    "تطور": 0.65, "تحسن": 0.65, "فعال": 0.7, "فعّال": 0.7,
    "مبتكر": 0.75, "ابداع": 0.8, "إبداع": 0.8, "خبرة": 0.65,
    "كفاءة": 0.75, "انجاز": 0.8, "إنجاز": 0.8, "راضي": 0.75,
    "مرضي": 0.7, "مقبول": 0.55, "صحيح": 0.6, "صادق": 0.7,
    # Business-specific
    "صفقة": 0.6, "عرض_جيد": 0.75, "قيمة": 0.6, "وفر": 0.65,
}

_NEGATIVE_WORDS: dict[str, float] = {
    # Negatives
    "سيء": -0.8, "رديء": -0.85, "فاشل": -0.85, "فشل": -0.8,
    "مشكلة": -0.6, "خطأ": -0.65, "غلط": -0.65, "بطيء": -0.6,
    "بطيئ": -0.6, "صعب": -0.5, "مكلف": -0.55, "غالي": -0.5,
    "احتيال": -0.95, "نصب": -0.95, "كذب": -0.85, "ضعيف": -0.75,
    "خسارة": -0.8, "ضرر": -0.8, "مخاطرة": -0.6, "تاخير": -0.7,
    "تأخير": -0.7, "رفض": -0.7, "الغاء": -0.65, "إلغاء": -0.65,
    "شكوى": -0.75, "اهمال": -0.8, "إهمال": -0.8, "فوضى": -0.75,
    "عدم_الثقة": -0.8, "تعقيد": -0.6, "صعوبة": -0.55,
}

# Negation modifiers — flip sentiment of next word
_NEGATION_WORDS = {"لا", "لم", "لن", "ليس", "ليست", "غير", "عدم", "لو_لا"}

# Intensifiers (amplify next word score by factor)
_INTENSIFIERS: dict[str, float] = {
    "جدا": 1.3, "جداً": 1.3, "كثيرا": 1.2, "كثيراً": 1.2,
    "للغاية": 1.4, "تماما": 1.25, "تماماً": 1.25, "أكثر": 1.2,
}


class ArabicSentimentAnalyzer:
    """
    Lexicon-based Arabic sentiment analyzer with LLM fallback.
    محلّل المشاعر العربية بالمعجم مع احتياط من النموذج اللغوي.
    """

    def analyze(self, text: str) -> dict[str, Any]:
        """
        Synchronous lexicon-based analysis.
        تحليل متزامن قائم على المعجم.

        Returns {"label": str, "score": float, "raw_score": float, "method": str}
        """
        tokens = tokenize_arabic(text, normalize=True)
        return self._score_tokens(tokens)

    async def analyze_async(
        self,
        text: str,
        *,
        force_llm: bool = False,
        llm_threshold: float = 0.55,
        task: Any = None,
    ) -> dict[str, Any]:
        """
        Async analysis with optional LLM fallback.
        تحليل غير متزامن مع احتياط من النموذج اللغوي.

        If lexicon confidence < llm_threshold OR force_llm=True and task provided,
        falls back to LLM for a more accurate result.
        """
        result = self.analyze(text)

        should_use_llm = (
            task is not None
            and (force_llm or result["score"] < llm_threshold)
        )
        if should_use_llm:
            try:
                llm_result = await self._analyze_llm(text, task)
                llm_result["lexicon_backup"] = result
                return llm_result
            except Exception as exc:
                logger.warning("sentiment_llm_error", error=str(exc))

        return result

    def _score_tokens(self, tokens: list[str]) -> dict[str, Any]:
        """Core lexicon scoring."""
        total_score = 0.0
        found_count = 0
        negated = False
        amplifier = 1.0

        for i, token in enumerate(tokens):
            # Negation window
            if token in _NEGATION_WORDS:
                negated = True
                continue

            # Intensifier
            if token in _INTENSIFIERS:
                amplifier = _INTENSIFIERS[token]
                continue

            # Positive lexicon
            score = _POSITIVE_WORDS.get(token, 0.0)
            if score == 0.0:
                score = -_NEGATIVE_WORDS.get(token, 0.0) if token not in _NEGATIVE_WORDS else _NEGATIVE_WORDS[token]
                score = _NEGATIVE_WORDS.get(token, 0.0)

            if score != 0.0:
                score *= amplifier
                if negated:
                    score = -score * 0.8  # weakened flip
                total_score += score
                found_count += 1
                negated = False
                amplifier = 1.0
            elif negated and i < len(tokens) - 1:
                # Reset negation after one non-sentiment word
                pass
            else:
                negated = False
                amplifier = 1.0

        if found_count == 0:
            return {"label": "neutral", "score": 0.5, "raw_score": 0.0, "method": "lexicon"}

        avg = total_score / found_count
        # Normalise to [0, 1] confidence
        confidence = min(abs(avg), 1.0)

        if avg > 0.15:
            label = "positive"
        elif avg < -0.15:
            label = "negative"
        else:
            label = "neutral"

        return {
            "label": label,
            "score": round(confidence, 3),
            "raw_score": round(avg, 4),
            "method": "lexicon",
        }

    async def _analyze_llm(self, text: str, task: Any) -> dict[str, Any]:
        """LLM-based sentiment analysis for complex cases."""
        import json

        from core.llm import get_router
        from core.llm.base import Message

        prompt = (
            "Analyze the sentiment of this Arabic business text.\n"
            "Return ONLY JSON: {\"label\": \"positive\"|\"negative\"|\"neutral\", "
            "\"score\": 0.0-1.0, \"reason\": \"...\"}\n\n"
            f"Text: {text}"
        )
        router = get_router()
        response = await router.run(
            task,
            messages=[Message(role="user", content=prompt)],
            system="You are an Arabic NLP expert. Output valid JSON only.",
            max_tokens=128,
            temperature=0.0,
        )
        raw = response.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```")
        raw = raw.removesuffix("```").strip()
        result = json.loads(raw)
        result["method"] = "llm"
        return result
