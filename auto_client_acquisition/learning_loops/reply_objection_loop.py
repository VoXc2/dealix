"""Learning loop (a) — classified replies to a deduplicated objection library.

Reads the output of the reply classifier
(``auto_client_acquisition.email.reply_classifier``) and aggregates
objection-type replies into a deduplicated library keyed by objection
category, each entry carrying a count and representative sample text.

Pure-function core. NO LLM. NO I/O. The result is a suggestion set —
nothing is auto-applied.
"""
from __future__ import annotations

import json
import os
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Reply-classifier categories that represent a genuine objection.
_OBJECTION_CATEGORIES: dict[str, dict[str, str]] = {
    "objection_budget": {
        "en": "Budget / price objection",
        "ar": "اعتراض على الميزانية أو السعر",
    },
    "objection_ai": {
        "en": "Distrust of AI / wants a human",
        "ar": "عدم الثقة بالذكاء الاصطناعي / يريد إنساناً",
    },
    "objection_privacy": {
        "en": "Privacy / PDPL / data residency concern",
        "ar": "قلق بشأن الخصوصية أو PDPL أو موقع البيانات",
    },
    "already_has_crm": {
        "en": "Already has a CRM / vendor",
        "ar": "لديه نظام CRM أو مزوّد بالفعل",
    },
    "not_now": {
        "en": "Timing objection — defer",
        "ar": "اعتراض توقيت — تأجيل",
    },
}


@dataclass
class ObjectionLibraryEntry:
    """One deduplicated objection in the learned library."""

    category: str
    label_en: str
    label_ar: str
    count: int
    sample_texts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "label_en": self.label_en,
            "label_ar": self.label_ar,
            "count": self.count,
            "sample_texts": self.sample_texts,
        }


def _category_of(record: Any) -> str:
    """Extract the classifier category from a record (dataclass or dict)."""
    if isinstance(record, dict):
        return str(record.get("category") or "")
    return str(getattr(record, "category", "") or "")


def _text_of(record: Any) -> str:
    """Best-effort extraction of the original reply text from a record."""
    if isinstance(record, dict):
        return str(
            record.get("original_text")
            or record.get("text")
            or record.get("reply_text")
            or ""
        )
    for attr in ("original_text", "text", "reply_text"):
        val = getattr(record, attr, None)
        if val:
            return str(val)
    return ""


def build_objection_library(
    classified_replies: Iterable[Any],
    *,
    max_samples: int = 3,
) -> list[ObjectionLibraryEntry]:
    """Aggregate classified replies into a deduplicated objection library.

    ``classified_replies`` is an iterable of reply-classifier outputs —
    either ``ReplyClassification`` instances or their ``to_dict()``
    forms. Non-objection categories are ignored. Entries are returned
    sorted by descending count.
    """
    buckets: dict[str, ObjectionLibraryEntry] = {}
    for record in classified_replies:
        category = _category_of(record)
        meta = _OBJECTION_CATEGORIES.get(category)
        if meta is None:
            continue
        entry = buckets.get(category)
        if entry is None:
            entry = ObjectionLibraryEntry(
                category=category,
                label_en=meta["en"],
                label_ar=meta["ar"],
                count=0,
            )
            buckets[category] = entry
        entry.count += 1
        text = _text_of(record).strip()
        # Deduplicate sample text — distinct phrasings only, bounded.
        if text and text not in entry.sample_texts and len(entry.sample_texts) < max_samples:
            entry.sample_texts.append(text[:280])

    return sorted(buckets.values(), key=lambda e: (-e.count, e.category))


def _classified_replies_path() -> Path:
    """Resolve the classified-replies JSONL store (env override aware)."""
    raw = os.environ.get("DEALIX_CLASSIFIED_REPLIES_PATH")
    if raw:
        return Path(raw)
    return Path("data") / "classified_replies.jsonl"


def load_classified_replies() -> list[dict[str, Any]]:
    """Read persisted classified replies from the JSONL store.

    Returns an empty list when the store does not exist yet — the loop
    then yields an empty objection library rather than crashing.
    """
    path = _classified_replies_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


__all__ = [
    "ObjectionLibraryEntry",
    "build_objection_library",
    "load_classified_replies",
]
