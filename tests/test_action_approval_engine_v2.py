"""Wave 12 §32.3.6 (Engine 6) — Action & Approval Engine v2 hardening tests.

Validates the schema extension (action_id, lead_id, customer_id, due_date,
audit_ref, proof_target) + ActionType Literal enum + is_canonical_action_type
helper, all per plan §32.3.6.

Reuses existing v1 ApprovalRequest; v2 fields all default to None so old
callers keep working unchanged.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from auto_client_acquisition.approval_center import (
    ActionType,
    ApprovalRequest,
    ApprovalStatus,
    is_canonical_action_type,
)


# ─────────────────────────────────────────────────────────────────────
# Schema extensions (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_v1_callers_still_work_via_defaults() -> None:
    """Backward-compat: a request built with the v1 fields only must
    succeed (all 6 new fields default to None)."""
    r = ApprovalRequest(
        object_type="message_draft",
        object_id="msg_test",
        action_type="draft_email",
    )
    # Existing v1 fields preserved
    assert r.object_type == "message_draft"
    assert r.action_type == "draft_email"
    assert r.action_mode == "approval_required"
    assert r.status == ApprovalStatus.PENDING
    # All 6 new v2 fields default to None
    assert r.action_id is None
    assert r.lead_id is None
    assert r.customer_id is None
    assert r.due_date is None
    assert r.audit_ref is None
    assert r.proof_target is None


def test_v2_fields_settable_with_values() -> None:
    """Wave 12 §32.3.6 — all 6 hardening fields can be set on construction."""
    deadline = datetime.now(timezone.utc) + timedelta(days=2)
    r = ApprovalRequest(
        object_type="message_draft",
        object_id="msg_v2",
        action_type="draft_linkedin_manual",
        action_id="act_xyz123",
        lead_id="lead_acme_001",
        customer_id="cust_acme_real_estate",
        due_date=deadline,
        audit_ref="radar_event_42",
        proof_target="reply_received",
    )
    assert r.action_id == "act_xyz123"
    assert r.lead_id == "lead_acme_001"
    assert r.customer_id == "cust_acme_real_estate"
    assert r.due_date == deadline
    assert r.audit_ref == "radar_event_42"
    assert r.proof_target == "reply_received"


def test_extra_fields_still_forbidden() -> None:
    """The schema's ``extra='forbid'`` must still reject unknown fields
    (so we don't silently accept typos like ``action_idd`` or ``lead``)."""
    with pytest.raises(ValidationError):
        ApprovalRequest(
            object_type="x",
            object_id="y",
            action_type="z",
            unknown_field="oops",  # type: ignore[call-arg]
        )


def test_approval_id_separate_from_action_id() -> None:
    """Hard rule: action_id is NOT approval_id.

    A single action can have N approvals over time (customer rejects,
    founder revises, customer re-approves) — the approval_id changes
    per cycle but action_id stays the same.
    """
    deadline = datetime.now(timezone.utc) + timedelta(hours=1)
    r1 = ApprovalRequest(
        object_type="msg",
        object_id="m1",
        action_type="draft_email",
        action_id="act_persistent_001",
        due_date=deadline,
    )
    r2 = ApprovalRequest(
        object_type="msg",
        object_id="m1",  # same underlying object
        action_type="draft_email",
        action_id="act_persistent_001",  # same action_id (revision cycle)
        due_date=deadline,
    )
    # approval_ids are distinct (auto-generated)
    assert r1.approval_id != r2.approval_id
    # action_ids match (same underlying action, different approval cycles)
    assert r1.action_id == r2.action_id == "act_persistent_001"


# ─────────────────────────────────────────────────────────────────────
# ActionType canonical enum (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_canonical_action_type_recognized() -> None:
    """All 11 canonical Wave 12 action types pass is_canonical_action_type()."""
    canonical = [
        "prepare_diagnostic", "draft_email", "draft_linkedin_manual",
        "call_script", "follow_up_task", "support_reply_draft",
        "payment_reminder", "delivery_task", "proof_request",
        "upsell_recommendation", "partner_intro",
    ]
    for action in canonical:
        assert is_canonical_action_type(action), \
            f"{action} should be canonical per Wave 12 §32.3.6"


def test_non_canonical_action_type_rejected_by_helper() -> None:
    """Free-form / legacy / unsafe action types do NOT pass is_canonical."""
    non_canonical = [
        "send_message_now",      # never a valid action — implies live send
        "blast_email",           # NO_BLAST violation
        "scrape_linkedin",       # NO_SCRAPING violation
        "auto_charge",           # NO_LIVE_CHARGE violation
        "",                      # empty
        "DRAFT_EMAIL",           # case mismatch
        "draft email",           # space mismatch
    ]
    for action in non_canonical:
        assert not is_canonical_action_type(action), \
            f"{action!r} must NOT be marked canonical (potential gate violation)"


def test_legacy_free_form_action_type_still_accepted_by_schema() -> None:
    """Backward-compat: schema still accepts ``action_type`` as ``str``
    (existing callers pass arbitrary strings). The Literal ActionType
    is for new type-checked code; the helper is_canonical_action_type
    flags legacy values."""
    # This must NOT raise — backward compat
    r = ApprovalRequest(
        object_type="legacy_object",
        object_id="leg_001",
        action_type="some_legacy_action_name",  # not canonical but accepted
    )
    assert r.action_type == "some_legacy_action_name"
    # Helper correctly flags it as non-canonical
    assert not is_canonical_action_type(r.action_type)


def test_action_type_literal_exported_for_type_checking() -> None:
    """ActionType Literal is exported from the package for downstream
    type annotations (Engines 4-12 will reference it)."""
    from auto_client_acquisition.approval_center import ActionType as Imported
    # Literal types don't have runtime introspection in old Pythons, but
    # we can verify the import succeeds (which it must for type checkers)
    assert Imported is ActionType


# ─────────────────────────────────────────────────────────────────────
# Total: 8 tests (4 schema + 4 ActionType enum)
# ─────────────────────────────────────────────────────────────────────
