"""AI Output QA Standard — 8 QA dimensions + 4-tier decision."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


QA_DIMENSIONS: tuple[str, ...] = (
    "accuracy",
    "source_support",
    "schema_validity",
    "arabic_quality",
    "business_usefulness",
    "governance_status",
    "claim_safety",
    "actionability",
)


class QADecision(str, Enum):
    CLIENT_READY = "client_ready"     # >=90
    REVIEW = "review"                 # 80..89
    REVISE = "revise"                 # 70..79
    REJECT = "reject"                 # <70


@dataclass(frozen=True)
class QAResult:
    score: int
    decision: QADecision
    notes: tuple[str, ...] = ()


def classify_qa_score(score: int) -> QADecision:
    if score >= 90:
        return QADecision.CLIENT_READY
    if score >= 80:
        return QADecision.REVIEW
    if score >= 70:
        return QADecision.REVISE
    return QADecision.REJECT
