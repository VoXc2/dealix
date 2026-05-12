"""T13d — enforce that every vertical's `agents:` list maps to a
registered skill handler.

Without this gate a future PR can ship a vertical claiming an agent
that doesn't actually run, which is exactly the kind of marketing /
code drift the commercial-readiness audit flagged."""

from __future__ import annotations

import pytest

# Trigger handler-registration side-effects so registered_ids() is populated.
from dealix.agents.skills import handlers_data, handlers_llm  # noqa: F401
from dealix.agents.skills.handlers import registered_ids
from dealix.verticals import list_all


def _registered_set() -> set[str]:
    return set(registered_ids())


def test_every_listed_agent_in_every_vertical_has_a_registered_handler() -> None:
    registered = _registered_set()
    missing: dict[str, list[str]] = {}
    for v in list_all():
        gap = [a for a in v.agents if a not in registered]
        if gap:
            missing[v.id] = gap
    assert missing == {}, (
        "Verticals are claiming agents that don't have registered handlers: "
        f"{missing}. Either register the handler or move it to roadmap_agents."
    )


@pytest.mark.parametrize(
    "expected_agent",
    [
        "sales_qualifier",
        "lead_scorer",
        "content_generator_ar",
        "ar_en_translator",
        "proposal_writer",
        "email_triage",
        "contract_analyst",
        "meeting_summarizer",
        "crm_syncer",
        "market_researcher",
        "renewal_forecaster",
        "compliance_reviewer",
    ],
)
def test_canonical_twelve_skills_are_registered(expected_agent: str) -> None:
    assert expected_agent in _registered_set(), (
        f"Canonical skill `{expected_agent}` is missing a Python handler — "
        f"every vertical bundle references some subset of these 12."
    )


def test_no_vertical_has_zero_agents() -> None:
    """A vertical without agents is just a landing page — surface it
    early so the sales rep doesn't hand a customer an empty bundle."""
    empty = [v.id for v in list_all() if not v.agents]
    assert empty == [], f"Verticals with empty `agents:` list: {empty}"
