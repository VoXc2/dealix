"""
Card Priority Ranker — ranks decision cards by composite score.

Pure function: given a list of cards (each with type/risk_level/proof_impact),
returns a sorted copy with top-N cards first.

Score formula (matches user spec):
  priority_score =
       urgency       * 0.25
     + revenue_impact* 0.25
     + risk_level    * 0.20
     + stale_time    * 0.15
     + proof_impact  * 0.15
"""

from __future__ import annotations

from typing import Any


_RISK_WEIGHT = {"low": 0.2, "medium": 0.6, "high": 1.0}

# Type → urgency + revenue weight
_TYPE_PROFILE: dict[str, dict[str, float]] = {
    "deal_followup":      {"urgency": 0.9, "revenue_impact": 0.9},
    "negotiation":        {"urgency": 0.7, "revenue_impact": 0.85},
    "close_plan":         {"urgency": 0.7, "revenue_impact": 0.95},
    "executive_decision": {"urgency": 0.85, "revenue_impact": 0.95},
    "proof_review":       {"urgency": 0.6, "revenue_impact": 0.5},
    "support_p0":         {"urgency": 1.0, "revenue_impact": 0.4},
    "proof_delay":        {"urgency": 0.6, "revenue_impact": 0.6},
    "upgrade_opportunity":{"urgency": 0.5, "revenue_impact": 0.85},
    "agency_action":      {"urgency": 0.5, "revenue_impact": 0.7},
    "invoice_ready":      {"urgency": 0.7, "revenue_impact": 0.8},
    "partner_commission": {"urgency": 0.4, "revenue_impact": 0.5},
    "compliance_alert":   {"urgency": 0.95, "revenue_impact": 0.3},
    "gate_alert":         {"urgency": 0.95, "revenue_impact": 0.3},
    "target_segment":     {"urgency": 0.5, "revenue_impact": 0.4},
    "channel_health":     {"urgency": 0.4, "revenue_impact": 0.3},
    "message_experiment": {"urgency": 0.4, "revenue_impact": 0.4},
    "funnel_focus":       {"urgency": 0.5, "revenue_impact": 0.6},
    "partner_opportunity":{"urgency": 0.5, "revenue_impact": 0.7},
}

_DEFAULT_PROFILE = {"urgency": 0.4, "revenue_impact": 0.4}


def score(card: dict[str, Any]) -> float:
    profile = _TYPE_PROFILE.get(card.get("type", ""), _DEFAULT_PROFILE)
    urgency = profile["urgency"]
    rev = profile["revenue_impact"]
    risk = _RISK_WEIGHT.get(card.get("risk_level", "low"), 0.2)
    stale = float(card.get("stale_score", 0.0))
    proof = float(card.get("proof_score", 1.0)) * (1.0 if card.get("proof_impact") else 0.0)
    if not card.get("proof_impact"):
        proof = 0.0
    s = (
        urgency * 0.25
        + rev    * 0.25
        + risk   * 0.20
        + stale  * 0.15
        + proof  * 0.15
    )
    return round(s, 4)


def rank(cards: list[dict[str, Any]], *, top_n: int = 3) -> list[dict[str, Any]]:
    if not cards:
        return []
    enriched = []
    for c in cards:
        enriched.append({**c, "priority_score": score(c)})
    enriched.sort(key=lambda x: x["priority_score"], reverse=True)
    # Filter out cards without next-action / owner / proof_impact (per spec)
    cleaned = [c for c in enriched if c.get("recommended_action_ar") and c.get("proof_impact")]
    return cleaned[:top_n]
