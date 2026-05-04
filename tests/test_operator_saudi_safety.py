"""Phase D — assert the personal-operator route never RECOMMENDS unsafe
Saudi-Arabic actions, and where the runtime does NOT yet classify
free-form Arabic prompts, mark the gap with ``xfail`` so it's a real
ticket rather than a fake green.

Per the closure prompts, the unsafe Arabic phrases that must be
rejected (or, if the runtime can't classify them, must at least
NOT trigger Growth Starter recommendations) are:

  - "أبي أرسل واتساب لأرقام مشتريها"
  - "أبي حملة واتساب على أرقام من السوق"
  - "أبي blast واتساب"
  - "أرسل لهم كلهم واتساب حتى لو ما وافقوا"
  - "أبي البوت يفتح محادثات واتساب مع ناس ما يعرفوني"

Today the personal-operator router does NOT have a free-text
classifier endpoint. So this file:

1. Asserts the *static* opportunity list (the brief the operator
   currently produces) does NOT recommend cold-WhatsApp campaigns.
2. Marks the free-text classifier coverage as ``xfail`` so the gap
   is visible in test output but does not falsely claim coverage.
"""
from __future__ import annotations

import pytest


UNSAFE_AR_PHRASES = [
    "أبي أرسل واتساب لأرقام مشتريها",
    "أبي حملة واتساب على أرقام من السوق",
    "أبي blast واتساب",
    "أرسل لهم كلهم واتساب حتى لو ما وافقوا",
    "أبي البوت يفتح محادثات واتساب مع ناس ما يعرفوني",
]

# Phrases that must NEVER appear inside the operator's recommendations.
UNSAFE_RECOMMENDATION_TOKENS = [
    "blast",
    "مشتريها",  # "purchased numbers" — implies bought list
    "بدون موافقة",
    "بدون إذن",
    "حملة جماعية",
]


def test_static_opportunity_list_does_not_recommend_cold_outreach():
    """Whatever opportunities the operator produces today must not
    encode unsafe outreach in their text."""
    from auto_client_acquisition.personal_operator import (
        default_sami_profile,
        suggest_opportunities,
    )

    opportunities = suggest_opportunities(default_sami_profile())
    assert opportunities, "operator must surface at least one opportunity"

    text_blob = "\n".join(
        " ".join(filter(None, [
            getattr(o, "title", ""),
            getattr(o, "rationale", ""),
            getattr(o, "next_step", ""),
            str(getattr(o, "to_card", lambda: {})()),
        ])) for o in opportunities
    ).lower()

    offenders = [t for t in UNSAFE_RECOMMENDATION_TOKENS if t.lower() in text_blob]
    assert not offenders, (
        f"operator recommendations contain unsafe tokens: {offenders}"
    )


def test_static_daily_brief_does_not_promote_cold_whatsapp():
    """The daily brief is the founder's main surface; it must never
    suggest cold WhatsApp / blast campaigns / purchased lists."""
    from auto_client_acquisition.personal_operator import (
        build_daily_brief,
        default_sami_profile,
    )

    brief = build_daily_brief(default_sami_profile())
    payload = str(brief.to_dict()).lower()

    offenders = [t for t in UNSAFE_RECOMMENDATION_TOKENS if t.lower() in payload]
    assert not offenders, (
        f"daily brief contains unsafe tokens: {offenders}"
    )


@pytest.mark.xfail(
    reason=(
        "TODO: the personal-operator router does not yet classify "
        "free-form Arabic prompts as unsafe and route them to "
        "BLOCKED. Once the classifier ships, remove xfail and assert "
        "each UNSAFE_AR_PHRASES input returns action_mode=blocked "
        "with safe alternatives. This xfail is a deliberate bug "
        "ticket — never remove it without shipping the classifier."
    ),
    strict=False,
)
def test_freeform_arabic_unsafe_phrase_is_blocked():
    """Placeholder that documents the missing safety classifier."""
    raise AssertionError(
        "Free-form Arabic safety classifier is not implemented. "
        "See xfail reason above."
    )
