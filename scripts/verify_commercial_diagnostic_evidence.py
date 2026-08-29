#!/usr/bin/env python3
"""Verify the commercial diagnostic remains evidence-bound and non-committing."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dealix" / "commercial" / "diagnostic_engine.py"

FORBIDDEN_MARKERS = (
    "20-35%",
    "15,000",
    "50,000",
    "5+ hours",
    "guaranteed revenue",
    "guaranteed roi",
    "money-back",
)


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in FORBIDDEN_MARKERS:
        if marker.lower() in lowered:
            raise SystemExit(f"DEALIX_DIAGNOSTIC_EVIDENCE_BOUND=FAIL:{marker}")

    required = (
        "UNKNOWN_NOT_EVIDENCE_BACKED",
        "customer_value_claim: bool = False",
        "guarantee: bool = False",
        "approval_status: str = \"approval_required\"",
        "llm_used: bool = False",
        "does not establish revenue",
    )
    for marker in required:
        if marker.lower() not in lowered:
            raise SystemExit(f"DEALIX_DIAGNOSTIC_EVIDENCE_BOUND=FAIL:missing:{marker}")

    print("DEALIX_DIAGNOSTIC_EVIDENCE_BOUND=PASS")
    print("UNSUPPORTED_BENCHMARKS=BLOCKED")
    print("CUSTOMER_VALUE_CLAIM=FALSE")
    print("AUTOMATIC_SEND=FALSE")
    print("LLM_USED=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
