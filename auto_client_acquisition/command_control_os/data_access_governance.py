"""Data Access Governance — deny-by-default decisions.

See ``docs/command_control/DATA_ACCESS_GOVERNANCE.md``. Builds on the
``global_grade_os.enterprise_trust.SourcePassport`` schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from auto_client_acquisition.global_grade_os.enterprise_trust import (
    AllowedUse,
    SourcePassport,
)


class DataAccessDecision(str, Enum):
    APPROVE = "APPROVE"
    DENY = "DENY"
    CONDITIONAL = "CONDITIONAL"


@dataclass(frozen=True)
class DataAccessRequest:
    requester: str
    requested_use: AllowedUse
    passport: SourcePassport | None
    business_purpose: str
    pii_checked: bool
    audit_event_id: str | None
    conditions: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DataAccessRecord:
    decision: DataAccessDecision
    reasons: tuple[str, ...]
    conditions: tuple[str, ...] = ()


def evaluate_data_access(request: DataAccessRequest) -> DataAccessRecord:
    """Apply the deny-by-default rule from the doctrine.

    Returns ``DENY`` unless every precondition is satisfied. Returns
    ``CONDITIONAL`` when the passport permits use but the request carries
    explicit conditions that must travel with the approval.
    """

    reasons: list[str] = []

    if request.passport is None:
        reasons.append("missing_passport")
    else:
        if not request.passport.ai_access_allowed:
            reasons.append("ai_access_not_allowed_on_passport")
        if not request.passport.permits(request.requested_use):
            reasons.append("requested_use_not_in_allowed_use")
        if (
            request.passport.contains_pii
            and request.requested_use is AllowedUse.PUBLIC_PUBLICATION
        ):
            reasons.append("pii_cannot_be_published")

    if not request.business_purpose:
        reasons.append("business_purpose_required")
    if not request.pii_checked:
        reasons.append("pii_check_required")
    if not request.audit_event_id:
        reasons.append("audit_event_required")

    if reasons:
        return DataAccessRecord(decision=DataAccessDecision.DENY, reasons=tuple(reasons))

    if request.conditions:
        return DataAccessRecord(
            decision=DataAccessDecision.CONDITIONAL,
            reasons=("preconditions_met_with_conditions",),
            conditions=request.conditions,
        )

    return DataAccessRecord(
        decision=DataAccessDecision.APPROVE,
        reasons=("all_preconditions_met",),
    )
