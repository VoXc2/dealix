"""Evals OS schemas — eval cases, results, run summaries.

Reuses ``knowledge_v10.RAGEvalResult`` for the RAG-quality metric so there
is one contract for grounding quality across the platform.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from auto_client_acquisition.knowledge_v10.schemas import RAGEvalResult

__all__ = [
    "EvalCase",
    "EvalResult",
    "EvalRunSummary",
    "RAGEvalResult",
]


@dataclass(frozen=True, slots=True)
class EvalCase:
    """A single check within a suite."""

    case_id: str
    suite_id: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class EvalResult:
    """The outcome of one eval case."""

    case_id: str
    suite_id: str
    passed: bool
    score: float  # 0..1
    failures: tuple[str, ...] = ()
    metrics: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["failures"] = list(self.failures)
        return d


@dataclass(frozen=True, slots=True)
class EvalRunSummary:
    """Aggregate outcome of a suite run."""

    run_id: str = field(default_factory=lambda: f"evrun_{uuid4().hex[:16]}")
    suite_id: str = ""
    customer_id: str = ""
    total: int = 0
    passed: int = 0
    pass_rate: float = 0.0
    regression_detected: bool = False
    results: tuple[EvalResult, ...] = ()
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "suite_id": self.suite_id,
            "customer_id": self.customer_id,
            "total": self.total,
            "passed": self.passed,
            "pass_rate": self.pass_rate,
            "regression_detected": self.regression_detected,
            "results": [r.to_dict() for r in self.results],
            "occurred_at": self.occurred_at,
        }
