"""Distribution funnel — the 12-stage path from target to paid revenue (no LLM, no I/O).

Every distribution motion in Dealix moves a subject through twelve ordered stages.
A stage may only advance to the *immediately next* stage, or drop to a terminal
outcome (``lost`` / ``refer_out``). Skipping ahead or stepping back is rejected —
the funnel is a forward-only ratchet so the pipeline can never claim a stage it
did not actually reach.

Each stage carries seven mandatory properties (owner, status, next_action,
evidence, approval_rule, kpi, failure_mode). A stage without all seven is not
"Full Ops" — it is undefined activity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from auto_client_acquisition.governance_os.approval_matrix import approval_for_action


class FunnelStage(StrEnum):
    """The 12 distribution stages, in canonical forward order."""

    TARGET = "target"
    PAIN_HYPOTHESIS = "pain_hypothesis"
    PROOF_ASSET = "proof_asset"
    MANUAL_OUTREACH = "manual_outreach"
    CONVERSATION = "conversation"
    DEMO_12MIN = "demo_12min"
    PILOT_DIAGNOSTIC = "pilot_diagnostic"
    PAYMENT_COMMITMENT = "payment_commitment"
    DELIVERY = "delivery"
    PROOF_PACK = "proof_pack"
    SPRINT_RETAINER = "sprint_retainer"
    REFERRAL_PARTNER_LOOP = "referral_partner_loop"


# Canonical order — index defines what "next" means.
STAGE_ORDER: tuple[FunnelStage, ...] = tuple(FunnelStage)

# Terminal outcomes reachable from any stage.
TERMINAL: frozenset[str] = frozenset({"lost", "refer_out"})


@dataclass(frozen=True, slots=True)
class StageSpec:
    """The seven mandatory properties of a funnel stage."""

    owner: str
    status: str
    next_action: str
    evidence: str
    approval_rule: str
    kpi: str
    failure_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# The MANUAL_OUTREACH approval rule is derived from the governance approval
# matrix so the funnel can never contradict it. Outreach is an email send →
# ("medium", "human"): human approval required before any external message.
_OUTREACH_RISK, _OUTREACH_ROUTE = approval_for_action("send email")
_OUTREACH_APPROVAL = f"{_OUTREACH_ROUTE} (risk={_OUTREACH_RISK}); draft-only — no live send"


STAGE_PROPERTIES: dict[FunnelStage, StageSpec] = {
    FunnelStage.TARGET: StageSpec(
        owner="founder",
        status="open",
        next_action="Add the account to the War Room table with city, segment, decision maker.",
        evidence="target.added event with account + segment recorded",
        approval_rule="auto — internal record, no external action",
        kpi="targets_added_per_day",
        failure_mode="vague target with no decision maker identified",
    ),
    FunnelStage.PAIN_HYPOTHESIS: StageSpec(
        owner="founder",
        status="open",
        next_action="Write one concrete pain hypothesis for this account.",
        evidence="pain.hypothesized event with the hypothesis text",
        approval_rule="auto — internal record",
        kpi="pain_hypotheses_written",
        failure_mode="generic pain that fits every account (not specific)",
    ),
    FunnelStage.PROOF_ASSET: StageSpec(
        owner="founder",
        status="open",
        next_action="Attach the proof asset that closes a conversation (sample Proof Pack / one-pager).",
        evidence="proof asset reference linked to the target",
        approval_rule="auto — reuse existing approved assets only",
        kpi="targets_with_proof_asset_ready",
        failure_mode="building 20 pages instead of one closing asset",
    ),
    FunnelStage.MANUAL_OUTREACH: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Draft the personalized message; queue for founder approval before sending.",
        evidence="message.drafted then message.approved then message.sent events",
        approval_rule=_OUTREACH_APPROVAL,
        kpi="messages_sent_per_day",
        failure_mode="sending before approval / cold WhatsApp / LinkedIn automation",
    ),
    FunnelStage.CONVERSATION: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Classify the reply and prepare the next follow-up.",
        evidence="reply.received and reply.classified events",
        approval_rule="human — each follow-up draft approved before send",
        kpi="reply_rate",
        failure_mode="no follow-up owner; replies decay unanswered",
    ),
    FunnelStage.DEMO_12MIN: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Run the 12-minute closing demo; end with the pilot ask.",
        evidence="meeting.booked then meeting.held events",
        approval_rule="auto — founder-led live call",
        kpi="demo_rate",
        failure_mode="full product tour instead of a close-focused demo",
    ),
    FunnelStage.PILOT_DIAGNOSTIC: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Send the scope for a single workflow / 10 opportunities.",
        evidence="scope.sent event with the scoped deliverable",
        approval_rule="human — scope reviewed before it is sent",
        kpi="pilot_offer_rate",
        failure_mode="scope too large; offer risk kills the close",
    ),
    FunnelStage.PAYMENT_COMMITMENT: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Send the invoice; record the payment or written commitment.",
        evidence="invoice.sent then invoice.paid or commitment.recorded events",
        approval_rule="human — no live charge; invoice sent manually after approval",
        kpi="payment_or_commitment_rate",
        failure_mode="discounting instead of reducing scope",
    ),
    FunnelStage.DELIVERY: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Deliver the first artifact within 24-48 hours.",
        evidence="delivery artifacts logged against the engagement",
        approval_rule="human — external sends in delivery stay draft-only",
        kpi="time_to_first_delivery_hours",
        failure_mode="waiting weeks; momentum lost after payment",
    ),
    FunnelStage.PROOF_PACK: StageSpec(
        owner="founder",
        status="in_progress",
        next_action="Assemble and deliver the Proof Pack documenting what happened.",
        evidence="proof.pack_requested then proof.pack_delivered events",
        approval_rule="human — final Proof Pack approved before it is shared",
        kpi="proof_pack_delivery_time",
        failure_mode="fake or unevidenced proof; claims without a source",
    ),
    FunnelStage.SPRINT_RETAINER: StageSpec(
        owner="founder",
        status="open",
        next_action="Offer the next rung (Sprint / Retainer) on the back of delivered proof.",
        evidence="deal.proposal_sent event referencing the Proof Pack",
        approval_rule="human — proposal approved before it is sent",
        kpi="upsell_candidate_rate",
        failure_mode="upsell pitched before proof exists",
    ),
    FunnelStage.REFERRAL_PARTNER_LOOP: StageSpec(
        owner="founder",
        status="open",
        next_action="Ask for a referral and open one partner conversation.",
        evidence="referral.requested and partner.conversation_logged events",
        approval_rule="human — partner terms approved individually",
        kpi="referral_rate",
        failure_mode="no loop closed; proof never converted into distribution",
    ),
}


def validate_transition(current: FunnelStage, target: str) -> tuple[bool, str]:
    """Return ``(ok, reason)`` for moving ``current`` -> ``target``.

    Allowed: the immediately next stage in :data:`STAGE_ORDER`, or any
    :data:`TERMINAL` outcome. Skipping ahead or stepping back is rejected.
    """
    if target in TERMINAL:
        return True, "terminal_outcome"
    try:
        target_stage = FunnelStage(target)
    except ValueError:
        return False, f"unknown_target_stage:{target}"
    cur_idx = STAGE_ORDER.index(current)
    tgt_idx = STAGE_ORDER.index(target_stage)
    if tgt_idx == cur_idx + 1:
        return True, "advance_one_stage"
    if tgt_idx <= cur_idx:
        return False, "backward_transition_not_allowed"
    return False, "skip_ahead_not_allowed"


def next_action_for(stage: FunnelStage) -> str:
    """The canonical next action for a stage."""
    return STAGE_PROPERTIES[stage].next_action


def approval_rule_for(stage: FunnelStage) -> str:
    """The canonical approval rule for a stage."""
    return STAGE_PROPERTIES[stage].approval_rule


__all__ = [
    "STAGE_ORDER",
    "STAGE_PROPERTIES",
    "TERMINAL",
    "FunnelStage",
    "StageSpec",
    "approval_rule_for",
    "next_action_for",
    "validate_transition",
]
