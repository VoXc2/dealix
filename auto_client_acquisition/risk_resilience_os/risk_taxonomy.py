"""Risk Taxonomy — 12 doctrine categories."""

from __future__ import annotations

from enum import Enum


class RiskCategory(str, Enum):
    DATA = "data_risk"
    PRIVACY = "privacy_risk"
    AI_OUTPUT = "ai_output_risk"
    AGENT_AUTONOMY = "agent_autonomy_risk"
    CHANNEL = "channel_risk"
    CLAIM = "claim_risk"
    CLIENT = "client_risk"
    DELIVERY = "delivery_risk"
    PARTNER = "partner_risk"
    FINANCIAL = "financial_risk"
    MARKET = "market_risk"
    STRATEGIC_DRIFT = "strategic_drift_risk"


RISK_CATEGORIES: tuple[RiskCategory, ...] = tuple(RiskCategory)
