from dealix.commercial.customer_value_authority import (
    CustomerValueEvidence,
    CustomerValueState,
    authorize_customer_value_transition,
)


def test_delivery_is_not_customer_value() -> None:
    decision = authorize_customer_value_transition(
        CustomerValueState.WORK_COMPLETED,
        CustomerValueState.DELIVERED,
        CustomerValueEvidence(delivery_receipt_refs=["provider::delivery-1"]),
    )
    assert decision.allowed is True
    assert decision.requested_state == CustomerValueState.DELIVERED
    assert decision.public_claim_allowed is False


def test_cannot_skip_from_work_completed_to_customer_value() -> None:
    decision = authorize_customer_value_transition(
        CustomerValueState.WORK_COMPLETED,
        CustomerValueState.CUSTOMER_VALIDATED_VALUE,
        CustomerValueEvidence(
            customer_value_validation_refs=["customer::feedback"],
            measurement_basis_refs=["baseline::1"],
        ),
    )
    assert decision.allowed is False
    assert decision.reason == "CANNOT_SKIP_CUSTOMER_VALUE_STATES"


def test_customer_validated_value_requires_customer_and_measurement_evidence() -> None:
    incomplete = authorize_customer_value_transition(
        CustomerValueState.CUSTOMER_ACCEPTED,
        CustomerValueState.CUSTOMER_VALIDATED_VALUE,
        CustomerValueEvidence(customer_value_validation_refs=["customer::feedback"]),
    )
    assert incomplete.allowed is False

    complete = authorize_customer_value_transition(
        CustomerValueState.CUSTOMER_ACCEPTED,
        CustomerValueState.CUSTOMER_VALIDATED_VALUE,
        CustomerValueEvidence(
            customer_value_validation_refs=["customer::feedback"],
            measurement_basis_refs=["baseline::approved"],
        ),
    )
    assert complete.allowed is True
    assert complete.public_claim_allowed is False


def test_public_proof_requires_permission() -> None:
    blocked = authorize_customer_value_transition(
        CustomerValueState.CUSTOMER_VALIDATED_VALUE,
        CustomerValueState.PUBLIC_PROOF,
        CustomerValueEvidence(),
    )
    assert blocked.allowed is False
    assert blocked.public_claim_allowed is False

    allowed = authorize_customer_value_transition(
        CustomerValueState.CUSTOMER_VALIDATED_VALUE,
        CustomerValueState.PUBLIC_PROOF,
        CustomerValueEvidence(public_proof_permission_refs=["customer::proof-permission"]),
    )
    assert allowed.allowed is True
    assert allowed.proof_ledger_event_allowed is True
    assert allowed.public_claim_allowed is True
