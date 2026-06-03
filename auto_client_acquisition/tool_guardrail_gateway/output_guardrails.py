"""Output guardrails — forbidden-token scrub + ROI-claim regex.

Reuses the same forbidden-token list as designops/safety_gate
+ leadops_spine/draft_builder.
"""
from __future__ import annotations

import re
from typing import Any

_FORBIDDEN_PATTERNS = [
    re.compile(r"\bguaranteed?\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\bscraping\b", re.IGNORECASE),
    re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    re.compile(r"نضمن"),
    re.compile(r"مضمون"),
]

# ROI-claim regex (e.g., "10x revenue", "5x growth")
_ROI_CLAIM_PATTERNS = [
    re.compile(r"\b\d+\s*x\s+(revenue|growth|leads?|sales|pipeline)\b", re.IGNORECASE),
    re.compile(r"\b\d+\s*%\s+(more|increase)\s+(revenue|growth|leads?)\b", re.IGNORECASE),
]


def check_output(*, text: str) -> dict[str, Any]:
    """Returns {passed, reasons, scrubbed_text}."""
    reasons: list[str] = []
    scrubbed = text

    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(scrubbed):
            reasons.append(f"forbidden_token:{pat.pattern[:30]}")
            scrubbed = pat.sub("[REDACTED]", scrubbed)

    for pat in _ROI_CLAIM_PATTERNS:
        if pat.search(scrubbed):
            reasons.append(f"roi_claim:{pat.pattern[:30]}")
            scrubbed = pat.sub("[CLAIM_BLOCKED]", scrubbed)

    return {
        "passed": len(reasons) == 0,
        "reasons": reasons,
        "scrubbed_text": scrubbed,
    }
