"""
Arabic NLP pipeline.
معالجة اللغة العربية.
"""

from core.nlp.ner import extract_entities
from core.nlp.normalizer import normalize_arabic
from core.nlp.pipeline import ArabicNLPPipeline
from core.nlp.sentiment import ArabicSentimentAnalyzer

__all__ = [
    "ArabicNLPPipeline",
    "ArabicSentimentAnalyzer",
    "extract_entities",
    "normalize_arabic",
]
