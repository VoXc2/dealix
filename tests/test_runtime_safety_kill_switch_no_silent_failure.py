"""Non-negotiable: a kill switch never silently fails.

Guards `no_silent_failures` — invalid kill-switch operations raise loudly.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.runtime_safety_os import (
    SafetyError,
    get_safety_engine,
    reset_safety_engine,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_safety_engine()


def test_engage_on_empty_target_raises() -> None:
    with pytest.raises(SafetyError):
        get_safety_engine().engage_kill_switch(target="")


def test_release_unknown_switch_raises() -> None:
    with pytest.raises(SafetyError):
        get_safety_engine().release_kill_switch("kil_does_not_exist")


def test_double_release_raises() -> None:
    engine = get_safety_engine()
    switch = engine.engage_kill_switch(target="wfX", reason="x")
    engine.release_kill_switch(switch.switch_id)
    with pytest.raises(SafetyError):
        engine.release_kill_switch(switch.switch_id)


def test_check_empty_target_raises() -> None:
    with pytest.raises(SafetyError):
        get_safety_engine().check(target="")
