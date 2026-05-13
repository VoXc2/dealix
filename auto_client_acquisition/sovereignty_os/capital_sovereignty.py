"""Capital Sovereignty — post-engagement capital review questions.

See ``docs/sovereignty/CAPITAL_SOVEREIGNTY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CapitalReviewQuestion(str, Enum):
    ASSET_PRODUCED = "asset_produced"
    REUSABLE = "reusable"
    RAISES_PRICING_POWER = "raises_pricing_power"
    REDUCES_DELIVERY_TIME = "reduces_delivery_time"
    REDUCES_RISK = "reduces_risk"
    RAISES_TRUST = "raises_trust"
    WORKS_AS_CONTENT_OR_BENCHMARK = "works_as_content_or_benchmark"
    OPENS_RETAINER = "opens_retainer"


REQUIRED_CAPITAL_REVIEW_QUESTIONS: tuple[CapitalReviewQuestion, ...] = tuple(
    CapitalReviewQuestion
)


@dataclass(frozen=True)
class CapitalReview:
    engagement_id: str
    answers: dict[CapitalReviewQuestion, bool]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        missing = set(REQUIRED_CAPITAL_REVIEW_QUESTIONS) - set(self.answers)
        if missing:
            raise ValueError(
                "missing_capital_review_answers:"
                + ",".join(sorted(q.value for q in missing))
            )

    def yes_count(self) -> int:
        return sum(1 for v in self.answers.values() if v)


def capital_review_pass(review: CapitalReview) -> bool:
    """Doctrine: a passable capital review answers `asset_produced` and at
    least three of the strategic questions affirmatively.
    """

    if not review.answers[CapitalReviewQuestion.ASSET_PRODUCED]:
        return False
    strategic = {
        CapitalReviewQuestion.REUSABLE,
        CapitalReviewQuestion.RAISES_PRICING_POWER,
        CapitalReviewQuestion.REDUCES_DELIVERY_TIME,
        CapitalReviewQuestion.REDUCES_RISK,
        CapitalReviewQuestion.RAISES_TRUST,
        CapitalReviewQuestion.WORKS_AS_CONTENT_OR_BENCHMARK,
        CapitalReviewQuestion.OPENS_RETAINER,
    }
    strategic_yes = sum(1 for q in strategic if review.answers[q])
    return strategic_yes >= 3
