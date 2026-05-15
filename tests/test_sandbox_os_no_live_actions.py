"""Non-negotiable: sandbox simulations never perform live actions.

Guards `no_live_send` / `no_live_charge` — sandbox runs are stubbed and flagged
non-production, and live-style action types are recorded as blocked.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.sandbox_os import (
    LIVE_ACTION_TYPES,
    SandboxStep,
    get_sandbox_engine,
    reset_sandbox_engine,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_sandbox_engine()


def test_simulation_is_never_production() -> None:
    run = get_sandbox_engine().simulate(
        workflow_id="wf1", steps=[SandboxStep(step_id="1", action_type="noop")]
    )
    assert run.is_production is False


def test_live_action_types_are_blocked_in_sandbox() -> None:
    steps = [
        SandboxStep(step_id=str(i), action_type=action)
        for i, action in enumerate(sorted(LIVE_ACTION_TYPES))
    ]
    run = get_sandbox_engine().simulate(workflow_id="wf1", steps=steps)
    for result in run.step_results:
        assert result["simulated"] is True
        assert result["live_blocked"] is True
        assert result["outcome"] == "stub_ok"


def test_non_live_action_runs_but_stays_simulated() -> None:
    run = get_sandbox_engine().simulate(
        workflow_id="wf1", steps=[SandboxStep(step_id="1", action_type="enrich")]
    )
    result = run.step_results[0]
    assert result["simulated"] is True
    assert result["live_blocked"] is False
