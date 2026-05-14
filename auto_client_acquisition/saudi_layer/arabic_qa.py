"""Arabic executive QA dimensions (0–100 inputs; no LLM)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArabicQADimensions:
    clarity: int
    executive_tone: int
    saudi_business_fit: int
    no_exaggeration: int
    claim_safety: int
    actionability: int


def arabic_qa_score(d: ArabicQADimensions) -> int:
    vals = (d.clarity, d.executive_tone, d.saudi_business_fit, d.no_exaggeration, d.claim_safety, d.actionability)
    clipped = tuple(max(0, min(100, v)) for v in vals)
    return sum(clipped) // len(clipped)


__all__ = ["ArabicQADimensions", "arabic_qa_score"]
