"""V18 No-Decision / Loss Intelligence (Workstream I / §18).

Track losses/stalls by reason. Each loss creates root-cause hypothesis,
safe improvement and next test. Never auto-relax governance because a deal
was lost.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LossReason(StrEnum):
    NO_REAL_PAIN = "NO_REAL_PAIN"
    NO_URGENCY = "NO_URGENCY"
    WRONG_BUYER = "WRONG_BUYER"
    HIDDEN_BUYER_VETO = "HIDDEN_BUYER_VETO"
    TRUST_GAP = "TRUST_GAP"
    PROOF_GAP = "PROOF_GAP"
    BUDGET = "BUDGET"
    TIMING = "TIMING"
    SECURITY = "SECURITY"
    COMPLIANCE = "COMPLIANCE"
    PROCUREMENT = "PROCUREMENT"
    INTEGRATION_BURDEN = "INTEGRATION_BURDEN"
    CHANGE_BURDEN = "CHANGE_BURDEN"
    COMPETITOR = "COMPETITOR"
    STATUS_QUO = "STATUS_QUO"
    NO_DECISION = "NO_DECISION"
    DEALIX_DELIVERY_GAP = "DEALIX_DELIVERY_GAP"
    BAD_PROPOSAL = "BAD_PROPOSAL"
    BAD_MESSAGE = "BAD_MESSAGE"
    BAD_CHANNEL = "BAD_CHANNEL"
    BAD_FOLLOWUP = "BAD_FOLLOWUP"


_VALID_REASONS = frozenset(r.value for r in LossReason)


@dataclass(frozen=True, slots=True)
class LossEvent:
    account_id: str
    reason: str
    evidence: str = ""
    root_cause_hypothesis: str = ""
    safe_improvement: str = ""
    next_test: str = ""
    governance_unchanged: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "reason": self.reason,
            "evidence": self.evidence,
            "root_cause_hypothesis": self.root_cause_hypothesis,
            "safe_improvement": self.safe_improvement,
            "next_test": self.next_test,
            "governance_unchanged": self.governance_unchanged,
        }


def record_loss(
    account_id: str,
    reason: str,
    *,
    evidence: str = "",
    root_cause_hypothesis: str = "",
    safe_improvement: str = "",
    next_test: str = "",
) -> tuple[LossEvent | None, list[str]]:
    """Deterministic loss recording. Requires a canonical reason and evidence.
    Governance is never relaxed by a loss; that stays explicit."""
    errors: list[str] = []
    if reason not in _VALID_REASONS:
        errors.append(f"INVALID_LOSS_REASON:{reason}")
    if not str(evidence or "").strip():
        errors.append("LOSS_WITHOUT_EVIDENCE")
    if errors:
        return None, errors
    return (
        LossEvent(
            account_id=account_id,
            reason=reason,
            evidence=evidence,
            root_cause_hypothesis=root_cause_hypothesis,
            safe_improvement=safe_improvement,
            next_test=next_test,
            governance_unchanged=True,
        ),
        [],
    )
