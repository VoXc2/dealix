"""Decision queue — decisions require evidence; types are explicit."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DecisionType(StrEnum):
    BUILD = "BUILD"
    SCALE = "SCALE"
    KILL = "KILL"
    HOLD = "HOLD"
    RAISE_PRICE = "RAISE_PRICE"
    OFFER_RETAINER = "OFFER_RETAINER"
    REJECT_REVENUE = "REJECT_REVENUE"
    CREATE_PLAYBOOK = "CREATE_PLAYBOOK"
    CREATE_BENCHMARK = "CREATE_BENCHMARK"
    CREATE_STANDARD = "CREATE_STANDARD"
    CREATE_VENTURE_CANDIDATE = "CREATE_VENTURE_CANDIDATE"


@dataclass(frozen=True, slots=True)
class DecisionQueueItem:
    decision_id: str
    decision_type: DecisionType
    target: str
    evidence: tuple[str, ...]
    owner: str
    deadline: str
    decision_status: str


def decision_has_evidence(item: DecisionQueueItem) -> bool:
    """Rule: no evidence → decision must not be treated as execution-ready."""
    return bool(item.evidence) and all(bool(e.strip()) for e in item.evidence)


def repeated_evidence_without_decision(
    *,
    same_theme_count: int,
    open_decision_exists: bool,
) -> bool:
    """Heuristic: recurring evidence with no open decision = waste signal."""
    return same_theme_count >= 3 and not open_decision_exists
