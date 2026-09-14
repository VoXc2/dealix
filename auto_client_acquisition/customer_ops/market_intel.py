"""Market-intelligence support: official/public sources + bounded adapters.

No scraping shortcut, no relationship inference. Thin read-only wrapper
over dealix.commercial.market_intelligence + intelligence modules.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def _stamp() -> str:
    return datetime.now(UTC).isoformat()


def official_sector_brief(sector: str) -> dict[str, Any]:
    """Curated public-research brief for a sector (read-only, with provenance)."""
    sector_key = (sector or "").strip().lower() or "technology_saas"
    brief_ar = ""
    brief_en = ""
    provenance: list[str] = ["dealix.commercial.market_intelligence:public_research"]
    try:
        from dealix.commercial.market_intelligence import MarketIntelligenceEngine

        engine = MarketIntelligenceEngine()
        data = engine.get_why_now_brief(sector_key)
        if isinstance(data, dict):
            brief_ar = str(data.get("ar", ""))
            brief_en = str(data.get("en", ""))
    except Exception:
        brief_ar, brief_en = "", ""
    if not brief_ar and not brief_en:
        # Fail-closed: no invented stats; caller must HOLD/ASK.
        return {
            "sector": sector_key,
            "brief_ar": "",
            "brief_en": "",
            "provenance": provenance,
            "current_only": True,
            "retrieved_at": _stamp(),
            "insufficient_evidence": True,
        }
    return {
        "sector": sector_key,
        "brief_ar": brief_ar,
        "brief_en": brief_en,
        "provenance": provenance,
        "current_only": True,
        "retrieved_at": _stamp(),
        "insufficient_evidence": False,
    }


def watch_signals(*, sector: str | None = None, urgency: str | None = None) -> dict[str, Any]:
    """Bounded watcher over curated signals (no scraping, aggregate only)."""
    try:
        from dealix.commercial.market_intelligence import MarketIntelligenceEngine

        engine = MarketIntelligenceEngine()
        signals = engine.get_all_signals(urgency_filter=urgency, sector_filter=sector)
        items = [s.model_dump() if hasattr(s, "model_dump") else dict(s) for s in signals]
    except Exception:
        items = []
    return {
        "sector": sector,
        "urgency": urgency,
        "count": len(items),
        "signals": items[:25],
        "provenance": ["dealix.commercial.market_intelligence:public_research"],
        "note": "aggregate sector signals only — never named buyer intent",
        "retrieved_at": _stamp(),
    }
