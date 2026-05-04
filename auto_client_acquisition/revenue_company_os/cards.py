"""
Decision Card schema + role/type taxonomy for the Command Center.

A card is the smallest unit of "next best revenue decision" that Dealix
emits to a human operator. Each card is renderable and reasonable in
isolation: it carries its own why_now, recommended_action, risk, proof
impact, and ≤3 buttons.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Role(str, Enum):
    CEO = "ceo"
    SALES = "sales"
    GROWTH = "growth"
    SERVICE = "service"
    SUPPORT = "support"
    AGENCY = "agency"


class CardType(str, Enum):
    CEO_DAILY = "ceo_daily"
    OPPORTUNITY = "opportunity"
    PARTNER = "partner"
    DEAL_FOLLOWUP = "deal_followup"
    NEGOTIATION = "negotiation"
    PROOF = "proof"
    SUPPORT = "support"
    RISK = "risk"
    APPROVAL = "approval"
    CUSTOMER_SUCCESS = "customer_success"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Maximum number of buttons per card — enforced by the schema validator.
# Matches the design system rule (.dx-card__buttons in landing/assets/css/cards.css).
MAX_BUTTONS = 3


@dataclass
class CardButton:
    label_ar: str
    action: str  # "prepare" | "approve" | "details" | "skip" | "dismiss" | ...
    primary: bool = False


_RISK_TO_BADGE = {
    RiskLevel.HIGH: "P1",
    RiskLevel.MEDIUM: "P2",
    RiskLevel.LOW: "P3",
}


@dataclass
class Card:
    id: str
    type: CardType
    role: Role
    title_ar: str
    why_now_ar: str
    recommended_action_ar: str
    proof_impact: list[str] = field(default_factory=list)
    risk: RiskLevel = RiskLevel.LOW
    risk_note_ar: str | None = None
    risk_badge: str | None = None  # P0|P1|P2|P3 — auto-derived from risk if absent
    buttons: list[CardButton] = field(default_factory=list)
    owner: str | None = None
    expires_at: datetime | None = None
    meta: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if len(self.buttons) > MAX_BUTTONS:
            raise ValueError(
                f"card {self.id} has {len(self.buttons)} buttons; max is {MAX_BUTTONS}"
            )
        if not self.title_ar:
            raise ValueError(f"card {self.id} missing Arabic title")
        if not self.why_now_ar:
            raise ValueError(f"card {self.id} missing why_now")
        if not self.risk_badge:
            self.risk_badge = _RISK_TO_BADGE.get(self.risk, "P3")
        if self.risk_badge not in ("P0", "P1", "P2", "P3"):
            raise ValueError(
                f"card {self.id} has invalid risk_badge {self.risk_badge!r}; must be P0|P1|P2|P3"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "role": self.role.value,
            "title_ar": self.title_ar,
            "why_now_ar": self.why_now_ar,
            "recommended_action_ar": self.recommended_action_ar,
            "proof_impact": list(self.proof_impact),
            "risk": self.risk.value,
            "risk_note_ar": self.risk_note_ar,
            "risk_badge": self.risk_badge,
            "buttons": [
                {"label_ar": b.label_ar, "action": b.action, "primary": b.primary}
                for b in self.buttons
            ],
            "owner": self.owner,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "meta": dict(self.meta),
            "created_at": self.created_at.isoformat(),
        }
