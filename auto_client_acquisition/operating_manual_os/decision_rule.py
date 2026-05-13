"""Dealix Decision Rule — six questions with a scoring band.

See ``docs/operating_manual/DEALIX_DECISION_RULE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DealixDecisionQuestion(str, Enum):
    SELLS = "does_it_sell"
    DELIVERS = "does_it_deliver"
    PROVES = "does_it_prove"
    GOVERNS = "does_it_govern"
    COMPOUNDS = "does_it_compound"
    SCALES = "does_it_scale"


DEALIX_DECISION_QUESTIONS: tuple[DealixDecisionQuestion, ...] = tuple(
    DealixDecisionQuestion
)


class DealixDecisionVerdict(str, Enum):
    DO_NOT_ACT = "do_not_act"
    ACT_WITH_CAUTION = "act_with_caution"
    PRIORITY = "priority"
    STRATEGIC_BET = "strategic_bet"


@dataclass(frozen=True)
class DealixDecisionAnswers:
    """Boolean answers to the six doctrine questions.

    A boolean answer is sufficient; the doctrine intentionally avoids a
    weighted score so the decision is not over-tuned.
    """

    candidate: str
    sells: bool
    delivers: bool
    proves: bool
    governs: bool
    compounds: bool
    scales: bool
    evidence: dict[DealixDecisionQuestion, str] | None = None

    def yes_count(self) -> int:
        return sum(
            (
                self.sells,
                self.delivers,
                self.proves,
                self.governs,
                self.compounds,
                self.scales,
            )
        )


@dataclass(frozen=True)
class DealixDecisionEvaluation:
    candidate: str
    yes_count: int
    verdict: DealixDecisionVerdict
    rationale: str


def _verdict_for(yes_count: int) -> DealixDecisionVerdict:
    if yes_count <= 2:
        return DealixDecisionVerdict.DO_NOT_ACT
    if yes_count == 3:
        return DealixDecisionVerdict.ACT_WITH_CAUTION
    if yes_count == 4:
        return DealixDecisionVerdict.PRIORITY
    return DealixDecisionVerdict.STRATEGIC_BET


_RATIONALES: dict[DealixDecisionVerdict, str] = {
    DealixDecisionVerdict.DO_NOT_ACT: "fewer_than_three_yeses_against_doctrine",
    DealixDecisionVerdict.ACT_WITH_CAUTION: "three_yeses_thirty_day_review_required",
    DealixDecisionVerdict.PRIORITY: "four_yeses_kill_criteria_required",
    DealixDecisionVerdict.STRATEGIC_BET: "five_or_six_yeses_capital_plan_required",
}


def evaluate_dealix_decision(answers: DealixDecisionAnswers) -> DealixDecisionEvaluation:
    yes = answers.yes_count()
    verdict = _verdict_for(yes)
    return DealixDecisionEvaluation(
        candidate=answers.candidate,
        yes_count=yes,
        verdict=verdict,
        rationale=_RATIONALES[verdict],
    )
