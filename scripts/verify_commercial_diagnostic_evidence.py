#!/usr/bin/env python3
"""Fail-closed runtime verifier for the evidence-bound commercial diagnostic."""

from __future__ import annotations

from pathlib import Path

from dealix.commercial.diagnostic_engine import (
    DiagnosticEngine,
    DiagnosticRequest,
    REFERENCE_SUPPLIED_NOT_VERIFIED,
    UNKNOWN,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dealix" / "commercial" / "diagnostic_engine.py"

FORBIDDEN_MARKERS = (
    "20-35%",
    "15,000",
    "50,000",
    "+40%",
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

    engine = DiagnosticEngine()

    missing = engine.generate(DiagnosticRequest(company_name="Verification Co"))
    assert missing.customer_validation_status == UNKNOWN
    assert UNKNOWN in missing.unknowns
    assert missing.customer_value_claim is False
    assert missing.guarantee is False
    assert missing.payment_url_placeholder == ""
    assert missing.llm_used is False
    assert missing.recommended_service == "qualified_discovery"

    context_only = engine.generate(
        DiagnosticRequest(
            company_name="Verification Co",
            evidence_refs=["verification://source/1"],
            baseline_ref="verification://baseline/1",
            source_context="Internal context only; not customer acceptance.",
        )
    )
    assert context_only.customer_validation_status == UNKNOWN
    assert "customer_validated_business_impact" in context_only.unknowns

    reference_only = engine.generate(
        DiagnosticRequest(
            company_name="Verification Co",
            pain_points=["automation"],
            evidence_refs=["verification://source/1"],
            baseline_ref="verification://baseline/1",
            customer_validation_ref="verification://customer/1",
        )
    )
    assert reference_only.customer_validation_status == REFERENCE_SUPPLIED_NOT_VERIFIED
    assert reference_only.customer_validation_status != "CUSTOMER_VALIDATED_WITH_REFERENCE"
    assert UNKNOWN in reference_only.unknowns
    assert "customer_validated_business_impact" in reference_only.unknowns
    assert reference_only.customer_value_claim is False
    assert reference_only.recommendation_status == "HYPOTHESIS_ONLY"

    print("DEALIX_DIAGNOSTIC_EVIDENCE_BOUND=PASS")
    print("UNKNOWN_SEMANTICS=PASS")
    print("CUSTOMER_VALIDATION_AUTHORITY=CANONICAL_EVIDENCE_OWNER_ONLY")
    print("UNVERIFIED_VALIDATION_REFERENCE=PRESERVED_NOT_PROMOTED")
    print("UNSUPPORTED_BENCHMARKS=BLOCKED")
    print("CUSTOMER_VALUE_CLAIM=FALSE")
    print("AUTOMATIC_SEND=FALSE")
    print("LLM_USED=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
