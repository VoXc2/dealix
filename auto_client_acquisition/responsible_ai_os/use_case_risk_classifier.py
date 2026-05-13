"""AI Use Case Risk Classifier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class UseCaseRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    FORBIDDEN = "forbidden"


_FORBIDDEN_PATTERNS: frozenset[str] = frozenset({
    "scraping",
    "cold_whatsapp_automation",
    "linkedin_automation",
    "guaranteed_sales_claims",
    "sourceless_decisioning",
})


@dataclass(frozen=True)
class UseCaseCard:
    use_case_id: str
    name: str
    department: str
    data_sources: tuple[str, ...]
    contains_pii: bool
    external_action_allowed: bool
    forbidden_patterns_detected: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        unknown = set(self.forbidden_patterns_detected) - _FORBIDDEN_PATTERNS
        if unknown:
            raise ValueError(
                "unknown_forbidden_pattern:" + ",".join(sorted(unknown))
            )


def classify_use_case(card: UseCaseCard) -> UseCaseRiskLevel:
    if card.forbidden_patterns_detected:
        return UseCaseRiskLevel.FORBIDDEN
    if card.external_action_allowed:
        return UseCaseRiskLevel.HIGH
    if card.contains_pii:
        return UseCaseRiskLevel.MEDIUM
    return UseCaseRiskLevel.LOW
