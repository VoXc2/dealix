"""Red team protocol — expansion-grade verdicts (broader than red_team.py)."""

from __future__ import annotations

from enum import StrEnum


class ExpansionRedTeamVerdict(StrEnum):
    PROCEED = "proceed"
    PROCEED_WITH_CONTROLS = "proceed_with_controls"
    RESCOPE = "rescope"
    PILOT_ONLY = "pilot_only"
    HOLD = "hold"
    KILL = "kill"


def expansion_red_team_verdict(
    *,
    sells: bool = True,
    repeatable: bool = True,
    has_proof: bool = True,
    safe: bool = True,
    builds_capital: bool = True,
    reduces_effort_later: bool = True,
    strengthens_core_os: bool = True,
) -> ExpansionRedTeamVerdict:
    """
    Conservative ordering for expansion decisions.
    All flags default True = healthy proposal.
    """
    if not safe:
        return ExpansionRedTeamVerdict.KILL
    if not sells:
        return ExpansionRedTeamVerdict.KILL
    if not has_proof:
        return ExpansionRedTeamVerdict.HOLD
    if not repeatable:
        return ExpansionRedTeamVerdict.PILOT_ONLY
    if not builds_capital:
        return ExpansionRedTeamVerdict.RESCOPE
    if not reduces_effort_later and not strengthens_core_os:
        return ExpansionRedTeamVerdict.PROCEED_WITH_CONTROLS
    return ExpansionRedTeamVerdict.PROCEED
