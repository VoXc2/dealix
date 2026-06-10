"""Per-source readiness check."""
from __future__ import annotations

import os
from typing import Any

_SUPPORTED_SOURCES = (
    "whatsapp", "form", "csv", "warm_intro",
    "google_places", "referral", "api", "manual",
)


def source_health() -> dict[str, Any]:
    """Returns readiness per source."""
    sources = []
    for src in _SUPPORTED_SOURCES:
        sources.append({
            "source": src,
            "ready": _is_source_ready(src),
            "blocker": _source_blocker(src),
        })
    return {
        "sources": sources,
        "ready_count": sum(1 for s in sources if s["ready"]),
        "total": len(sources),
    }


def _is_source_ready(source: str) -> bool:
    if source == "manual":
        return True  # Always available
    if source == "warm_intro":
        return True  # Always available
    if source == "form":
        return True  # /diagnostic.html always works
    if source == "csv":
        return True  # CSV upload manual
    if source == "whatsapp":
        # Needs Meta WhatsApp credentials
        return bool(os.environ.get("META_WHATSAPP_TOKEN"))
    if source == "google_places":
        return bool(os.environ.get("GOOGLE_PLACES_API_KEY"))
    if source == "api":
        return True  # `/api/v1/leadops/run` always callable
    return source == "referral"


def _source_blocker(source: str) -> str | None:
    if source == "whatsapp" and not os.environ.get("META_WHATSAPP_TOKEN"):
        return "META_WHATSAPP_TOKEN env var not set"
    if source == "google_places" and not os.environ.get("GOOGLE_PLACES_API_KEY"):
        return "GOOGLE_PLACES_API_KEY env var not set"
    return None
