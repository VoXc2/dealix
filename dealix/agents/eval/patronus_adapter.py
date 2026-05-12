"""
Patronus — AI safety + hallucination scoring via REST.
Inert without PATRONUS_API_KEY.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class PatronusVerdict:
    pass_: bool
    score: float
    flagged_dimensions: list[str]
    provider: str


def is_configured() -> bool:
    return bool(os.getenv("PATRONUS_API_KEY", "").strip())


async def evaluate(
    *,
    prompt: str,
    response: str,
    evaluators: list[str] | None = None,
) -> PatronusVerdict:
    if not is_configured():
        return PatronusVerdict(
            pass_=True, score=0.0, flagged_dimensions=[], provider="none"
        )
    key = os.getenv("PATRONUS_API_KEY", "").strip()
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post(
                "https://api.patronus.ai/v1/evaluate",
                headers={"X-API-Key": key, "Content-Type": "application/json"},
                json={
                    "evaluators": evaluators or ["hallucination", "toxicity"],
                    "evaluated_model_input": prompt,
                    "evaluated_model_output": response,
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("patronus_evaluate_failed")
        return PatronusVerdict(
            pass_=False, score=0.0, flagged_dimensions=[], provider="patronus"
        )
    results = data.get("results", [])
    flagged = [r.get("evaluator") for r in results if r.get("pass") is False]
    score = float(sum(float(r.get("score") or 0) for r in results) / max(len(results), 1))
    return PatronusVerdict(
        pass_=not flagged,
        score=score,
        flagged_dimensions=flagged,
        provider="patronus",
    )
