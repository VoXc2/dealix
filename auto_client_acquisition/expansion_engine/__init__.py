"""Wave 12.5 §33.2.5 — Expansion Engine v2.

Composes proof history + customer health into an Expansion Readiness
Score that drives next-best-offer decisions.

Hard rule (Article 8): expansion offers are gated by proof.
- No proof → no upsell (returns ``not_ready``)
- Low proof level → suggest_only (founder reviews)
- Customer-approved proof (L3+) → can recommend offers
- Public proof (L4+) → can recommend public-facing campaigns
"""
from __future__ import annotations

from auto_client_acquisition.expansion_engine.readiness_score import (
    ExpansionReadinessScore,
    NextBestOffer,
    compute_readiness_score,
    recommend_next_offer,
)

__all__ = [
    "ExpansionReadinessScore",
    "NextBestOffer",
    "compute_readiness_score",
    "recommend_next_offer",
]
