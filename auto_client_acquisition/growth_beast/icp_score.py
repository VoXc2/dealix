"""Simple ICP scoring from a profile blob."""
from __future__ import annotations

from typing import Any


def score_icp(profile: dict[str, Any]) -> dict[str, Any]:
    sector = str(profile.get("sector") or "").lower()
    score = 55
    reasons: list[str] = []
    if "agency" in sector or "وكالة" in sector:
        score += 20
        reasons.append("agency_wedge")
    if profile.get("ideal_customer"):
        score += 10
        reasons.append("icp_text_present")
    score = min(100, score)
    return {"schema_version": 1, "icp_score": score, "reasons": reasons}
