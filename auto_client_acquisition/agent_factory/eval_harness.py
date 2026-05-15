"""Agent evaluation harness — deterministic, NO LLM-as-judge.
حزمة تقييم الوكلاء — حتمية، بدون استخدام نموذج لغوي كحَكَم.

Scaffold mirroring ``knowledge_v10.eval_contract``: pure heuristic checks so
the bundle stays deterministic and offline-safe.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AgentEvalCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(..., min_length=1)
    description: str = ""
    input_summary: str = ""
    expected_outcome: str = ""
    expected_escalation: bool = False


class AgentEvalSuite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suite_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    cases: list[AgentEvalCase] = Field(default_factory=list)


class AgentEvalResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    passed: bool = False
    governance_compliant: bool = True
    escalation_correct: bool = False
    notes: str = ""


class AgentEvalSuiteResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suite_id: str
    agent_id: str
    results: list[AgentEvalResult] = Field(default_factory=list)
    pass_rate: float = Field(default=0.0, ge=0.0, le=1.0)


def run_eval_case(
    case: AgentEvalCase,
    *,
    observed_outcome: str,
    observed_escalation: bool,
) -> AgentEvalResult:
    """Deterministically compare an observed run against a case.

    # LATER WAVE: a real harness will execute the agent against
    # ``orchestrator.runtime`` and capture the observation automatically.
    """
    outcome_match = observed_outcome.strip() == case.expected_outcome.strip()
    escalation_correct = observed_escalation == case.expected_escalation
    return AgentEvalResult(
        case_id=case.case_id,
        passed=outcome_match and escalation_correct,
        governance_compliant=True,
        escalation_correct=escalation_correct,
        notes="" if outcome_match else "outcome_mismatch",
    )


def run_eval_suite(
    suite: AgentEvalSuite,
    observations: dict[str, tuple[str, bool]],
) -> AgentEvalSuiteResult:
    """Run every case. ``observations`` maps ``case_id -> (outcome, escalation)``."""
    results: list[AgentEvalResult] = []
    for case in suite.cases:
        outcome, escalation = observations.get(case.case_id, ("", False))
        results.append(
            run_eval_case(
                case,
                observed_outcome=outcome,
                observed_escalation=escalation,
            ),
        )
    passed = sum(1 for r in results if r.passed)
    pass_rate = float(passed) / float(len(results)) if results else 0.0
    return AgentEvalSuiteResult(
        suite_id=suite.suite_id,
        agent_id=suite.agent_id,
        results=results,
        pass_rate=pass_rate,
    )


__all__ = [
    "AgentEvalCase",
    "AgentEvalResult",
    "AgentEvalSuite",
    "AgentEvalSuiteResult",
    "run_eval_case",
    "run_eval_suite",
]
