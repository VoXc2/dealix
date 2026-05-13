"""Trust Engine — components + six required output questions."""

from __future__ import annotations

from dataclasses import dataclass


TRUST_ENGINE_COMPONENTS: tuple[str, ...] = (
    "source_passport",
    "data_quality_score",
    "pii_detection",
    "allowed_use_registry",
    "llm_gateway",
    "agent_control_plane",
    "governance_runtime",
    "approval_engine",
    "audit_trail",
    "proof_pack",
    "incident_response",
)


TRUST_ENGINE_QUESTIONS: tuple[str, ...] = (
    "what_is_the_data_source",
    "is_pii_present",
    "is_use_allowed",
    "which_agent_or_model_was_used",
    "is_output_draft_or_final",
    "who_approved_what_evidence_what_risks",
)


@dataclass(frozen=True)
class TrustEngineCheck:
    output_id: str
    answers: dict[str, str]  # keys must be from TRUST_ENGINE_QUESTIONS


@dataclass(frozen=True)
class TrustEngineCheckResult:
    is_complete: bool
    missing_answers: tuple[str, ...]


def evaluate_trust_engine_check(check: TrustEngineCheck) -> TrustEngineCheckResult:
    missing = tuple(q for q in TRUST_ENGINE_QUESTIONS if q not in check.answers or not check.answers[q].strip())
    return TrustEngineCheckResult(is_complete=not missing, missing_answers=missing)
