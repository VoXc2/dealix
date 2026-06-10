"""Decision labels for intelligence layer — taxonomy only (no side effects)."""

from __future__ import annotations

from enum import StrEnum


class IntelligenceDecision(StrEnum):
    """Types of recurring operating decisions."""

    SELL_MORE = "sell_more"
    RAISE_PRICE = "raise_price"
    STOP_SELLING = "stop_selling"
    PRODUCTIZE = "productize"
    CREATE_PLAYBOOK = "create_playbook"
    OFFER_RETAINER = "offer_retainer"
    CREATE_PARTNER_OFFER = "create_partner_offer"
    PROMOTE_TO_BUSINESS_UNIT = "promote_to_business_unit"
    PROMOTE_TO_VENTURE_CANDIDATE = "promote_to_venture_candidate"
    KILL_EXPERIMENT = "kill_experiment"
