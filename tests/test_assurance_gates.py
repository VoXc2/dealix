"""Assurance System — readiness gate tests."""
from __future__ import annotations

from auto_client_acquisition.assurance_os.gates import GATE_SPECS, evaluate_gates
from auto_client_acquisition.assurance_os.models import AssuranceInputs


def _all_gate_answers(value: bool) -> dict[str, bool]:
    return {cid: value for _, _, _, crits in GATE_SPECS for cid, _, _ in crits}


def test_six_gates_exist() -> None:
    gates = evaluate_gates(AssuranceInputs())
    assert len(gates) == 6
    assert {g.gate_id for g in gates} == {
        "gate1_sales", "gate2_marketing", "gate3_support",
        "gate4_delivery", "gate5_affiliate_partner", "gate6_governance",
    }


def test_empty_inputs_no_gate_passes() -> None:
    gates = evaluate_gates(AssuranceInputs())
    assert all(not g.passed for g in gates)
    # most criteria unknown -> counted
    assert all(g.unknown_count > 0 for g in gates if g.gate_id != "gate6_governance")


def test_derived_governance_criteria_auto_pass() -> None:
    """gate6 yaml-existence criteria are verified by the system itself."""
    gate6 = next(g for g in evaluate_gates(AssuranceInputs())
                 if g.gate_id == "gate6_governance")
    derived = {c.id: c.passed for c in gate6.criteria}
    assert derived["gate6_approval_policy"] is True
    assert derived["gate6_stage_transitions"] is True
    assert derived["gate6_claim_policy"] is True
    # no high-risk auto-send is read live from the empty approval store
    assert derived["gate6_no_high_risk_auto_send"] is True


def test_derived_affiliate_forbidden_claims_auto_pass() -> None:
    gate5 = next(g for g in evaluate_gates(AssuranceInputs())
                 if g.gate_id == "gate5_affiliate_partner")
    crit = next(c for c in gate5.criteria if c.id == "gate5_forbidden_claims")
    assert crit.passed is True


def test_all_answers_true_passes_every_gate() -> None:
    gates = evaluate_gates(AssuranceInputs(gate_answers=_all_gate_answers(True)))
    assert all(g.passed for g in gates)
    assert all(g.unknown_count == 0 for g in gates)


def test_one_false_answer_fails_its_gate() -> None:
    answers = _all_gate_answers(True)
    answers["gate1_invoice_needs_scope"] = False
    gates = evaluate_gates(AssuranceInputs(gate_answers=answers))
    g1 = next(g for g in gates if g.gate_id == "gate1_sales")
    assert g1.passed is False
