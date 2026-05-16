"""Doctrine tests for the Governed Revenue Ops engagement state machine.

Asserts the non-negotiables hold:
- `draft → sent` is impossible (no send without approval).
- No state may be skipped.
- `invoice_paid` is terminal.
- The diagnostic carries the bilingual disclaimer and source_refs.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_ops.diagnostics import run_diagnostic
from auto_client_acquisition.revenue_ops.state_machine import (
    ENGAGEMENT_STATES,
    EngagementStateError,
    next_states,
    validate_transition,
)


def test_draft_cannot_skip_to_sent() -> None:
    """No external send is reachable without an explicit approval."""
    with pytest.raises(EngagementStateError):
        validate_transition("draft", "sent")


def test_draft_to_approved_allowed() -> None:
    validate_transition("draft", "approved")


def test_approved_to_sent_allowed() -> None:
    validate_transition("approved", "sent")


def test_no_state_skip() -> None:
    """Every transition must be one linear step forward."""
    with pytest.raises(EngagementStateError):
        validate_transition("sent", "scope_requested")
    with pytest.raises(EngagementStateError):
        validate_transition("used_in_meeting", "invoice_sent")


def test_invoice_paid_is_terminal() -> None:
    assert next_states("invoice_paid") == frozenset()
    with pytest.raises(EngagementStateError):
        validate_transition("invoice_paid", "draft")


def test_rejection_rollback_allowed() -> None:
    """A pending-approval item may be rejected back to draft."""
    validate_transition("approved", "draft")


def test_full_happy_path_walks_every_state() -> None:
    chain = list(ENGAGEMENT_STATES)
    for current, target in zip(chain, chain[1:]):
        validate_transition(current, target)


def test_unknown_state_rejected() -> None:
    with pytest.raises(EngagementStateError):
        validate_transition("draft", "shipped")
    with pytest.raises(EngagementStateError):
        validate_transition("nonsense", "draft")


def test_diagnostic_findings_carry_source_ref() -> None:
    result = run_diagnostic(
        "rvo_test",
        crm_rows=[{"company_name": "Acme", "stage": "", "owner": "", "amount": "", "last_activity_at": ""}],
        ai_usage_ungoverned=True,
        has_decision_trail=False,
    )
    assert result.findings, "expected findings for an incomplete CRM export"
    for finding in result.findings:
        assert finding.source_ref, "every finding must carry a source_ref"
        assert finding.severity in {"low", "medium", "high"}


def test_diagnostic_carries_bilingual_disclaimer() -> None:
    result = run_diagnostic("rvo_test", crm_rows=[])
    assert result.to_dict()["disclaimer"] == (
        "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"
    )


def test_diagnostic_recommends_a_catalog_service() -> None:
    result = run_diagnostic("rvo_test", crm_rows=[])
    assert result.recommended_next in {"revenue_intelligence_sprint", "governed_ops_retainer"}
