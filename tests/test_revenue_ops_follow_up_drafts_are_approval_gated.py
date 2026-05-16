"""Follow-up drafts must be approval-gated and governance-audited; never auto-sent."""

from __future__ import annotations

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.revenue_ops.follow_up_drafts import (
    generate_follow_up_drafts,
)


def test_generated_drafts_are_approval_required() -> None:
    drafts = generate_follow_up_drafts(diagnostic_id="diag_1", customer_id="c1")
    assert drafts, "expected at least one follow-up draft"
    for d in drafts:
        assert d.requires_approval is True
        assert d.action_mode == "approval_required"


def test_generated_drafts_pass_governance_audit() -> None:
    drafts = generate_follow_up_drafts(diagnostic_id="diag_1", customer_id="c1")
    for d in drafts:
        # Drafts are clean per their own audit.
        assert d.governance_clean is True
        assert d.governance_issues == ()
        # Re-audit the rendered text independently — still clean.
        issues = audit_draft_text(f"{d.subject}\n{d.body}")
        assert issues == [], f"draft {d.draft_id} has governance issues: {issues}"


def test_draft_serialization_never_marks_as_sent() -> None:
    drafts = generate_follow_up_drafts(diagnostic_id="diag_1", customer_id="c1")
    for d in drafts:
        payload = d.to_dict()
        assert payload["requires_approval"] is True
        # No "sent" / auto-send flag is ever set on a generated draft.
        assert "sent_at" not in payload
        assert payload.get("action_mode") == "approval_required"


def test_extra_context_is_carried_but_still_audited() -> None:
    drafts = generate_follow_up_drafts(
        diagnostic_id="diag_1",
        customer_id="c1",
        extra_context="Happy to align on scope this week.",
    )
    for d in drafts:
        assert "scope this week" in d.body
        assert d.governance_clean is True


def test_draft_with_forbidden_phrasing_is_flagged_not_sent() -> None:
    # Sanity: the audit catches forbidden phrasing if it ever appeared.
    issues = audit_draft_text("We guarantee roi and will auto-send this.")
    assert issues, "audit_draft_text should flag forbidden phrasing"
