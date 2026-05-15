"""Deterministic stage progression for the Transformation System.

Linear, no skipping. A stage transition is rejected unless verified
evidence for the stage being closed is supplied — this honors
``no_unverified_outcomes``: no growth without proof.
"""

from __future__ import annotations

from auto_client_acquisition.transformation_os.schemas import (
    StageEvidence,
    TransformationRecord,
    TransformationStage,
)

# Linear progression — each stage may only advance to the next one.
ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    TransformationStage.ASSESSMENT.value: (TransformationStage.PILOT.value,),
    TransformationStage.PILOT.value: (TransformationStage.WORKFLOW_REDESIGN.value,),
    TransformationStage.WORKFLOW_REDESIGN.value: (
        TransformationStage.OPERATIONAL_DEPLOYMENT.value,
    ),
    TransformationStage.OPERATIONAL_DEPLOYMENT.value: (
        TransformationStage.GOVERNANCE_SCALE.value,
    ),
    TransformationStage.GOVERNANCE_SCALE.value: (),
}


def can_advance(
    record: TransformationRecord,
    target_stage: str,
    evidence: list[StageEvidence],
) -> tuple[bool, list[str]]:
    """Check whether ``record`` may advance to ``target_stage``.

    Returns ``(allowed, reasons)``. ``reasons`` is empty when allowed.
    """
    reasons: list[str] = []

    valid_stages = {s.value for s in TransformationStage}
    if target_stage not in valid_stages:
        reasons.append(f"unknown target stage: {target_stage}")
        return False, reasons

    allowed = ALLOWED_TRANSITIONS.get(record.current_stage, ())
    if target_stage not in allowed:
        reasons.append(
            f"transition {record.current_stage} -> {target_stage} not allowed; "
            f"valid: {list(allowed) or '[terminal]'}"
        )

    if not evidence:
        reasons.append("no evidence supplied (no_unverified_outcomes)")
    else:
        if any(not e.verified for e in evidence):
            reasons.append("all evidence must be verified (no_unverified_outcomes)")
        if not any(e.stage == record.current_stage for e in evidence):
            reasons.append(
                f"no evidence references the stage being closed "
                f"({record.current_stage})"
            )

    return (not reasons), reasons


def advance_stage(
    record: TransformationRecord,
    target_stage: str,
    evidence: list[StageEvidence],
) -> TransformationRecord:
    """Advance ``record`` to ``target_stage``; return the new record.

    Raises ValueError if the transition is not permitted.
    """
    allowed, reasons = can_advance(record, target_stage, evidence)
    if not allowed:
        raise ValueError("; ".join(reasons))
    return TransformationRecord(
        engagement_id=record.engagement_id,
        client_id=record.client_id,
        current_stage=target_stage,
        completed_stages=(*record.completed_stages, record.current_stage),
        evidence=(*record.evidence, *evidence),
    )
