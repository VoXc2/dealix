from __future__ import annotations

from dealix.commercial.arm_registry import ALL_ARMS, get_active_arms


def test_arm_registry_has_unique_dynamic_inventory() -> None:
    ids = [arm.arm_id for arm in ALL_ARMS]
    assert ids
    assert len(ids) == len(set(ids))
    assert get_active_arms()


def test_arm_registry_does_not_reassert_legacy_runtime_architecture() -> None:
    text = "\n".join(arm.purpose.lower() for arm in ALL_ARMS)
    forbidden = (
        "deepwip 3",
        "5-agent dispatch",
        "five-agent dispatch",
        "local→free→cheap→premium",
        "local->free->cheap->premium",
    )
    for marker in forbidden:
        assert marker not in text


def test_model_router_is_provider_neutral_fail_closed() -> None:
    arm = next(arm for arm in ALL_ARMS if arm.arm_id == "arm_39_model_router")
    purpose = arm.purpose.lower()
    assert "provider-neutral" in purpose
    assert "hold" in purpose
    assert "no silent paid spill" in purpose


def test_agent_packets_are_logical_agent_not_fixed_five_authority() -> None:
    arm = next(arm for arm in ALL_ARMS if arm.arm_id == "arm_23_agent_packets")
    purpose = arm.purpose.lower()
    assert "logical-agent" in purpose
    assert "5-agent" not in purpose


def test_resource_governor_is_runtime_capacity_authority_in_arm_copy() -> None:
    economic = next(arm for arm in ALL_ARMS if arm.arm_id == "arm_02_economic_cell")
    portfolio = next(arm for arm in ALL_ARMS if arm.arm_id == "arm_06_portfolio_bets")
    assert "resourcegovernor" in economic.purpose.lower()
    assert "resourcegovernor" in portfolio.purpose.lower()
