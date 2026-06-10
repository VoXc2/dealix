"""Match lead text to objection_engine_registry drafts (deterministic)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_REGISTRY = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "commercial"
    / "operations"
    / "objection_engine_registry.yaml"
)


@lru_cache(maxsize=1)
def load_objection_registry() -> list[dict[str, Any]]:
    if not _REGISTRY.is_file():
        return []
    data = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8")) or {}
    items = data.get("objections") or []
    return [x for x in items if isinstance(x, dict)]


def match_objections(text: str, *, limit: int = 3) -> list[dict[str, Any]]:
    """Return objection entries whose labels appear in text (AR/EN)."""
    blob = (text or "").lower()
    hits: list[dict[str, Any]] = []
    for obj in load_objection_registry():
        labels = list(obj.get("labels_ar") or []) + list(obj.get("labels_en") or [])
        for label in labels:
            lab = str(label).strip().lower()
            if lab and lab in blob:
                hits.append(
                    {
                        "id": obj.get("id"),
                        "classify": obj.get("classify"),
                        "response_draft_ar": (obj.get("response_draft_ar") or "").strip(),
                        "matched_label": label,
                    },
                )
                break
    return hits[:limit]
