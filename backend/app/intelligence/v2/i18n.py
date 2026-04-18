"""
Arabic/English i18n Utilities — Dealix Lead Intelligence Engine V2
==================================================================
Transliteration, name normalization, Arabic digit normalization,
and bilingual string helpers for Gulf-focused lead processing.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

# ─────────────────────────── Arabic Digit Normalization ──────────────────────

# Eastern Arabic digits (٠١٢٣٤٥٦٧٨٩) and Farsi/Extended digits
_AR_DIGIT_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


def normalize_arabic_digits(text: str) -> str:
    """Convert Arabic-Indic / Farsi digits to ASCII digits."""
    if not text:
        return text
    return text.translate(_AR_DIGIT_MAP)


# ─────────────────────────── Arabic Text Cleaning ────────────────────────────

_ARABIC_DIACRITICS_RE = re.compile(
    r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]"
)
_TATWEEL_RE = re.compile(r"\u0640")  # Arabic Tatweel / Kashida


def strip_diacritics(text: str) -> str:
    """Remove Arabic diacritics (tashkeel) and tatweel from text."""
    text = _ARABIC_DIACRITICS_RE.sub("", text)
    text = _TATWEEL_RE.sub("", text)
    return text


def normalize_arabic_text(text: str) -> str:
    """
    Full Arabic normalization pipeline:
    1. Remove diacritics
    2. Normalize Arabic letters (alef variants → ا, ya/alef maqsura)
    3. Normalize Arabic digits
    4. Strip extra whitespace
    """
    if not text:
        return text
    text = strip_diacritics(text)
    # Normalize alef variants
    text = re.sub(r"[أإآٱ]", "ا", text)
    # Normalize ya variants
    text = re.sub(r"ى", "ي", text)
    # Normalize ta marbuta
    text = re.sub(r"ة", "ه", text)
    text = normalize_arabic_digits(text)
    text = " ".join(text.split())
    return text


# ─────────────────────────── Transliteration ─────────────────────────────────

# Simple Arabic → Latin transliteration table (common Gulf names)
_AR_TO_EN_MAP: dict[str, str] = {
    "ا": "a", "أ": "a", "إ": "i", "آ": "aa", "ب": "b", "ت": "t",
    "ث": "th", "ج": "j", "ح": "h", "خ": "kh", "د": "d", "ذ": "dh",
    "ر": "r", "ز": "z", "س": "s", "ش": "sh", "ص": "s", "ض": "d",
    "ط": "t", "ظ": "dh", "ع": "a", "غ": "gh", "ف": "f", "ق": "q",
    "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "و": "w",
    "ي": "y", "ى": "a", "ة": "a", "ء": "", "ئ": "y", "ؤ": "w",
    " ": " ",
}


def transliterate_ar_to_en(text: str) -> str:
    """Transliterate Arabic text to approximate Latin characters."""
    if not text:
        return text
    result = []
    for char in text:
        result.append(_AR_TO_EN_MAP.get(char, char))
    return "".join(result).strip()


# ─────────────────────────── Name Normalization ──────────────────────────────

# Common Arabic company suffixes to strip for dedup
_AR_COMPANY_SUFFIXES = [
    "شركة", "مؤسسة", "مجموعة", "للتجارة", "للخدمات", "للتسويق",
    "للمقاولات", "للاستشارات", "الشركة", "المؤسسة", "المجموعة",
    "ذ.م.م", "ش.م.م", "ش.م.ع", "م.م.ح",
]

# Common English company suffixes to strip for dedup
_EN_COMPANY_SUFFIXES = [
    "llc", "ltd", "limited", "inc", "corp", "corporation", "co",
    "company", "group", "holding", "holdings", "international",
    "est", "establishment", "trading", "services",
]

_SUFFIX_RE_AR = re.compile(
    r"\b(" + "|".join(re.escape(s) for s in _AR_COMPANY_SUFFIXES) + r")\b",
    re.UNICODE,
)
_SUFFIX_RE_EN = re.compile(
    r"\b(" + "|".join(re.escape(s) for s in _EN_COMPANY_SUFFIXES) + r")\b",
    re.IGNORECASE,
)


def normalize_company_name(name: str, lang: str = "en") -> str:
    """
    Normalize a company name for deduplication:
    - Lowercase + strip whitespace
    - Remove legal suffixes (LLC, Ltd, شركة, etc.)
    - Normalize Arabic text if Arabic
    """
    if not name:
        return ""
    name = name.strip()
    if lang == "ar":
        name = normalize_arabic_text(name)
        name = _SUFFIX_RE_AR.sub("", name)
    else:
        name = name.lower()
        name = _SUFFIX_RE_EN.sub("", name)
    # Remove punctuation
    name = re.sub(r"[^\w\s\u0600-\u06FF]", " ", name)
    name = " ".join(name.split())
    return name


def detect_language(text: str) -> str:
    """Return 'ar' if text contains Arabic characters, else 'en'."""
    if not text:
        return "en"
    arabic_chars = sum(1 for c in text if "\u0600" <= c <= "\u06FF")
    return "ar" if arabic_chars > len(text) * 0.2 else "en"


# ─────────────────────────── Arabic Name Extraction ──────────────────────────

# Arabic name pattern: sequence of Arabic words (2-5 tokens)
_AR_NAME_RE = re.compile(
    r"(?:[\u0621-\u064A\u0660-\u0669]{2,}\s+){1,4}[\u0621-\u064A\u0660-\u0669]{2,}"
)


def extract_arabic_names(text: str) -> list[str]:
    """Extract potential Arabic person/company names from free text."""
    if not text:
        return []
    return [m.strip() for m in _AR_NAME_RE.findall(text)]


# ─────────────────────────── Search Query Helpers ────────────────────────────

def make_bilingual_queries(term_en: str, term_ar: str | None = None) -> list[str]:
    """Return both English and Arabic variants for a search term."""
    queries = [term_en]
    if term_ar:
        queries.append(term_ar)
    return queries


# Commonly used Arabic business terms for Gulf searches
AR_BUSINESS_TERMS = {
    "restaurant": "مطعم",
    "cafe": "مقهى",
    "hotel": "فندق",
    "real_estate": "عقار",
    "clinic": "عيادة",
    "hospital": "مستشفى",
    "school": "مدرسة",
    "company": "شركة",
    "group": "مجموعة",
    "establishment": "مؤسسة",
    "trading": "تجارة",
    "technology": "تقنية",
    "software": "برمجيات",
    "marketing": "تسويق",
    "logistics": "لوجستيات",
    "construction": "مقاولات",
    "consulting": "استشارات",
    "education": "تعليم",
    "healthcare": "رعاية صحية",
    "ecommerce": "تجارة إلكترونية",
}


def get_arabic_term(english_term: str) -> str | None:
    """Look up an Arabic business term by English key."""
    return AR_BUSINESS_TERMS.get(english_term.lower().replace(" ", "_"))


def normalize_phone_display(phone: str) -> str:
    """
    Normalize phone for display (doesn't do E.164 — use phonenumbers library for that).
    Strips spaces/dashes, normalizes Arabic digits.
    """
    if not phone:
        return phone
    phone = normalize_arabic_digits(phone)
    phone = re.sub(r"[\s\-\.\(\)]", "", phone)
    return phone
