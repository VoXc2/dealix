#!/usr/bin/env python3
"""Fail-closed runtime verifier for workload economics attribution."""

from __future__ import annotations

from dealix.observability.economic_attribution import (
    UNKNOWN,
    WorkloadEconomicsAttribution,
    WorkloadMeasurement,
)


def main() -> int:
    run = WorkloadMeasurement(
        run_id="verification-run",
        workload_id="verification-workload",
        agent_id="dealix-engineer",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:05:00+00:00",
        output_evidence_refs=["evidence-1"],
        first_evidence_at="2026-08-29T08:02:00+00:00",
    )
    report = WorkloadEconomicsAttribution().summarize([run])

    assert report.semantic_dict() == (
        WorkloadEconomicsAttribution().summarize([run]).semantic_dict()
    )
    assert report.runs[0].time_to_evidence_ms == 120_000.0
    assert report.runs[0].llm_cost_usd == UNKNOWN
    assert report.guardrails["verified_revenue"] == UNKNOWN
    assert report.guardrails["invoice_is_not_payment"] is True
    print("PASS: workload economics attribution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
