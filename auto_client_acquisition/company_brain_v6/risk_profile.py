"""Risk profile flags for a customer brain — pure local heuristics."""
from __future__ import annotations

from typing import Any


def compute_risk_profile(brain: Any) -> dict[str, Any]:
    """Return a dict of risk flags + supporting reasons."""
    pain_points = [str(p).lower() for p in (getattr(brain, "pain_points", []) or [])]
    blocked = [str(c).lower() for c in (getattr(brain, "blocked_channels", []) or [])]
    current = [str(c).lower() for c in (getattr(brain, "current_channels", []) or [])]

    pain_blob = " ".join(pain_points)

    high_pdpl_risk = any(
        token in pain_blob
        for token in ("spam", "pdpl", "consent", "موافقة", "إزعاج")
    )
    high_brand_risk = (
        "cold_whatsapp" in blocked
        or "cold_whatsapp" in current
        or "linkedin_automation" in current
        or "scrape_web" in current
    )
    has_no_channels = not (getattr(brain, "current_channels", []) or [])
    weak_growth_signal = not (getattr(brain, "growth_goal", "") or "").strip()

    return {
        "high_pdpl_risk": bool(high_pdpl_risk),
        "high_brand_risk": bool(high_brand_risk),
        "has_no_channels": bool(has_no_channels),
        "weak_growth_signal": bool(weak_growth_signal),
    }
