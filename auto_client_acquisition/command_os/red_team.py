"""Red team — ordered verdict from self-review flags."""

from __future__ import annotations

from enum import StrEnum


class RedTeamVerdict(StrEnum):
    PROCEED = "proceed"
    PROCEED_WITH_CONTROLS = "proceed_with_controls"
    RESCOPE = "rescope"
    REJECT = "reject"
    ESCALATE = "escalate"


def red_team_verdict(
    *,
    custom_work_only: bool = False,
    real_proof: bool = True,
    high_pii_risk: bool = False,
    over_claim: bool = False,
    cannot_redeliver: bool = False,
    partner_trust_risk: bool = False,
    builds_capital: bool = True,
) -> RedTeamVerdict:
    """Apply simple priority rules; first match wins (broadly conservative)."""
    if cannot_redeliver:
        return RedTeamVerdict.ESCALATE
    if over_claim and not real_proof:
        return RedTeamVerdict.REJECT
    if partner_trust_risk:
        return RedTeamVerdict.ESCALATE
    if high_pii_risk:
        return RedTeamVerdict.PROCEED_WITH_CONTROLS
    if custom_work_only and not builds_capital:
        return RedTeamVerdict.RESCOPE
    return RedTeamVerdict.PROCEED
