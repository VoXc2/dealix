"""
Arabic NLP pipeline.
معالجة اللغة العربية.
"""

from core.nlp.pipeline import ArabicNLPPipeline
from core.nlp.normalizer import normalize_arabic
from core.nlp.sentiment import ArabicSentimentAnalyzer
from core.nlp.ner import extract_entities

__all__ = [
    "ArabicNLPPipeline",
    "normalize_arabic",
    "ArabicSentimentAnalyzer",
    "extract_entities",
]
