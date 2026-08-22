"""Safety invariants for canonical Collaboration OS event contracts."""

import pytest

from dealix.company_intelligence.collaboration_contracts import (
    CollaborationActorType,
    CollaborationEventKind,
    build_collaboration_event,
)


def _event(**overrides):
    payload = {
        "tenant_id": "tenant-a",
        "deduplication_key": "safety:event:1",
        "kind": CollaborationEventKind.MESSAGE,
        "actor_id": "founder",
        "actor_type": CollaborationActorType.HUMAN,
        "source_id": "test",
        "channel_id": "ops",
        "content": "internal coordination only",
    }
    payload.update(overrides)
    return build_collaboration_event(**payload)


def test_collaboration_event_cannot_be_business_proof() -> None:
    with pytest.raises(ValueError, match="cannot become business proof"):
        _event(proof_eligible=True)


def test_collaboration_metadata_rejects_obvious_credentials_recursively() -> None:
    with pytest.raises(ValueError, match="credential-bearing metadata"):
        _event(metadata={"connector": {"access_token": "never-store-me"}})


def test_dm_creation_requires_participants() -> None:
    with pytest.raises(ValueError, match="at least two participants"):
        _event(
            kind=CollaborationEventKind.DM_CREATED,
            deduplication_key="dm:bad",
            channel_id="dm-1",
            metadata={"participants": ["founder"]},
        )


def test_approval_and_proof_references_require_canonical_ids() -> None:
    with pytest.raises(ValueError, match="approval_id"):
        _event(
            kind=CollaborationEventKind.APPROVAL_REFERENCE,
            deduplication_key="approval-ref:bad",
            channel_id="",
            metadata={},
        )

    with pytest.raises(ValueError, match="proof_event_id"):
        _event(
            kind=CollaborationEventKind.PROOF_REFERENCE,
            deduplication_key="proof-ref:bad",
            channel_id="",
            metadata={},
        )


def test_valid_reference_is_internal_and_non_executing() -> None:
    event = _event(
        kind=CollaborationEventKind.APPROVAL_REFERENCE,
        deduplication_key="approval-ref:ok",
        channel_id="",
        metadata={"approval_id": "approval-123"},
    )
    assert event.external_effect is False
    assert event.execution_allowed is False
    assert event.proof_eligible is False
