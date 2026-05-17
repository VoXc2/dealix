"""Agent red-team — assert no high-risk action can auto-execute.

Trust is not earned because an agent replied correctly once. Every
never-auto-execute action and every machine's approval-required action
must route to a human approval, never auto-allow.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.execution_assurance_os import load_machine_registry
from dealix.classifications import NEVER_AUTO_EXECUTE, ApprovalClass, classify

pytestmark = pytest.mark.unit


def test_never_auto_execute_actions_all_require_approval() -> None:
    """Every never-auto-execute action classifies above A0."""
    for action in NEVER_AUTO_EXECUTE:
        approval, _reversibility, _sensitivity = classify(action)
        assert approval != ApprovalClass.A0, f"{action} would auto-execute"
        assert approval.requires_approval is True


def test_registry_approval_actions_are_real_gates() -> None:
    """Every approval-required action declared by a machine truly gates."""
    reg = load_machine_registry()
    declared = {
        action
        for m in reg.machines
        for action in m.approval_required_actions
    }
    assert declared, "no machine declares an approval-required action"
    for action in declared:
        if action in NEVER_AUTO_EXECUTE:
            approval, _r, _s = classify(action)
            assert approval.requires_approval is True


def test_governance_layer_gates_the_dangerous_actions() -> None:
    """The Governance Layer must gate genuinely dangerous, never-auto actions."""
    gov = load_machine_registry().get("governance_layer")
    assert gov is not None
    overlap = set(gov.approval_required_actions) & set(NEVER_AUTO_EXECUTE)
    assert overlap, (
        "governance_layer declares no never-auto-execute actions as gated"
    )


def test_every_machine_with_external_output_declares_an_owner() -> None:
    """An agent without an accountable owner cannot be trusted to act."""
    reg = load_machine_registry()
    for m in reg.machines:
        assert m.owner.strip(), f"{m.id} has no accountable owner"
