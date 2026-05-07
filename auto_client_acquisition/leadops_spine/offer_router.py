"""Offer router — picks the channel + medium for a given lead.

Reads channels preference from CustomerBrainSnapshot if available;
falls back to a sector-based default. Never auto-sends — only
recommends; the actual send goes through approval_center.

Default sector → channel map matches existing
market_intelligence.opportunity_feed._DEFAULT_CHANNEL_BY_SECTOR.
"""
from __future__ import annotations

from typing import Any, Literal

Channel = Literal["whatsapp", "email", "linkedin", "phone", "dashboard"]
Medium = Literal["text", "voice_note", "pdf", "form_link"]

_DEFAULT_CHANNEL_BY_SECTOR: dict[str, Channel] = {
    "real_estate": "whatsapp",
    "clinics": "whatsapp",
    "logistics": "email",
    "hospitality": "email",
    "restaurants": "whatsapp",
    "training": "linkedin",
    "agencies": "email",
    "construction": "email",
}


def route_offer(
    *,
    sector: str | None,
    score: dict[str, Any] | None = None,
    brain_channels: list[str] | None = None,
) -> dict[str, Any]:
    """Return {'channel', 'medium', 'reason'}.

    Priority:
      1. CustomerBrainSnapshot.channels (if known)
      2. Sector default
      3. 'dashboard' (safe fallback — no external send)
    """
    score = score or {}
    fit = float(score.get("fit", 0))

    if brain_channels:
        chosen = brain_channels[0]
        reason = "brain.channels[0]"
    elif sector and sector in _DEFAULT_CHANNEL_BY_SECTOR:
        chosen = _DEFAULT_CHANNEL_BY_SECTOR[sector]
        reason = f"sector_default:{sector}"
    else:
        chosen = "dashboard"
        reason = "no_channel_known_default_to_dashboard"

    medium: Medium = "voice_note" if chosen == "whatsapp" and fit >= 0.7 else "text"

    return {
        "channel": chosen,
        "medium": medium,
        "reason": reason,
        "approval_required_before_send": True,
    }
