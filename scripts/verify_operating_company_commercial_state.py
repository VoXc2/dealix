#!/usr/bin/env python3
"""Deterministically verify the canonical Dealix commercial state contract."""

from __future__ import annotations

from auto_client_acquisition.orchestrator.operating_company_contract import (
    CANONICAL_COMMERCIAL_CHAIN,
    DEFAULT_OPERATING_COMPANY_CONTRACT,
)

EXPECTED_CHAIN = (
    "real_interaction",
    "verified_relationship",
    "qualified_problem",
    "free_mini_diagnostic",
    "qualified_discovery",
    "customer_specific_quote",
    "pilot_decision",
    "pilot_payment_verified",
    "pilot_delivery",
    "proof_review",
    "expansion_or_stop",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    contract = DEFAULT_OPERATING_COMPANY_CONTRACT

    require(CANONICAL_COMMERCIAL_CHAIN == EXPECTED_CHAIN, "canonical commercial chain drift")

    ok, _ = contract.validate_state_transition(
        src="research_signal", dst="verified_relationship"
    )
    require(not ok, "research must not promote directly to verified relationship")

    ok, _ = contract.validate_event(
        event_type="relationship_verified",
        history=("interaction_captured",),
        payload={"interaction_evidence_ref": "receipt://interaction/1"},
    )
    require(ok, "relationship should accept real interaction evidence")

    for blank in ("", "   ", None):
        ok, _ = contract.validate_event(
            event_type="relationship_verified",
            history=("interaction_captured",),
            payload={"interaction_evidence_ref": blank},
        )
        require(not ok, "blank interaction reference must not verify relationship")

    ok, _ = contract.validate_event(
        event_type="diagnostic_started",
        history=("problem_qualified",),
        payload={},
    )
    require(ok, "Free Mini Diagnostic must not require payment")

    ok, _ = contract.validate_event(
        event_type="diagnostic_started",
        history=("relationship_verified",),
        payload={},
    )
    require(not ok, "diagnostic must require a qualified problem")

    ok, _ = contract.validate_event(
        event_type="pilot_payment_verified",
        history=("pilot_decision_approved",),
        payload={},
    )
    require(not ok, "pilot payment cannot verify without payment evidence")

    for blank in ("", "   ", None):
        ok, _ = contract.validate_event(
            event_type="pilot_payment_verified",
            history=("pilot_decision_approved",),
            payload={"payment_proof_ref": blank},
        )
        require(not ok, "blank payment reference must not verify pilot payment")

    ok, _ = contract.validate_event(
        event_type="pilot_payment_verified",
        history=("pilot_decision_approved",),
        payload={"payment_proof_ref": "receipt://payment/1"},
    )
    require(ok, "pilot payment should accept explicit payment evidence")

    ok, _ = contract.validate_event(
        event_type="pilot_delivery_started",
        history=("pilot_payment_verified",),
        payload={},
    )
    require(not ok, "pilot delivery must fail closed without payment proof reference")

    ok, _ = contract.validate_event(
        event_type="pilot_delivery_started",
        history=("pilot_payment_verified",),
        payload={"payment_proof_ref": "receipt://payment/1"},
    )
    require(ok, "pilot delivery should start only with verified payment proof")

    ok, _ = contract.validate_event(
        event_type="closed_won",
        history=("final_proof_pack_ready",),
        payload={},
    )
    require(not ok, "closed_won must not promote without payment evidence")

    ok, _ = contract.validate_event(
        event_type="closed_won",
        history=("pilot_payment_verified",),
        payload={"payment_proof_ref": "   "},
    )
    require(not ok, "whitespace payment reference must not create closed_won truth")

    ok, _ = contract.validate_event(
        event_type="case_study_approved",
        history=(),
        payload={"client_permission": "   "},
    )
    require(not ok, "whitespace permission must not authorize case-study approval")

    quote_approval, _ = contract.requires_approval_for_action(
        action_id="send_customer_specific_quote"
    )
    require(quote_approval, "customer-specific quote send must remain approval-gated")

    print("PASS: operating-company commercial state contract")
    print("chain=" + " -> ".join(CANONICAL_COMMERCIAL_CHAIN))
    print("blank_evidence_refs=BLOCKED")
    print("whitespace_evidence_refs=BLOCKED")
    print("blank_truthy_permissions=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
