"""
Smoke tests for the governance layer ported from ai-company-saudi.

These intentionally avoid any DB / FastAPI wiring so they run in any env.
See docs/project-merge-ai-company-saudi.md for the full import rationale.
"""
from __future__ import annotations


def test_classifications_enum_shape() -> None:
    from app.governance.classifications import (
        ACTION_CLASSIFICATIONS,
        NEVER_AUTO_EXECUTE,
        ApprovalClass,
        ReversibilityClass,
        SensitivityClass,
    )

    assert ApprovalClass.A0.requires_approval is False
    assert ApprovalClass.A3.requires_approval is True
    assert ReversibilityClass.R3.blocks_auto_execution is True
    assert SensitivityClass.S3.value == "S3"
    assert len(NEVER_AUTO_EXECUTE) > 0
    assert len(ACTION_CLASSIFICATIONS) > 0


def test_decision_output_contract_validates() -> None:
    from app.governance.classifications import (
        ApprovalClass,
        ReversibilityClass,
        SensitivityClass,
    )
    from app.governance.contracts import DecisionOutput

    d = DecisionOutput(
        entity_id="lead_123",
        objective="qualify_lead",
        agent_name="unit_test",
        recommendation={"action": "log_and_continue"},
        confidence=0.9,
        rationale="Internal note only — no external effect.",
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S0,
        trace_id="trace-xyz",
    )
    assert d.decision_id.startswith("dec_")
    assert d.trace_id == "trace-xyz"
    assert d.is_high_stakes is False
    assert d.requires_human_approval is False


def test_policy_evaluator_has_default_rules() -> None:
    from app.governance.trust.policy import PolicyEvaluator

    ev = PolicyEvaluator()
    assert hasattr(ev, "rules")
    assert len(ev.rules) > 0


def test_contract_schemas_are_present() -> None:
    import pathlib

    schemas_dir = (
        pathlib.Path(__file__).resolve().parents[2]
        / "app"
        / "governance"
        / "contracts"
        / "schemas"
    )
    assert (schemas_dir / "decision_output.schema.json").exists()
    assert (schemas_dir / "event_envelope.schema.json").exists()
    assert (schemas_dir / "evidence_pack.schema.json").exists()
    assert (schemas_dir / "audit_entry.schema.json").exists()


def test_registers_yaml_present() -> None:
    import pathlib

    regs_dir = (
        pathlib.Path(__file__).resolve().parents[2]
        / "app"
        / "governance"
        / "registers"
    )
    for name in (
        "no_overclaim.yaml",
        "compliance_saudi.yaml",
        "technology_radar.yaml",
        "90_day_execution.yaml",
    ):
        assert (regs_dir / name).exists(), name
