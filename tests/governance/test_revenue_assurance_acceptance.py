"""Red-Team Acceptance Suite — every guardrail case must pass.

These cases test the system against failure: unsupported claims, missing
approvals, missing disclosures, and revenue without payment must all be
caught. A failure here means a non-negotiable boundary has regressed.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_assurance_os.acceptance_tests import (
    acceptance_suite_passed,
    run_acceptance_suite,
)


def test_full_acceptance_suite_passes() -> None:
    results = run_acceptance_suite()
    failed = [r.to_dict() for r in results if not r.passed]
    assert not failed, f"acceptance regressions: {failed}"
    assert acceptance_suite_passed() is True


def test_guaranteed_revenue_claim_is_blocked() -> None:
    result = next(r for r in run_acceptance_suite() if r.case_id == "guaranteed_revenue_claim")
    assert result.passed is True


def test_invoice_without_scope_is_blocked() -> None:
    result = next(r for r in run_acceptance_suite() if r.case_id == "invoice_without_scope")
    assert result.passed is True


def test_revenue_without_payment_is_blocked() -> None:
    result = next(r for r in run_acceptance_suite() if r.case_id == "revenue_without_payment")
    assert result.passed is True
