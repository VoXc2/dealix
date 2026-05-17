"""Sales OS — distribution funnel: 12 stages, forward-only transitions."""

from __future__ import annotations

from auto_client_acquisition.governance_os.approval_matrix import approval_for_action
from auto_client_acquisition.sales_os.funnel import (
    STAGE_ORDER,
    STAGE_PROPERTIES,
    TERMINAL,
    FunnelStage,
    approval_rule_for,
    next_action_for,
    validate_transition,
)


def test_twelve_stages_present() -> None:
    assert len(FunnelStage) == 12
    assert len(STAGE_ORDER) == 12
    assert len(STAGE_PROPERTIES) == 12


def test_every_stage_has_all_seven_properties_non_empty() -> None:
    for stage in FunnelStage:
        spec = STAGE_PROPERTIES[stage]
        for field_name in (
            "owner",
            "status",
            "next_action",
            "evidence",
            "approval_rule",
            "kpi",
            "failure_mode",
        ):
            value = getattr(spec, field_name)
            assert value and value.strip(), f"{stage}.{field_name} is empty"


def test_forward_transition_allowed() -> None:
    for i in range(len(STAGE_ORDER) - 1):
        ok, reason = validate_transition(STAGE_ORDER[i], STAGE_ORDER[i + 1].value)
        assert ok, f"{STAGE_ORDER[i]} -> {STAGE_ORDER[i + 1]} should advance: {reason}"


def test_skip_ahead_rejected() -> None:
    ok, reason = validate_transition(FunnelStage.TARGET, FunnelStage.DEMO_12MIN.value)
    assert not ok
    assert reason == "skip_ahead_not_allowed"


def test_backward_transition_rejected() -> None:
    ok, reason = validate_transition(FunnelStage.DEMO_12MIN, FunnelStage.TARGET.value)
    assert not ok
    assert reason == "backward_transition_not_allowed"


def test_same_stage_rejected() -> None:
    ok, reason = validate_transition(FunnelStage.TARGET, FunnelStage.TARGET.value)
    assert not ok
    assert reason == "backward_transition_not_allowed"


def test_terminal_outcomes_reachable_from_any_stage() -> None:
    assert frozenset({"lost", "refer_out"}) == TERMINAL
    for stage in FunnelStage:
        for outcome in TERMINAL:
            ok, reason = validate_transition(stage, outcome)
            assert ok, f"{stage} -> {outcome} should be allowed"
            assert reason == "terminal_outcome"


def test_unknown_target_rejected() -> None:
    ok, reason = validate_transition(FunnelStage.TARGET, "not_a_stage")
    assert not ok
    assert reason.startswith("unknown_target_stage")


def test_manual_outreach_approval_matches_governance_matrix() -> None:
    risk, route = approval_for_action("send email")
    rule = approval_rule_for(FunnelStage.MANUAL_OUTREACH)
    assert route in rule
    assert risk in rule
    assert "draft-only" in rule


def test_next_action_helper() -> None:
    assert next_action_for(FunnelStage.TARGET) == STAGE_PROPERTIES[FunnelStage.TARGET].next_action
