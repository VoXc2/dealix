"""Intelligence Signal — typed shape across six intelligence types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SignalKind(str, Enum):
    MARKET = "market"
    CLIENT = "client"
    DATA = "data"
    WORKFLOW = "workflow"
    GOVERNANCE = "governance"
    PRODUCT = "product"


@dataclass(frozen=True)
class IntelligenceSignal:
    signal_id: str
    kind: SignalKind
    source: str
    evidence: tuple[str, ...]
    recommended_decision: str
    commercial_link: str | None = None
    confidence: str = "medium"  # low | medium | high
    metadata: dict[str, str] = field(default_factory=dict)
