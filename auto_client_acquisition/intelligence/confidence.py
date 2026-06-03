"""Dealix Intelligence — Confidence Scoring.

Every model output (local or cloud) gets a ConfidenceScore so downstream
code can decide:
- accept the answer (high confidence)
- escalate to founder (low confidence + fallback_to_human=True)
- retry with stronger model (low confidence + fallback to cloud allowed)
- block + degrade to draft_only (very low confidence + safety risk)

Confidence is computed deterministically from explicit signals
(structured-output validation, internal model probability when available,
contradiction with other agents, presence of refusal markers).

Article 8: confidence is NEVER fabricated. When no signal is available,
returns ``unknown`` rather than a fake middling value.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

ConfidenceLevel = Literal["unknown", "very_low", "low", "medium", "high", "very_high"]


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    """Confidence in a single model output.

    ``score`` is in [0.0, 1.0] when computable; None when unknown.
    ``level`` is the bucketed label.
    ``reasons`` lists the signals that drove the bucket assignment
    (for audit + debugging).
    """

    score: float | None
    level: ConfidenceLevel
    reasons: tuple[str, ...]

    @property
    def is_actionable(self) -> bool:
        """True when the answer is safe to act on without human review.

        Threshold: medium or higher (≥0.6). Below that, the caller
        should treat the output as a draft requiring approval.
        """
        return self.level in ("medium", "high", "very_high")

    @property
    def needs_human_review(self) -> bool:
        """True when the output should NOT be acted on automatically."""
        return self.level in ("unknown", "very_low", "low")


# Refusal markers — when the model generated text that indicates
# it couldn't or wouldn't answer (Anthropic / OpenAI / Gemini patterns).
_REFUSAL_PATTERNS = (
    re.compile(r"\bI cannot\b|\bI can't\b|\bI'm unable\b|\bI am unable\b", re.IGNORECASE),
    re.compile(r"\bI don't have (enough )?information\b", re.IGNORECASE),
    re.compile(r"\bnot able to\b|\bunable to provide\b", re.IGNORECASE),
    re.compile(r"\bclarif", re.IGNORECASE),  # "could you clarify"
    re.compile(r"لا (أستطيع|أقدر)|ليس لدي معلومات|أحتاج توضيح"),
)

# Hedge markers — model is uncertain but answered anyway.
_HEDGE_PATTERNS = (
    re.compile(r"\bperhaps\b|\bmaybe\b|\bpossibly\b|\bmight\b", re.IGNORECASE),
    re.compile(r"\bI think\b|\bI believe\b|\bI'm not sure\b", re.IGNORECASE),
    re.compile(r"ربما|قد يكون|أعتقد|أظن|من الممكن"),
)


def from_text_signals(text: str, *, expected_json: bool = False) -> ConfidenceScore:
    """Compute confidence from the response text alone.

    This is the cheapest signal — works for any model output without
    needing model-internal probabilities. Use as the baseline when
    no other signal is available.

    Args:
        text: The model's response text.
        expected_json: When True, requires the text to parse as JSON
            for the result to be considered structured-valid.

    Returns:
        ConfidenceScore with level + reasons.
    """
    if not text or not text.strip():
        return ConfidenceScore(
            score=0.0, level="very_low",
            reasons=("empty_response",),
        )

    text_stripped = text.strip()
    reasons: list[str] = []
    score = 0.5  # neutral starting point

    # Refusal markers → very_low
    for pat in _REFUSAL_PATTERNS:
        if pat.search(text_stripped):
            return ConfidenceScore(
                score=0.1, level="very_low",
                reasons=("model_refused_or_clarified",),
            )

    # Hedge markers → drop confidence
    hedge_count = sum(1 for pat in _HEDGE_PATTERNS if pat.search(text_stripped))
    if hedge_count > 0:
        score -= 0.1 * hedge_count
        reasons.append(f"hedged_{hedge_count}x")

    # Length signal — too short = likely incomplete
    if len(text_stripped) < 20:
        score -= 0.2
        reasons.append("very_short_output")
    elif len(text_stripped) > 100:
        score += 0.1
        reasons.append("substantial_output")

    # JSON validation (when caller expected JSON)
    if expected_json:
        try:
            import json as _json
            _json.loads(text_stripped)
            score += 0.2
            reasons.append("valid_json")
        except (ValueError, TypeError):
            score -= 0.3
            reasons.append("invalid_json")

    # Bound in [0, 1]
    score = max(0.0, min(1.0, score))
    return ConfidenceScore(
        score=score, level=_score_to_level(score),
        reasons=tuple(reasons) if reasons else ("baseline",),
    )


def from_logprobs(*, avg_logprob: float | None) -> ConfidenceScore:
    """Compute confidence from model-reported logprobs.

    Most providers don't expose logprobs by default, so this is the
    secondary path. ``avg_logprob`` is the average per-token log-
    probability; closer to 0 = more confident.

    Returns ``unknown`` when ``avg_logprob`` is None.
    """
    if avg_logprob is None:
        return ConfidenceScore(score=None, level="unknown", reasons=("no_logprobs",))
    # Convert logprob to probability (e^logprob), then bucket
    import math
    prob = math.exp(avg_logprob)
    return ConfidenceScore(
        score=prob, level=_score_to_level(prob),
        reasons=(f"avg_logprob={avg_logprob:.3f}",),
    )


def combine(*scores: ConfidenceScore) -> ConfidenceScore:
    """Combine multiple confidence scores (e.g. text-signal + logprob).

    Uses minimum-weighted-average — pessimistic so that one weak signal
    drags the combined score down (Article 8: never inflate confidence).
    """
    if not scores:
        return ConfidenceScore(score=None, level="unknown", reasons=("no_inputs",))
    numeric = [s.score for s in scores if s.score is not None]
    if not numeric:
        return ConfidenceScore(
            score=None, level="unknown",
            reasons=("all_inputs_unknown",),
        )
    # Weighted: 60% min, 40% mean (pessimistic)
    min_score = min(numeric)
    mean_score = sum(numeric) / len(numeric)
    combined = 0.6 * min_score + 0.4 * mean_score
    all_reasons = tuple(r for s in scores for r in s.reasons)
    return ConfidenceScore(
        score=combined, level=_score_to_level(combined),
        reasons=all_reasons + (f"combined_{len(scores)}_signals",),
    )


def _score_to_level(score: float) -> ConfidenceLevel:
    """Bucket a numeric score into a ConfidenceLevel.

    Thresholds (intentionally conservative — Article 8):
      ≥0.85: very_high
      ≥0.70: high
      ≥0.55: medium
      ≥0.35: low
      <0.35: very_low
    """
    if score >= 0.85:
        return "very_high"
    if score >= 0.70:
        return "high"
    if score >= 0.55:
        return "medium"
    if score >= 0.35:
        return "low"
    return "very_low"
