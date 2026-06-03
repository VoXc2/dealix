"""Tests for World-Class Execution System helpers."""

from __future__ import annotations

from auto_client_acquisition.command_os import (
    BOARD_MEMO_SECTION_TITLES,
    ExpansionRedTeamVerdict,
    WorldClassAllocationBand,
    WorldClassAllocationInputs,
    compute_world_class_allocation_score,
    expansion_red_team_verdict,
    kill_partner_recommended,
    world_class_allocation_band,
)
from auto_client_acquisition.institutional_os import (
    DEALIX_INSTITUTIONS,
    DEALIX_LAWS,
    DEFENSE_LAYERS,
    ECONOMY_CURRENCIES,
)
from auto_client_acquisition.scorecards import (
    CLIENT_SCORECARD_FIELDS,
    GROUP_SCORECARD_FIELDS,
)


def test_world_class_allocation_band() -> None:
    i = WorldClassAllocationInputs(90, 90, 90, 90, 90, 90, 90)
    s = compute_world_class_allocation_score(i)
    assert s >= 85
    assert world_class_allocation_band(s) == WorldClassAllocationBand.INVEST_HARD


def test_expansion_red_team_kill_unsafe() -> None:
    assert (
        expansion_red_team_verdict(safe=False) == ExpansionRedTeamVerdict.KILL
    )


def test_expansion_red_team_proceed() -> None:
    assert expansion_red_team_verdict() == ExpansionRedTeamVerdict.PROCEED


def test_kill_partner() -> None:
    assert kill_partner_recommended(
        sells_unsafe_promises=True,
        bypasses_governance=False,
        harms_brand=False,
        qa_non_compliant=False,
    )


def test_board_memo_len() -> None:
    assert len(BOARD_MEMO_SECTION_TITLES) == 10


def test_institutional_os_constants() -> None:
    assert len(DEALIX_LAWS) == 7
    assert "strategy_office" in DEALIX_INSTITUTIONS
    assert "proof" in ECONOMY_CURRENCIES
    assert len(DEFENSE_LAYERS) == 6


def test_scorecard_fields() -> None:
    assert "capability_score" in CLIENT_SCORECARD_FIELDS
    assert "mrr" in GROUP_SCORECARD_FIELDS
