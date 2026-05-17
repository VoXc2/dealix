"""Revenue Ops Machine — draft generation + the governance gate.

This module is the SINGLE integration point between the machine and the
outreach queue. It is the hard guarantee behind "drafts + queue only":

  * Every draft is run through claim-safety (``governance_os``).
  * A forbidden *claim* (guaranteed results, fake proof) -> BLOCK; the draft is
    dropped and a ``RISK_BLOCKED`` proof event is produced.
  * Every surviving draft becomes an ``OutreachQueueRecord`` with
    ``approval_required=True`` and ``status="queued"``.
  * Nothing here ever sets ``status="sent"`` or calls a send function.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
    governance_decision_for_pii_external,
)
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
from auto_client_acquisition.proof_ledger.schemas import ProofEvent, ProofEventType
from db.models import OutreachQueueRecord

# Channels that leave Dealix and therefore always require founder approval.
_EXTERNAL_CHANNELS = frozenset({"email", "whatsapp", "linkedin", "sms"})


@dataclass(frozen=True, slots=True)
class DraftSpec:
    """An un-gated draft produced by an ops handler."""

    kind: str
    channel: str
    message: str

    @property
    def is_external(self) -> bool:
        return self.channel in _EXTERNAL_CHANNELS


@dataclass(frozen=True, slots=True)
class GatedDraft:
    """A draft after the governance gate has classified it."""

    spec: DraftSpec
    decision: GovernanceDecision
    blocked: bool
    issues: tuple[str, ...] = field(default_factory=tuple)


def gate_specs(specs: list[DraftSpec]) -> list[GatedDraft]:
    """Run claim-safety + the governance router over every draft. Pure."""
    gated: list[GatedDraft] = []
    for spec in specs:
        safety = audit_claim_safety(spec.message)
        if safety.suggested_decision == GovernanceDecision.BLOCK:
            gated.append(GatedDraft(spec, GovernanceDecision.BLOCK, True, safety.issues))
            continue
        # Every machine draft is treated as PII-bearing; external drafts also
        # request an external action. Both paths land on a human-approval gate.
        decision = governance_decision_for_pii_external(
            contains_pii=True,
            external_action_requested=spec.is_external,
            passport_external_allowed=True,
        )
        gated.append(GatedDraft(spec, decision, False, safety.issues))
    return gated


def to_outreach_records(gated: list[GatedDraft], lead_id: str) -> list[OutreachQueueRecord]:
    """Build queued ``OutreachQueueRecord`` rows for every non-blocked draft.

    Rows are returned un-committed. ``status`` is always ``"queued"`` and
    ``approval_required`` is always ``True`` — this function never sends.
    """
    records: list[OutreachQueueRecord] = []
    for g in gated:
        if g.blocked:
            continue
        records.append(
            OutreachQueueRecord(
                id=f"oq_{uuid4().hex[:24]}",
                lead_id=lead_id,
                channel=g.spec.channel,
                message=g.spec.message,
                approval_required=True,
                status="queued",
                risk_reason=f"{g.spec.kind}:{g.decision}",
            )
        )
    return records


def blocked_proof_events(
    gated: list[GatedDraft], customer_handle: str = "Saudi B2B customer"
) -> list[ProofEvent]:
    """A ``RISK_BLOCKED`` proof event for every draft the gate dropped."""
    events: list[ProofEvent] = []
    for g in gated:
        if not g.blocked:
            continue
        events.append(
            ProofEvent(
                event_type=ProofEventType.RISK_BLOCKED,
                customer_handle=customer_handle,
                summary_en=(f"Draft '{g.spec.kind}' blocked by claim-safety gate."),
                summary_ar="تم حظر مسودة بسبب فحص سلامة الادعاءات.",
                evidence_source="revenue_ops_machine.drafts.gate_specs",
                risk_level="high",
                payload={"kind": g.spec.kind, "issues": list(g.issues)},
            )
        )
    return events


__all__ = [
    "DraftSpec",
    "GatedDraft",
    "gate_specs",
    "to_outreach_records",
    "blocked_proof_events",
]
