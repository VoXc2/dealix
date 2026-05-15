"""
Arabic NLP pipeline — orchestrates normalizer + NER + sentiment for a given text.
خط معالجة اللغة العربية — يُنسّق التطبيع + استخراج الكيانات + تحليل المشاعر.

Usage:
    pipeline = ArabicNLPPipeline()
    result = await pipeline.run("الخدمة ممتازة. اتصل بمحمد على 0512345678")
    # {
    #   "normalized": "...",
    #   "entities": [...],
    #   "sentiment": {"label": "positive", "score": 0.87, ...},
    #   "language": "ar",
    #   "token_count": 7
    # }
"""

from __future__ import annotations

from typing import Any

from core.logging import get_logger
from core.nlp.ner import extract_entities
from core.nlp.normalizer import is_arabic, normalize_arabic, tokenize_arabic
from core.nlp.sentiment import ArabicSentimentAnalyzer

logger = get_logger(__name__)


class ArabicNLPPipeline:
    """
    End-to-end Arabic NLP pipeline.
    خط أنابيب NLP العربي الكامل.

    Combines:
      - Text normalization
      - Language detection
      - Named entity extraction (regex + optional LLM)
      - Sentiment analysis (lexicon + optional LLM)

    All steps are optional and configurable.
    """

    def __init__(self) -> None:
        self._sentiment = ArabicSentimentAnalyzer()

    async def run(
        self,
        text: str,
        *,
        include_ner: bool = True,
        include_sentiment: bool = True,
        include_llm_ner: bool = False,
        include_llm_sentiment: bool = False,
        llm_task: Any = None,
    ) -> dict[str, Any]:
        """
        Run the full Arabic NLP pipeline.
        تشغيل خط أنابيب NLP العربي الكامل.

        Parameters
        ----------
        text : str
            Raw input text (Arabic or mixed).
        include_ner : bool
            Extract named entities (default True).
        include_sentiment : bool
            Analyze sentiment (default True).
        include_llm_ner : bool
            Use LLM for richer NER — PERSON, ORG, GPE, PRODUCT (default False).
        include_llm_sentiment : bool
            Use LLM for sentiment when lexicon confidence is low (default False).
        llm_task : Task | None
            LLM task handle required for LLM-based features.

        Returns
        -------
        dict with keys: normalized, entities, sentiment, language, token_count
        """
        if not text or not text.strip():
            return _empty_result()

        # 1. Normalize
        normalized = normalize_arabic(text)

        # 2. Language detection
        language = "ar" if is_arabic(text) else "mixed"

        # 3. Tokenize
        tokens = tokenize_arabic(normalized, normalize=False)

        # 4. NER
        entities: list[dict[str, Any]] = []
        if include_ner:
            try:
                entities = await extract_entities(
                    text,
                    include_llm=include_llm_ner,
                    llm_task=llm_task,
                )
            except Exception as exc:
                logger.warning("pipeline_ner_error", error=str(exc))

        # 5. Sentiment
        sentiment: dict[str, Any] = {}
        if include_sentiment:
            try:
                sentiment = await self._sentiment.analyze_async(
                    normalized,
                    force_llm=include_llm_sentiment,
                    task=llm_task,
                )
            except Exception as exc:
                logger.warning("pipeline_sentiment_error", error=str(exc))
                sentiment = {"label": "neutral", "score": 0.5, "method": "fallback"}

        return {
            "original": text,
            "normalized": normalized,
            "language": language,
            "token_count": len(tokens),
            "entities": entities,
            "sentiment": sentiment,
        }

    def normalize(self, text: str) -> str:
        """Convenience: normalize only."""
        return normalize_arabic(text)

    def detect_language(self, text: str) -> str:
        """Convenience: detect language."""
        return "ar" if is_arabic(text) else "mixed"


def _empty_result() -> dict[str, Any]:
    return {
        "original": "",
        "normalized": "",
        "language": "unknown",
        "token_count": 0,
        "entities": [],
        "sentiment": {},
    }
