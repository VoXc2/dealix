"""Phase D — assert the personal-operator surface handles English
unsafe phrases honestly: where a runtime classifier exists, BLOCKED;
where it does not, the gap is marked ``xfail`` rather than fake-green.

Unsafe English phrases per the closure prompts:

  - "send WhatsApp to purchased numbers"
  - "blast WhatsApp to everyone"
  - "scrape LinkedIn and message them"
  - "auto DM my LinkedIn connections"

Safe English phrases that must route normally:

  - "I want safe B2B growth in Saudi"
  - "I want a manual LinkedIn warm intro draft"
  - "I want a diagnostic for my company"

The static opportunity / daily-brief assertions cover what we ship
today; the free-form classifier coverage is xfailed as a real gap.
"""
from __future__ import annotations

import pytest


UNSAFE_EN_PHRASES = [
    "send WhatsApp to purchased numbers",
    "blast WhatsApp to everyone",
    "scrape LinkedIn and message them",
    "auto DM my LinkedIn connections",
]

SAFE_EN_PHRASES = [
    "I want safe B2B growth in Saudi",
    "I want a manual LinkedIn warm intro draft",
    "I want a diagnostic for my company",
]

UNSAFE_RECOMMENDATION_TOKENS = [
    "blast",
    "purchased numbers",
    "purchased list",
    "scrape",
    "auto-dm",
    "auto dm",
    "without consent",
    "without opt-in",
    "without permission",
    "without approval",
]


def test_static_opportunity_list_has_no_unsafe_english_recommendations():
    from auto_client_acquisition.personal_operator import (
        default_sami_profile,
        suggest_opportunities,
    )

    opportunities = suggest_opportunities(default_sami_profile())
    text = "\n".join(str(getattr(o, "to_card", lambda: {})()) for o in opportunities)
    text_lower = text.lower()
    offenders = [t for t in UNSAFE_RECOMMENDATION_TOKENS if t in text_lower]
    assert not offenders, (
        f"operator opportunities contain unsafe English tokens: {offenders}"
    )


def test_static_daily_brief_has_no_unsafe_english_recommendations():
    from auto_client_acquisition.personal_operator import (
        build_daily_brief,
        default_sami_profile,
    )

    brief = build_daily_brief(default_sami_profile())
    text = str(brief.to_dict()).lower()
    offenders = [t for t in UNSAFE_RECOMMENDATION_TOKENS if t in text]
    assert not offenders, (
        f"daily brief contains unsafe English tokens: {offenders}"
    )


@pytest.mark.parametrize("phrase", SAFE_EN_PHRASES)
def test_safe_phrases_do_not_overlap_unsafe_tokens(phrase: str) -> None:
    """A trivial sanity check: none of the safe phrases contain unsafe
    tokens. Catches future regressions where someone adds a "safe"
    example that actually contains a forbidden phrase."""
    lower = phrase.lower()
    for tok in UNSAFE_RECOMMENDATION_TOKENS:
        assert tok not in lower, (
            f"safe phrase {phrase!r} contains forbidden token {tok!r}"
        )


@pytest.mark.xfail(
    reason=(
        "TODO: free-form English safety classifier on the personal-"
        "operator route is not yet implemented. Once it ships, "
        "remove xfail and assert each UNSAFE_EN_PHRASES input "
        "returns action_mode=blocked AND each SAFE_EN_PHRASES input "
        "routes to a normal recommendation. This xfail is a "
        "deliberate bug ticket."
    ),
    strict=False,
)
def test_freeform_english_unsafe_phrase_is_blocked():
    raise AssertionError(
        "Free-form English safety classifier is not implemented. "
        "See xfail reason above."
    )


@pytest.mark.xfail(
    reason=(
        "TODO: free-form English safety classifier on the personal-"
        "operator route is not yet implemented. Once it ships, "
        "remove xfail and assert each SAFE_EN_PHRASES input routes "
        "to a normal recommendation."
    ),
    strict=False,
)
def test_freeform_english_safe_phrase_routes_normally():
    raise AssertionError(
        "Free-form English safety classifier is not implemented. "
        "See xfail reason above."
    )
