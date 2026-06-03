"""A draft below P1 personalization cannot be send-ready."""

from core.safety.draft import personalization_grade, grade_at_least, evaluate_draft
from tests._fixtures import good_cold_email, generic_bad_draft


def test_generic_draft_is_below_p1():
    grade = personalization_grade(generic_bad_draft())
    assert grade == "P0"
    assert grade_at_least(grade, "P1") is False


def test_personalized_draft_meets_threshold():
    grade = personalization_grade(good_cold_email())
    assert grade_at_least(grade, "P1") is True


def test_below_p1_is_not_send_ready():
    result = evaluate_draft(generic_bad_draft(), channel="email")
    assert result.send_ready is False
    assert any("below_min_personalization" in v for v in result.violations)


def test_grade_ordering():
    assert grade_at_least("P3", "P1")
    assert grade_at_least("P1", "P1")
    assert not grade_at_least("P0", "P1")
