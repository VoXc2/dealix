"""Red-Team Acceptance Suite — test the system against failure, not success.

Each case states an input and the expected protective behaviour, then
routes to the real governance checker (or a Revenue Assurance gate) and
verifies it. A failing case means a guardrail has regressed.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any

from auto_client_acquisition.governance_os import (
    approval_for_action,
    policy_check_draft,
)
from auto_client_acquisition.revenue_assurance_os import gates


@dataclass(frozen=True, slots=True)
class AcceptanceResult:
    case_id: str
    description: str
    expected: str
    actual: str
    passed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _case_guaranteed_revenue_claim() -> tuple[str, str, bool]:
    result = policy_check_draft("نضمن لك زيادة إيراد 30% خلال شهر")
    actual = f"allowed={result.allowed} issues={list(result.issues)}"
    return ("blocked", actual, result.allowed is False)


def _case_cold_whatsapp() -> tuple[str, str, bool]:
    result = policy_check_draft("Use cold whatsapp to reach every prospect")
    actual = f"allowed={result.allowed} issues={list(result.issues)}"
    return ("blocked", actual, result.allowed is False)


def _case_scraping() -> tuple[str, str, bool]:
    result = policy_check_draft("scrape leads from public directories")
    actual = f"allowed={result.allowed} issues={list(result.issues)}"
    return ("blocked", actual, result.allowed is False)


def _case_email_send_requires_human() -> tuple[str, str, bool]:
    risk, route = approval_for_action("send email to prospect")
    actual = f"risk={risk} route={route}"
    return ("human-review required", actual, route == "human")


def _case_linkedin_automation() -> tuple[str, str, bool]:
    risk, route = approval_for_action("linkedin automation outreach")
    actual = f"risk={risk} route={route}"
    return ("blocked", actual, route == "blocked")


def _case_weak_lead_no_disturb() -> tuple[str, str, bool]:
    outcome = gates.lead_approval_gate(lead_score=20)
    actual = f"generates_approval_task={outcome.flags['generates_approval_task']}"
    return ("no founder approval task", actual, outcome.flags["generates_approval_task"] is False)


def _case_strong_lead_generates_task() -> tuple[str, str, bool]:
    outcome = gates.lead_approval_gate(lead_score=88)
    actual = f"generates_approval_task={outcome.flags['generates_approval_task']}"
    return (
        "founder approval task created",
        actual,
        outcome.flags["generates_approval_task"] is True,
    )


def _case_claim_without_source() -> tuple[str, str, bool]:
    outcome = gates.claim_source_gate(has_source=False)
    actual = f"allowed={outcome.allowed} risk={outcome.flags['risk_level']}"
    return ("blocked", actual, outcome.allowed is False)


def _case_invoice_without_scope() -> tuple[str, str, bool]:
    outcome = gates.invoice_gate(scope_approved=False)
    actual = f"allowed={outcome.allowed} reason={outcome.reason}"
    return ("blocked", actual, outcome.allowed is False)


def _case_affiliate_without_disclosure() -> tuple[str, str, bool]:
    outcome = gates.affiliate_disclosure_gate(has_disclosure=False)
    actual = (
        f"compliance_flag={outcome.flags['compliance_flag']} "
        f"payout_hold={outcome.flags['payout_hold']}"
    )
    return (
        "compliance_flag + payout_hold",
        actual,
        outcome.flags["compliance_flag"] is True and outcome.flags["payout_hold"] is True,
    )


def _case_support_high_risk_escalates() -> tuple[str, str, bool]:
    outcome = gates.support_escalation_gate(is_high_risk=True)
    actual = f"escalated={outcome.flags['escalated']}"
    return ("escalated to human", actual, outcome.flags["escalated"] is True)


def _case_agent_output_without_source() -> tuple[str, str, bool]:
    outcome = gates.agent_output_confidence_gate(has_source=False)
    actual = f"confidence={outcome.flags['confidence']}"
    return ("low confidence", actual, outcome.flags["confidence"] == "low")


def _case_revenue_without_payment() -> tuple[str, str, bool]:
    outcome = gates.revenue_record_gate(payment_confirmed=False)
    actual = f"allowed={outcome.allowed} reason={outcome.reason}"
    return ("blocked", actual, outcome.allowed is False)


def _case_revenue_with_payment() -> tuple[str, str, bool]:
    outcome = gates.revenue_record_gate(payment_confirmed=True)
    actual = f"allowed={outcome.allowed} reason={outcome.reason}"
    return ("allowed", actual, outcome.allowed is True)


# (case_id, description, check) — check returns (expected, actual, passed).
_CASES: tuple[tuple[str, str, Callable[[], tuple[str, str, bool]]], ...] = (
    (
        "guaranteed_revenue_claim",
        "Unsupported revenue guarantee is blocked",
        _case_guaranteed_revenue_claim,
    ),
    ("cold_whatsapp", "Cold WhatsApp copy is blocked", _case_cold_whatsapp),
    ("scraping", "Scraping copy is blocked", _case_scraping),
    ("email_send", "Email send requires human review", _case_email_send_requires_human),
    ("linkedin_automation", "LinkedIn automation is blocked", _case_linkedin_automation),
    ("weak_lead", "Weak lead does not disturb the founder", _case_weak_lead_no_disturb),
    ("strong_lead", "Strong lead generates an approval task", _case_strong_lead_generates_task),
    ("claim_without_source", "Claim without a source is blocked", _case_claim_without_source),
    (
        "invoice_without_scope",
        "Invoice without an approved scope is blocked",
        _case_invoice_without_scope,
    ),
    (
        "affiliate_without_disclosure",
        "Affiliate without disclosure is flagged",
        _case_affiliate_without_disclosure,
    ),
    (
        "support_high_risk",
        "High-risk support question escalates",
        _case_support_high_risk_escalates,
    ),
    (
        "agent_output_without_source",
        "Unsourced agent output is low-confidence",
        _case_agent_output_without_source,
    ),
    (
        "revenue_without_payment",
        "Revenue without payment is blocked",
        _case_revenue_without_payment,
    ),
    (
        "revenue_with_payment",
        "Revenue with confirmed payment is allowed",
        _case_revenue_with_payment,
    ),
)


def run_acceptance_suite() -> list[AcceptanceResult]:
    """Run every Red-Team acceptance case and return structured results."""
    results: list[AcceptanceResult] = []
    for case_id, description, check in _CASES:
        try:
            expected, actual, passed = check()
        except Exception as exc:  # noqa: BLE001 — a crash is a failed guardrail
            expected, actual, passed = ("no exception", f"raised:{exc!r}", False)
        results.append(AcceptanceResult(case_id, description, expected, actual, passed))
    return results


def acceptance_suite_passed() -> bool:
    """True only when every acceptance case passes."""
    return all(r.passed for r in run_acceptance_suite())


__all__ = [
    "AcceptanceResult",
    "acceptance_suite_passed",
    "run_acceptance_suite",
]
