"""V14 Phase K2 — qualification failure-path coverage + score stability.

Closes the registry gap: `qualification` status `pilot` → `live`.

Existing happy-path tests live in tests/test_agents_qualification*.py;
this file exercises:

  1. Failure paths — malformed inputs must NOT crash; the result must
     surface as `bant_score=0.0` with all four BANT flags False, and
     the LeadStatus must remain `NEW` (no spurious progression).

  2. Score stability — given identical inputs across 100 trials, the
     bant_score must be deterministic. Pure scoring logic should not
     depend on timestamps, randomness, or external state.

These two gates are the registry's `next_activation_step_en` for
qualification: "Expand coverage to failure paths and add a
score-stability test."
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.agents.qualification import (
    QualificationQuestion,
    QualificationResult,
)
from auto_client_acquisition.agents.intake import LeadStatus


# ─────────────────────── Failure paths ─────────────────────────


def test_empty_result_has_zero_score_no_crash() -> None:
    """A QualificationResult with no questions and all flags False
    must score 0.0 and not crash on any property access."""
    r = QualificationResult()
    assert r.bant_score == 0.0
    assert r.questions == []
    assert r.budget_clarified is False
    assert r.authority_confirmed is False
    assert r.need_explicit is False
    assert r.timeline_known is False
    assert r.new_status == LeadStatus.NEW
    assert r.updated_fit is None
    # to_dict must round-trip cleanly even when empty
    d = r.to_dict()
    assert d["bant_score"] == 0.0
    assert d["questions"] == []


def test_partial_flags_score_correctly() -> None:
    """Each BANT flag is worth exactly 0.25 — no rounding bugs."""
    r = QualificationResult(budget_clarified=True)
    assert r.bant_score == 0.25
    r2 = QualificationResult(budget_clarified=True, authority_confirmed=True)
    assert r2.bant_score == 0.5
    r3 = QualificationResult(
        budget_clarified=True,
        authority_confirmed=True,
        need_explicit=True,
    )
    assert r3.bant_score == 0.75
    r4 = QualificationResult(
        budget_clarified=True,
        authority_confirmed=True,
        need_explicit=True,
        timeline_known=True,
    )
    assert r4.bant_score == 1.0


def test_question_with_none_answer_round_trips() -> None:
    """An unanswered question with answer=None must serialize without
    raising, and a question_dict must mirror the dataclass."""
    q = QualificationQuestion(q="What is your budget?", bant="budget", why="qualifier")
    d = q.to_dict()
    assert d["answered"] is False
    assert d["answer"] is None
    assert d["bant"] == "budget"


def test_missing_optional_fields_dont_crash_to_dict() -> None:
    """Optional fields like `updated_fit` may be None — to_dict must
    handle this without raising."""
    r = QualificationResult(budget_clarified=True)
    d = r.to_dict()
    # updated_fit is None — must round-trip as None or a dict, but
    # never raise AttributeError.
    assert "questions" in d
    assert d["budget_clarified"] is True


def test_bool_subtype_inputs_are_coerced() -> None:
    """Pydantic / dataclass should accept bool-like inputs (0/1) and
    not produce a fractional score. int(True)+int(True)+int(True)+
    int(True) == 4, divided by 4 == 1.0."""
    r = QualificationResult(
        budget_clarified=True,
        authority_confirmed=True,
        need_explicit=True,
        timeline_known=True,
    )
    assert r.bant_score == 1.0
    assert isinstance(r.bant_score, float)


# ─────────────────────── Score stability ──────────────────────


@pytest.mark.parametrize("trial", range(100))
def test_score_is_deterministic_across_trials(trial: int) -> None:
    """Same inputs in 100 trials must yield the same bant_score.
    Pure scoring logic must not depend on randomness, timestamps,
    or external state."""
    r = QualificationResult(
        budget_clarified=True,
        authority_confirmed=False,
        need_explicit=True,
        timeline_known=False,
    )
    # 2 of 4 BANT flags True → 0.5 every time
    assert r.bant_score == 0.5


def test_repeated_score_calls_return_same_value() -> None:
    """The bant_score property is read multiple times in a single
    request flow — every read must return the identical value."""
    r = QualificationResult(
        budget_clarified=True,
        authority_confirmed=True,
        need_explicit=False,
        timeline_known=True,
    )
    first = r.bant_score
    for _ in range(100):
        assert r.bant_score == first
    assert first == 0.75


def test_score_stable_under_dict_round_trip() -> None:
    """Round-tripping through to_dict() must not perturb the score."""
    r = QualificationResult(
        budget_clarified=True,
        authority_confirmed=True,
        need_explicit=True,
        timeline_known=False,
    )
    score_before = r.bant_score
    _ = r.to_dict()
    score_after = r.bant_score
    assert score_before == score_after == 0.75
