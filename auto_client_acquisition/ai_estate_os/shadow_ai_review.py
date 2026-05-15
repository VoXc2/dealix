"""Shadow AI review — flag undeclared tools/models."""

from __future__ import annotations


def shadow_ai_risk_score(*, undeclared_tools: int, undeclared_models: int) -> int:
    return min(100, undeclared_tools * 15 + undeclared_models * 10)


__all__ = ["shadow_ai_risk_score"]
