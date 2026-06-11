"""Normalizer — convert any raw record to the canonical lead schema."""
from __future__ import annotations

import datetime as dt
from typing import Any


def normalize_lead(raw: dict, source_type: str, source_note: str) -> dict:
    return {
        "id": raw.get("id") or f"lead-{dt.date.today().isoformat()}-{hash(raw.get('name', '')) % 10000}",
        "name": raw.get("name", "Unknown"),
        "segment": raw.get("segment", "b2b_services"),
        "city": raw.get("city", ""),
        "sourceType": source_type,
        "sourceNote": source_note,
        "visibleSignal": raw.get("visibleSignal", raw.get("signal", "")),
        "weaknessHypothesis": raw.get("weaknessHypothesis", ""),
        "recommendedOffer": raw.get("recommendedOffer", "diagnostic_sprint"),
        "score": int(raw.get("score", 0) or 0),
        "stage": raw.get("stage", "new"),
        "owner": raw.get("owner", "Founder"),
        "reviewStatus": "not_started",
        "demo": bool(raw.get("demo", True)),
        "createdAt": dt.date.today().isoformat(),
    }
