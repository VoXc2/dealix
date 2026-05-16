"""Governed follow-up draft generation for the Revenue Ops Diagnostic.

Drafts are generated as approval-required items only. Every draft is audited by
`governance_os.draft_gate.audit_draft_text`; a draft with governance issues is
returned with `approved=False` and its issues, never auto-sent. Sending a draft
always requires a separate, explicit founder approval downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text

# Every follow-up draft is an approval-required action. Nothing auto-sends.
_ACTION_MODE = "approval_required"


@dataclass(frozen=True)
class FollowUpDraft:
    """One follow-up draft staged for founder approval. Never auto-sent."""

    draft_id: str
    channel: str
    subject: str
    body: str
    action_mode: str = _ACTION_MODE
    requires_approval: bool = True
    governance_clean: bool = True
    governance_issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "draft_id": self.draft_id,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "action_mode": self.action_mode,
            "requires_approval": self.requires_approval,
            "governance_clean": self.governance_clean,
            "governance_issues": list(self.governance_issues),
        }


# Draft templates — channel, subject, body. Deliberately conservative copy:
# no metric claims, no guarantee language. The diagnostic_id is interpolated.
_TEMPLATES: tuple[tuple[str, str, str], ...] = (
    (
        "email",
        "Your Governed Revenue Ops Diagnostic — next step",
        "Thank you for the time on the diagnostic. We have prepared a short "
        "summary of the revenue workflow review and a recommended next step. "
        "May we share it for your review?",
    ),
    (
        "email",
        "Diagnostic summary ready for your review",
        "The decision passport from the diagnostic is ready. It outlines the "
        "pipeline risks we reviewed and a recommended next step. Would a brief "
        "call this week suit you?",
    ),
)


def generate_follow_up_drafts(
    *,
    diagnostic_id: str,
    customer_id: str,
    extra_context: str = "",
) -> list[FollowUpDraft]:
    """Generate governed follow-up drafts as approval-required items.

    Args:
        diagnostic_id: the diagnostic the drafts belong to.
        customer_id: the Dealix customer.
        extra_context: optional founder-supplied context appended to each body.

    Returns:
        A list of `FollowUpDraft`. Each is audited by `audit_draft_text`;
        none is sent. A draft with governance issues carries
        `governance_clean=False` and the issue list.
    """
    drafts: list[FollowUpDraft] = []
    for idx, (channel, subject, body) in enumerate(_TEMPLATES):
        full_body = body
        if extra_context.strip():
            full_body = f"{body}\n\n{extra_context.strip()}"
        issues = audit_draft_text(f"{subject}\n{full_body}")
        drafts.append(
            FollowUpDraft(
                draft_id=f"{diagnostic_id}_draft_{idx + 1}",
                channel=channel,
                subject=subject,
                body=full_body,
                governance_clean=not issues,
                governance_issues=tuple(issues),
            )
        )
    return drafts
