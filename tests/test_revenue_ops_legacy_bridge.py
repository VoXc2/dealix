"""Revenue Ops Machine — one-way bridge to the legacy 12-stage deal machine."""

from __future__ import annotations

from api.routers.full_os import STAGES as LEGACY_STAGES
from api.routers.full_os import TRANSITIONS as LEGACY_TRANSITIONS
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    FROM_LEGACY,
    LEGACY_STAGE_BRIDGE,
    FunnelState,
    legacy_stage,
)


def test_every_funnel_state_maps_to_a_real_legacy_stage() -> None:
    for state in FunnelState:
        mapped = LEGACY_STAGE_BRIDGE[state]
        assert mapped in LEGACY_STAGES, f"{state} -> unknown legacy stage {mapped}"


def test_legacy_stage_helper_matches_the_bridge() -> None:
    for state in FunnelState:
        assert legacy_stage(state) == LEGACY_STAGE_BRIDGE[state]


def test_from_legacy_covers_every_legacy_stage() -> None:
    for stage in LEGACY_STAGES:
        assert stage in FROM_LEGACY
        assert isinstance(FROM_LEGACY[stage], FunnelState)


def test_from_legacy_round_trips_to_a_valid_legacy_stage() -> None:
    for stage, funnel in FROM_LEGACY.items():
        # The reverse map need not be exact, but re-bridging must stay legal.
        assert legacy_stage(funnel) in LEGACY_STAGES


def test_legacy_machine_is_untouched() -> None:
    # The legacy machine must still be the canonical 12-stage shape.
    assert len(LEGACY_STAGES) == 13  # 10 active + 3 terminal
    assert "new_lead" in LEGACY_STAGES
    assert "closed_won" in LEGACY_STAGES
    assert LEGACY_TRANSITIONS["closed_won"] == []
