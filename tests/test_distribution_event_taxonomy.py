"""Distribution OS — new event types are registered and constructible."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_memory.events import EVENT_TYPES, make_event

_DISTRIBUTION_EVENT_TYPES = (
    "target.added",
    "pain.hypothesized",
    "proof.pack_requested",
    "proof.pack_delivered",
    "scope.sent",
    "invoice.sent",
    "invoice.paid",
    "commitment.recorded",
    "partner.conversation_logged",
    "partner.classified",
    "referral.requested",
    "affiliate.application_received",
    "commission.eligibility_checked",
)


def test_distribution_event_types_registered() -> None:
    for event_type in _DISTRIBUTION_EVENT_TYPES:
        assert event_type in EVENT_TYPES, f"{event_type} missing from EVENT_TYPES"


def test_make_event_builds_each_distribution_type() -> None:
    for event_type in _DISTRIBUTION_EVENT_TYPES:
        evt = make_event(
            event_type=event_type,
            customer_id="dealix_founder",
            subject_type="account",
            subject_id="acc_1",
        )
        assert evt.event_type == event_type
        assert evt.event_id.startswith("evt_")


def test_unknown_event_type_still_rejected() -> None:
    with pytest.raises(ValueError, match="unknown event_type"):
        make_event(
            event_type="bogus.thing",
            customer_id="dealix_founder",
            subject_type="account",
            subject_id="acc_1",
        )


def test_event_types_has_no_duplicates() -> None:
    assert len(EVENT_TYPES) == len(set(EVENT_TYPES))
