"""Select proof-like themes safe for marketing exploration."""
from __future__ import annotations

from typing import Any


def select_proof_themes(raw_events: list[dict[str, Any]]) -> list[str]:
    themes: list[str] = []
    for ev in raw_events:
        et = str(ev.get("event_type") or "")
        if "delivered" in et or "diagnostic" in et:
            themes.append(et)
    return themes[:5] or ["internal_proof_placeholder"]
