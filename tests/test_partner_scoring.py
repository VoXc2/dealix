"""Partner scoring rubric — playbook section 6.

Verifies the positive/negative signal weights and the recommendation
thresholds of ``score_partner``.
"""

from __future__ import annotations

from auto_client_acquisition.partnership_os.partner_scoring import score_partner


def _strong_application() -> dict[str, object]:
    return {
        "audience_type": "b2b",
        "country": "sa",
        "main_channel": "consulting",
        "prior_referrals": 4,
        "content_quality": True,
        "trusted_brand": True,
        "disclosure_accepted": True,
        "plan": "We will introduce Dealix to our B2B consulting clients via "
        "warm intros and a quarterly review.",
    }


def test_strong_application_scores_high_and_is_approve_candidate() -> None:
    result = score_partner(_strong_application())
    # +4 b2b +3 gcc +3 consultant +2 prior +2 content +2 brand = 16
    assert result.score == 16
    assert result.recommendation == "approve_candidate"


def test_b2b_audience_signal_adds_four() -> None:
    result = score_partner(
        {"audience_type": "b2b", "disclosure_accepted": True, "plan": "x" * 30}
    )
    assert result.breakdown.get("b2b_audience") == 4


def test_gcc_country_signal_adds_three() -> None:
    result = score_partner(
        {"country": "UAE", "disclosure_accepted": True, "plan": "x" * 30}
    )
    assert result.breakdown.get("gcc") == 3


def test_missing_disclosure_penalised() -> None:
    result = score_partner({"audience_type": "b2b", "plan": "x" * 30})
    assert result.breakdown.get("no_disclosure") == -3


def test_vague_plan_penalised() -> None:
    result = score_partner(
        {"audience_type": "b2b", "disclosure_accepted": True, "plan": "soon"}
    )
    assert result.breakdown.get("vague_plan") == -3


def test_spam_and_fake_audience_drive_rejection() -> None:
    result = score_partner(
        {
            "audience_type": "b2c",
            "spam_behavior": True,
            "fake_audience": True,
            "disclosure_accepted": False,
            "plan": "",
        }
    )
    # -5 spam -4 fake -3 no_disclosure -3 vague = -15
    assert result.score < 0
    assert result.recommendation == "reject"


def test_to_dict_round_trips() -> None:
    result = score_partner(_strong_application())
    payload = result.to_dict()
    assert payload["score"] == result.score
    assert payload["recommendation"] == result.recommendation
    assert isinstance(payload["breakdown"], dict)
