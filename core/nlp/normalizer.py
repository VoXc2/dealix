"""
Arabic text normalizer — pre-processing before any NLP task.
مُوحِّد النص العربي — معالجة مسبقة قبل أي مهمة NLP.

Operations (applied in order):
  1. Unicode normalisation (NFC)
  2. Alef variants → bare alef (أ/إ/آ → ا)
  3. Teh marbuta variants → ة
  4. Remove tashkeel / harakat (short vowels: ً ٌ ٍ َ ُ ِ ّ ْ)
  5. Remove tatweel (ـ)
  6. Normalise Hamza above/below Alef
  7. Collapse repeated characters (لللللبنان → للبنان, limit 2)
  8. Strip non-Arabic / non-alphanumeric noise (configurable)
  9. Normalise whitespace

Usage:
    from core.nlp.normalizer import normalize_arabic
    clean = normalize_arabic("أَلسَّلامُ عَليكم!")
    # → "السلام عليكم"
"""

from __future__ import annotations

import re
import unicodedata


# ── Character maps ────────────────────────────────────────────────

# All Alef variants → bare Alef
_ALEF_MAP = str.maketrans(
    "\u0623\u0625\u0622\u0671\u0670\u0627",  # أ إ آ ٱ ٰ ا
    "\u0627\u0627\u0627\u0627\u0627\u0627",
)

# Arabic-Indic digits → ASCII digits
_ARABIC_INDIC_DIGITS = str.maketrans(
    "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669",
    "0123456789",
)

# Tashkeel (harakat) characters to strip
_TASHKEEL = re.compile(
    r"[\u064b-\u065f\u0670\u0640]"  # fathatan..hamza above, tatweel
)

# Alef Maqsura (ى) → Yaa (ي) — common normalisation for Saudi dialect
_ALEF_MAQSURA = str.maketrans("\u0649", "\u064a")

# Teh Marbuta without dots → with dots (optional)
_TEH_MARBUTA = str.maketrans("\u0647", "\u0629")  # only at end of word — applied carefully below

# Repeated characters (e.g. كككثير → كثير) — max 2 repetitions
_REPEAT_RE = re.compile(r"(.)\1{2,}")


def normalize_arabic(
    text: str,
    *,
    remove_tashkeel: bool = True,
    normalize_alef: bool = True,
    normalize_alef_maqsura: bool = True,
    normalize_digits: bool = True,
    collapse_repeats: bool = True,
    remove_punctuation: bool = False,
    lowercase_latin: bool = True,
) -> str:
    """
    Normalize an Arabic string.
    توحيد النص العربي.

    Parameters
    ----------
    text : str
        Raw input string.
    remove_tashkeel : bool
        Strip harakat / short vowel diacritics (default: True).
    normalize_alef : bool
        Unify all Alef variants to bare Alef (default: True).
    normalize_alef_maqsura : bool
        Map ى → ي (default: True).
    normalize_digits : bool
        Convert Arabic-Indic digits to ASCII (default: True).
    collapse_repeats : bool
        Collapse 3+ repeated chars to 2 (default: True).
    remove_punctuation : bool
        Remove all non-alphanumeric, non-Arabic chars (default: False).
    lowercase_latin : bool
        Lowercase any Latin characters in the string (default: True).

    Returns
    -------
    str
        Normalised text.
    """
    if not text:
        return text

    # 1. Unicode NFC
    text = unicodedata.normalize("NFC", text)

    # 2. Alef variants
    if normalize_alef:
        text = text.translate(_ALEF_MAP)

    # 3. Remove tashkeel + tatweel
    if remove_tashkeel:
        text = _TASHKEEL.sub("", text)

    # 4. Alef Maqsura
    if normalize_alef_maqsura:
        text = text.translate(_ALEF_MAQSURA)

    # 5. Arabic-Indic digits
    if normalize_digits:
        text = text.translate(_ARABIC_INDIC_DIGITS)

    # 6. Collapse repeated characters
    if collapse_repeats:
        text = _REPEAT_RE.sub(r"\1\1", text)

    # 7. Remove punctuation (keep Arabic + ASCII alphanumeric + spaces)
    if remove_punctuation:
        text = re.sub(r"[^\w\s\u0600-\u06ff]", " ", text)

    # 8. Lowercase Latin
    if lowercase_latin:
        text = text.lower()

    # 9. Normalise whitespace
    text = " ".join(text.split())

    return text


def tokenize_arabic(text: str, *, normalize: bool = True) -> list[str]:
    """
    Simple whitespace tokenizer for Arabic (no stemming).
    مُجزّئ بسيط للنص العربي.

    For production use: integrate CAMeL Tools or Farasa morphological analyzer.
    """
    if normalize:
        text = normalize_arabic(text)
    return text.split()


def is_arabic(text: str, *, threshold: float = 0.5) -> bool:
    """
    Return True if the majority of alphabetic characters are Arabic.
    يُعيد True إذا كانت غالبية الأحرف عربية.
    """
    if not text:
        return False
    arabic_count = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count == 0:
        return False
    return (arabic_count / alpha_count) >= threshold
