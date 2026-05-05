"""Extract top decisions from the daily growth loop output."""
from __future__ import annotations

from typing import Any


def _coerce_titles(d: dict[str, Any]) -> tuple[str, str]:
    title_ar = (
        d.get("title_ar")
        or d.get("name_ar")
        or d.get("title")
        or d.get("description")
        or ""
    )
    title_en = (
        d.get("title_en")
        or d.get("name_en")
        or d.get("title")
        or d.get("description")
        or ""
    )
    return str(title_ar), str(title_en)


def _coerce_recommendations(d: dict[str, Any]) -> tuple[str, str]:
    rec_ar = (
        d.get("recommendation_ar")
        or d.get("rationale_ar")
        or d.get("rationale")
        or d.get("next_action_ar")
        or ""
    )
    rec_en = (
        d.get("recommendation_en")
        or d.get("rationale_en")
        or d.get("rationale")
        or d.get("next_action_en")
        or ""
    )
    return str(rec_ar), str(rec_en)


def decision_summary(loop: dict[str, Any] | None, *, limit: int = 3) -> list[dict[str, str]]:
    """Return a clean, bilingual list of top decisions.

    Founder cannot process more than ~5 decisions a week; we cap at
    ``limit`` (default 3). Pure formatter — no I/O.
    """
    if not isinstance(loop, dict):
        return []

    raw = loop.get("decisions") or []
    out: list[dict[str, str]] = []
    for item in raw[: max(0, limit)]:
        if isinstance(item, dict):
            title_ar, title_en = _coerce_titles(item)
            rec_ar, rec_en = _coerce_recommendations(item)
        elif isinstance(item, str):
            title_ar = title_en = item
            rec_ar = rec_en = ""
        else:
            continue
        if not (title_ar or title_en):
            continue
        out.append({
            "title_ar": title_ar,
            "title_en": title_en,
            "recommendation_ar": rec_ar,
            "recommendation_en": rec_en,
        })
    return out
