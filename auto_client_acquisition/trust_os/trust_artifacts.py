"""Trust artifact vocabulary — no trust claim without artifact."""

from __future__ import annotations

TRUST_ARTIFACT_TYPES: tuple[str, ...] = (
    "source_passport",
    "governance_decision_log",
    "ai_run_ledger",
    "proof_pack",
    "approval_record",
    "incident_log",
)


def trust_artifact_coverage_score(present: frozenset[str]) -> int:
    if not TRUST_ARTIFACT_TYPES:
        return 0
    n = sum(1 for t in TRUST_ARTIFACT_TYPES if t in present)
    return (n * 100) // len(TRUST_ARTIFACT_TYPES)


__all__ = ["TRUST_ARTIFACT_TYPES", "trust_artifact_coverage_score"]
