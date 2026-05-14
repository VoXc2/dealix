"""Event signals → recommended executive / operator decisions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionDecision:
    decision: str
    target: str
    reason: str
    action: str
    risk_note: str


def recommend_decisions(
    *,
    data_quality_score: int | None = None,
    proof_strength: int | None = None,
    client_health: int | None = None,
    manual_step_repeat_count: int | None = None,
    blocked_action_repeat_count: int | None = None,
    paid_clients: int | None = None,
    retainer_count: int | None = None,
) -> tuple[ExecutionDecision, ...]:
    """Deterministic rules mirroring docs/execution/EVENT_TO_DECISION_SYSTEM.md."""
    out: list[ExecutionDecision] = []

    if data_quality_score is not None and data_quality_score < 60:
        out.append(
            ExecutionDecision(
                decision="DATA_READINESS_FIRST",
                target="client_onboarding",
                reason=f"data_quality_score={data_quality_score} below 60",
                action="Recommend Data Readiness work before governed AI workflow.",
                risk_note="Downstream models and workflows amplify bad inputs.",
            ),
        )

    if (
        proof_strength is not None
        and client_health is not None
        and proof_strength > 85
        and client_health > 70
    ):
        out.append(
            ExecutionDecision(
                decision="RECOMMEND_RETAINER",
                target="account_expansion",
                reason="Strong proof and healthy client relationship.",
                action="Propose monthly operating retainer with explicit monthly value.",
                risk_note="Ensure Proof Pack and governance baselines stay current.",
            ),
        )

    if manual_step_repeat_count is not None and manual_step_repeat_count >= 3:
        out.append(
            ExecutionDecision(
                decision="PRODUCTIZE",
                target="internal_workflow",
                reason=f"Manual step repeated {manual_step_repeat_count}+ times.",
                action="Create productization candidate; scope module + test harness.",
                risk_note="Validate revenue link and governance before build.",
            ),
        )

    if blocked_action_repeat_count is not None and blocked_action_repeat_count >= 2:
        out.append(
            ExecutionDecision(
                decision="TIGHTEN_GOVERNANCE",
                target="policy_engine",
                reason="Repeated blocked actions indicate pattern risk.",
                action="Add/adjust governance rule; prepare sales objection response.",
                risk_note="Document audit trail for policy change.",
            ),
        )

    if paid_clients is not None and retainer_count is not None:
        if paid_clients >= 5 and retainer_count >= 2:
            out.append(
                ExecutionDecision(
                    decision="VENTURE_REVIEW",
                    target="business_unit",
                    reason="Paid traction + recurring retainers.",
                    action="Run venture candidate review (module, playbook, margin, owner).",
                    risk_note="No spinout without Venture Gate checklist.",
                ),
            )

    return tuple(out)
