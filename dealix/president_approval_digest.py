"""Founder-facing President digest with evidence-bound truth and WIP controls.

The projection is read-only. It does not approve, send, merge, deploy, spend, or
mutate company truth. It compresses already-classified company state into the
five founder surfaces: MONEY / DECISIONS / RISKS / APPROVALS / NEXT ACTION.

Truth boundary:
- caller-supplied numerics are not verified money without payment evidence;
- caller-supplied movement is not verified movement without movement evidence;
- approval rows are projections of canonical approval evidence, never grants;
- WIP limits are supplied with source/evidence refs rather than owned here.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Literal

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

WorkKind = Literal["company_p0", "build_pr", "experiment", "other"]
WorkStatus = Literal["active", "blocked", "done", "stopped"]
MoneyEvidenceClass = Literal[
    "PAYMENT_EVIDENCE",
    "INVOICE",
    "PROPOSAL",
    "CRM_AMOUNT",
    "ANALYTICS_EVENT",
    "UNKNOWN",
]
MovementTruthClass = Literal[
    "VERIFIED_ECONOMIC_MOVEMENT",
    "UNKNOWN_NOT_EVIDENCE_BACKED",
]
ApprovalState = Literal["PENDING", "REVOKED", "EXPIRED", "UNKNOWN"]


def _parse_aware_timestamp(value: str, *, field: str) -> datetime:
    text = value.strip()
    if not text:
        raise ValueError(f"{field} is required")
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _iso_utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _non_empty_refs(values: tuple[str, ...], *, field: str) -> tuple[str, ...]:
    refs = tuple(ref.strip() for ref in values if ref.strip())
    if not refs or len(refs) != len(values):
        raise ValueError(f"{field} must contain non-empty evidence references")
    return refs


@dataclass(frozen=True)
class MoneySnapshot:
    """Read-only projection of canonical economic truth.

    Only PAYMENT_EVIDENCE with non-empty refs can be projected as verified
    money. Invoice/proposal/CRM/analytics amounts remain unknown.
    """

    revenue_sar: float | None
    paid_pilots: int | None
    evidence_class: MoneyEvidenceClass
    evidence_refs: tuple[str, ...]
    as_of: str

    def __post_init__(self) -> None:
        if self.revenue_sar is not None and self.revenue_sar < 0:
            raise ValueError("revenue_sar must be non-negative")
        if self.paid_pilots is not None and self.paid_pilots < 0:
            raise ValueError("paid_pilots must be non-negative")
        _parse_aware_timestamp(self.as_of, field="money.as_of")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("money evidence_refs cannot contain empty refs")

    def project(self) -> dict[str, object]:
        verified = (
            self.evidence_class == "PAYMENT_EVIDENCE"
            and bool(self.evidence_refs)
            and self.revenue_sar is not None
            and self.paid_pilots is not None
        )
        return {
            "verified_revenue_sar": self.revenue_sar if verified else UNKNOWN,
            "verified_paid_pilots": self.paid_pilots if verified else UNKNOWN,
            "truth_state": "VERIFIED_PAYMENT_EVIDENCE" if verified else UNKNOWN,
            "evidence_class": self.evidence_class,
            "evidence_refs": list(self.evidence_refs),
            "as_of": _iso_utc(_parse_aware_timestamp(self.as_of, field="money.as_of")),
            "projection_only": True,
        }


@dataclass(frozen=True)
class WipPolicy:
    """Read-only projection of the canonical portfolio/Company Machine policy."""

    max_company_p0s: int
    max_build_prs_per_owner: int
    max_experiments_per_funnel_stage: int
    source_ref: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if min(
            self.max_company_p0s,
            self.max_build_prs_per_owner,
            self.max_experiments_per_funnel_stage,
        ) < 1:
            raise ValueError("WIP limits must be positive")
        if not self.source_ref.strip():
            raise ValueError("WIP policy source_ref is required")
        _non_empty_refs(self.evidence_refs, field="WIP policy evidence_refs")


@dataclass(frozen=True)
class ApprovalRequest:
    approval_id: str
    action_fingerprint: str
    exact_scope: str
    authority_class: str
    evidence_refs: tuple[str, ...]
    risk_class: str
    expires_at: str
    approval_state: ApprovalState
    state_checked_at: str
    approval_state_ref: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.approval_id, "approval_id"),
            (self.action_fingerprint, "action_fingerprint"),
            (self.exact_scope, "exact_scope"),
            (self.authority_class, "authority_class"),
            (self.risk_class, "risk_class"),
            (self.expires_at, "expires_at"),
            (self.state_checked_at, "state_checked_at"),
            (self.approval_state_ref, "approval_state_ref"),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        _non_empty_refs(self.evidence_refs, field="approval evidence_refs")
        _parse_aware_timestamp(self.expires_at, field="approval.expires_at")
        _parse_aware_timestamp(self.state_checked_at, field="approval.state_checked_at")


@dataclass(frozen=True)
class WorkItem:
    work_id: str
    kind: WorkKind
    owner: str
    status: WorkStatus
    next_action: str
    priority_score: float
    evidence_refs: tuple[str, ...]
    verified_movement: float = 0.0
    movement_truth_class: MovementTruthClass = "UNKNOWN_NOT_EVIDENCE_BACKED"
    movement_evidence_refs: tuple[str, ...] = ()
    founder_minutes: float = 0.0
    cost: float = 0.0
    uncertainty: float = 0.0
    risk: float = 0.0
    funnel_stage: str = ""
    review_after_founder_minutes: float | None = None
    review_after_cost: float | None = None
    max_uncertainty: float | None = None
    max_risk: float | None = None

    def __post_init__(self) -> None:
        if not self.work_id.strip() or not self.owner.strip() or not self.next_action.strip():
            raise ValueError("work_id, owner and next_action are required")
        _non_empty_refs(self.evidence_refs, field="work evidence_refs")
        for value, name in (
            (self.priority_score, "priority_score"),
            (self.verified_movement, "verified_movement"),
            (self.founder_minutes, "founder_minutes"),
            (self.cost, "cost"),
            (self.uncertainty, "uncertainty"),
            (self.risk, "risk"),
        ):
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.kind == "experiment" and not self.funnel_stage.strip():
            raise ValueError("experiment work requires funnel_stage")
        if any(not ref.strip() for ref in self.movement_evidence_refs):
            raise ValueError("movement_evidence_refs cannot contain empty refs")

    def has_verified_movement(self) -> bool:
        return (
            self.verified_movement > 0
            and self.movement_truth_class == "VERIFIED_ECONOMIC_MOVEMENT"
            and bool(self.movement_evidence_refs)
        )

    def requires_review_or_stop(self) -> bool:
        if self.status != "active" or self.has_verified_movement():
            return False
        return any(
            (
                self.review_after_founder_minutes is not None
                and self.founder_minutes >= self.review_after_founder_minutes,
                self.review_after_cost is not None and self.cost >= self.review_after_cost,
                self.max_uncertainty is not None and self.uncertainty >= self.max_uncertainty,
                self.max_risk is not None and self.risk >= self.max_risk,
            )
        )


@dataclass(frozen=True)
class PresidentDigest:
    money: dict[str, object]
    decisions: tuple[dict[str, object], ...]
    risks: tuple[dict[str, object], ...]
    approvals: tuple[dict[str, object], ...]
    next_action: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "MONEY": self.money,
            "DECISIONS": list(self.decisions),
            "RISKS": list(self.risks),
            "APPROVALS": list(self.approvals),
            "NEXT_ACTION": self.next_action,
        }


def build_president_digest(
    *,
    money: MoneySnapshot,
    work_items: tuple[WorkItem, ...],
    approvals: tuple[ApprovalRequest, ...],
    wip_policy: WipPolicy,
    evaluated_at: str,
) -> PresidentDigest:
    """Build the five-surface digest without manufacturing truth or authority."""
    evaluated = _parse_aware_timestamp(evaluated_at, field="evaluated_at")
    active = tuple(item for item in work_items if item.status == "active")
    risks: list[dict[str, object]] = []
    decisions: list[dict[str, object]] = []

    active_p0 = [item for item in active if item.kind == "company_p0"]
    if len(active_p0) > wip_policy.max_company_p0s:
        risks.append(
            {
                "code": "COMPANY_P0_WIP_EXCEEDED",
                "limit": wip_policy.max_company_p0s,
                "active": len(active_p0),
                "policy_source_ref": wip_policy.source_ref,
                "required_decision": "STOP_OR_DOWNGRADE_EXCESS_P0",
            }
        )

    build_counts = Counter(item.owner for item in active if item.kind == "build_pr")
    for owner, count in sorted(build_counts.items()):
        if count > wip_policy.max_build_prs_per_owner:
            risks.append(
                {
                    "code": "BUILD_PR_WIP_EXCEEDED",
                    "owner": owner,
                    "limit": wip_policy.max_build_prs_per_owner,
                    "active": count,
                    "policy_source_ref": wip_policy.source_ref,
                    "required_decision": "CLOSE_MERGE_DECISION_OR_STOP_BEFORE_NEW_BUILD",
                }
            )

    experiment_counts = Counter(item.funnel_stage for item in active if item.kind == "experiment")
    for stage, count in sorted(experiment_counts.items()):
        if count > wip_policy.max_experiments_per_funnel_stage:
            risks.append(
                {
                    "code": "FUNNEL_EXPERIMENT_WIP_EXCEEDED",
                    "funnel_stage": stage,
                    "limit": wip_policy.max_experiments_per_funnel_stage,
                    "active": count,
                    "policy_source_ref": wip_policy.source_ref,
                    "required_decision": "KEEP_ONE_EXPERIMENT_AND_STOP_OR_RETEST_THE_REST",
                }
            )

    review_items = sorted(
        (item for item in active if item.requires_review_or_stop()),
        key=lambda item: (-item.priority_score, item.work_id),
    )
    for item in review_items:
        decisions.append(
            {
                "work_id": item.work_id,
                "decision": "REVIEW_OR_STOP",
                "reason": "NO_VERIFIED_MOVEMENT_BEYOND_DECLARED_COST_TIME_UNCERTAINTY_OR_RISK_BOUNDARY",
                "movement_truth_class": item.movement_truth_class,
                "movement_evidence_refs": list(item.movement_evidence_refs),
                "founder_minutes": item.founder_minutes,
                "cost": item.cost,
                "uncertainty": item.uncertainty,
                "risk": item.risk,
            }
        )

    seen_fingerprints: set[str] = set()
    approval_rows: list[dict[str, object]] = []
    for approval in sorted(approvals, key=lambda item: (item.risk_class, item.approval_id)):
        if approval.action_fingerprint in seen_fingerprints:
            raise ValueError("duplicate action_fingerprint in approval digest")
        seen_fingerprints.add(approval.action_fingerprint)

        expiry = _parse_aware_timestamp(approval.expires_at, field="approval.expires_at")
        state_checked = _parse_aware_timestamp(
            approval.state_checked_at,
            field="approval.state_checked_at",
        )
        lifecycle_state: ApprovalState = approval.approval_state
        if state_checked > evaluated:
            lifecycle_state = "UNKNOWN"
        elif lifecycle_state == "PENDING" and expiry <= evaluated:
            lifecycle_state = "EXPIRED"

        actionable_pending = lifecycle_state == "PENDING" and expiry > evaluated
        row = asdict(approval)
        row["evidence_refs"] = list(approval.evidence_refs)
        row["lifecycle_state"] = lifecycle_state
        row["actionable_pending"] = actionable_pending
        row["approval_granted"] = False
        row["execution_performed"] = False
        row["projection_only"] = True
        approval_rows.append(row)

    candidates = sorted(
        (item for item in active if not item.requires_review_or_stop()),
        key=lambda item: (-item.priority_score, item.work_id),
    )
    if review_items:
        highest = review_items[0]
        next_action = {
            "work_id": highest.work_id,
            "action": "REVIEW_OR_STOP",
            "execution_authority": False,
        }
    elif candidates:
        highest = candidates[0]
        next_action = {
            "work_id": highest.work_id,
            "action": highest.next_action,
            "execution_authority": False,
        }
    else:
        next_action = {
            "work_id": "",
            "action": "NO_EVIDENCE_BACKED_ACTIVE_ACTION",
            "execution_authority": False,
        }

    return PresidentDigest(
        money=money.project(),
        decisions=tuple(decisions),
        risks=tuple(risks),
        approvals=tuple(approval_rows),
        next_action=next_action,
    )


__all__ = [
    "UNKNOWN",
    "ApprovalRequest",
    "MoneySnapshot",
    "PresidentDigest",
    "WipPolicy",
    "WorkItem",
    "build_president_digest",
]
