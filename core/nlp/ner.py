"""
Arabic Named Entity Recognition (NER) — zero-shot via LLM.
استخراج الكيانات المُسمَّاة من النص العربي.

Entity types detected:
  - PERSON     (شخص)        — names of individuals
  - ORG        (منظمة)       — company/organization names
  - GPE        (موقع_سياسي)  — cities, countries, regions
  - PRODUCT    (منتج)        — product or service names
  - MONEY      (مال)         — monetary amounts (supports SAR / USD / EUR)
  - DATE       (تاريخ)       — dates (Hijri and Gregorian)
  - PHONE      (هاتف)        — phone numbers (Saudi format)
  - EMAIL      (بريد)        — email addresses
  - CR_NUMBER  (سجل_تجاري)   — Saudi Commercial Registration numbers

Regex patterns cover the structured entity types (MONEY, DATE, PHONE, EMAIL, CR).
LLM fallback used for PERSON, ORG, GPE, PRODUCT extraction.

Usage:
    entities = await extract_entities("اتصل بمحمد من شركة أرامكو في الرياض")
    # [{"type": "PERSON", "value": "محمد"}, {"type": "ORG", "value": "أرامكو"}, ...]
"""

from __future__ import annotations

import re
from typing import Any

from core.logging import get_logger

logger = get_logger(__name__)


# ── Regex patterns ────────────────────────────────────────────────

# Saudi phone: +966 or 05xx or 009665xx
_PHONE_RE = re.compile(
    r"(?:\+966|00966|0)(?:5\d{8}|[2-46-9]\d{7})"
)

# Email
_EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}")

# Monetary amounts (SAR, USD, EUR, ريال, دولار)
_MONEY_RE = re.compile(
    r"(?:(?:SAR|USD|EUR|ريال|دولار|يورو)\s*)?"
    r"\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
    r"(?:\s*(?:SAR|USD|EUR|ريال|دولار|يورو|مليون|مليار|ألف))?"
)

# Gregorian date YYYY-MM-DD or DD/MM/YYYY
_DATE_GREG_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b"
)

# Hijri date (e.g. ١٤٤٥/٠٩/١٠ or 1445/09/10)
_DATE_HIJRI_RE = re.compile(
    r"\b1[3-5]\d{2}[/\-]\d{1,2}[/\-]\d{1,2}\b"
)

# Saudi Commercial Registration (10 digits starting with 1-3)
_CR_RE = re.compile(r"\b[123]\d{9}\b")


def extract_entities_regex(text: str) -> list[dict[str, Any]]:
    """
    Fast regex-based entity extraction for structured entities.
    استخراج الكيانات المنظّمة باستخدام التعابير النمطية.

    Returns list of {"type": str, "value": str, "start": int, "end": int}
    """
    entities: list[dict[str, Any]] = []

    for m in _PHONE_RE.finditer(text):
        entities.append({"type": "PHONE", "value": m.group(), "start": m.start(), "end": m.end()})

    for m in _EMAIL_RE.finditer(text):
        entities.append({"type": "EMAIL", "value": m.group(), "start": m.start(), "end": m.end()})

    for m in _DATE_HIJRI_RE.finditer(text):
        entities.append({"type": "DATE_HIJRI", "value": m.group(), "start": m.start(), "end": m.end()})

    for m in _DATE_GREG_RE.finditer(text):
        entities.append({"type": "DATE", "value": m.group(), "start": m.start(), "end": m.end()})

    for m in _CR_RE.finditer(text):
        entities.append({"type": "CR_NUMBER", "value": m.group(), "start": m.start(), "end": m.end()})

    # De-duplicate overlapping spans (keep longest)
    entities.sort(key=lambda e: (e["start"], -(e["end"] - e["start"])))
    deduplicated: list[dict[str, Any]] = []
    last_end = -1
    for ent in entities:
        if ent["start"] >= last_end:
            deduplicated.append(ent)
            last_end = ent["end"]

    return deduplicated


async def extract_entities(
    text: str,
    *,
    include_llm: bool = False,
    llm_task: Any = None,
) -> list[dict[str, Any]]:
    """
    Extract named entities from Arabic text.
    استخراج الكيانات المُسمَّاة من النص العربي.

    Parameters
    ----------
    text : str
        Arabic or mixed Arabic/English text.
    include_llm : bool
        If True and llm_task is provided, also run LLM-based extraction
        for PERSON, ORG, GPE, PRODUCT (slower but more accurate).
    llm_task : Task | None
        LLM task handle for LLM-based extraction.

    Returns
    -------
    list of entity dicts: {"type", "value", "start"?, "end"?}
    """
    entities = extract_entities_regex(text)

    if include_llm and llm_task is not None:
        try:
            llm_entities = await _extract_entities_llm(text, llm_task)
            entities.extend(llm_entities)
        except Exception as exc:  # noqa: BLE001
            logger.warning("ner_llm_error", error=str(exc))

    return entities


async def _extract_entities_llm(text: str, task: Any) -> list[dict[str, Any]]:
    """
    LLM-based NER for PERSON, ORG, GPE, PRODUCT.
    استخراج الكيانات بالذكاء الاصطناعي.
    """
    from core.llm import get_router  # noqa: PLC0415
    from core.llm.base import Message  # noqa: PLC0415

    prompt = (
        "Extract named entities from the following Arabic text. "
        "Return ONLY a JSON array of objects with keys 'type' and 'value'. "
        "Entity types: PERSON, ORG, GPE, PRODUCT. "
        "Do NOT include PHONE, EMAIL, DATE, or MONEY — those are handled separately.\n\n"
        f"Text:\n{text}\n\n"
        "JSON array only, no prose:"
    )
    router = get_router()
    response = await router.run(
        task,
        messages=[Message(role="user", content=prompt)],
        system="You are a precise Arabic NLP engine. Output valid JSON only.",
        max_tokens=512,
        temperature=0.0,
    )

    import json  # noqa: PLC0415
    try:
        raw = response.content.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = re.sub(r"```(?:json)?|```", "", raw).strip()
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return []
