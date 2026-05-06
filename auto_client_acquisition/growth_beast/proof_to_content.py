"""Bridge proof events to content ideas (approval-gated)."""
from __future__ import annotations

from typing import Any


def proof_to_snippets(proof_themes: list[str]) -> dict[str, Any]:
    themes = proof_themes[:3] if proof_themes else ["delivery_quality"]
    return {
        "schema_version": 1,
        "snippet_ideas_ar": [
            f"درس مختصر: كيف تعاملنا مع '{t}' بدون ادعاء أرقام غير مؤكدة" for t in themes
        ],
        "approval_required": True,
        "no_logo_without_consent": True,
    }
