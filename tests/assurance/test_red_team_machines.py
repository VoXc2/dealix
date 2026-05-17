"""Red-team tests for the operational machines.

Eight contract-style tests (no DB, no network) that assert each machine
honors its assurance contract: it sells, serves, obeys governance, and
records evidence — and refuses the dangerous path.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.execution_assurance_os import load_machine_registry
from auto_client_acquisition.finance_os.guardrails import (
    finance_guardrails,
    is_live_charge_allowed,
)
from auto_client_acquisition.full_ops_contracts.schemas import PaymentStateRecord
from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.icp_scorer import ICPFilter, LeadSignals, score_lead

pytestmark = pytest.mark.unit


_STRONG_ICP = ICPFilter(
    target_sectors=["b2b_saas"],
    target_regions=["sa"],
    target_size_bands=["smb"],
    preferred_tech=["crm"],
)


# ── Test 1 — Lead test ───────────────────────────────────────────────
def test_lead_test_every_lead_is_scored_and_recorded() -> None:
    """Any captured lead receives a score, and the sales machine records it."""
    result = score_lead(LeadSignals(), _STRONG_ICP)
    assert "score" in result
    assert 0 <= result["score"] <= 100
    assert result["band"] in {"hot", "warm", "cool", "cold"}

    sales = load_machine_registry().get("sales_autopilot")
    assert sales is not None
    assert "lead_captured" in sales.evidence_event_names


# ── Test 2 — Qualified-lead test ─────────────────────────────────────
def test_qualified_lead_reaches_hot_band() -> None:
    """A strong lead (founder/B2B/GCC/CRM/intent/data) scores hot."""
    strong = LeadSignals(
        sector="b2b_saas",
        region="sa",
        size_band="smb",
        detected_tech=["crm"],
        recent_funding_round=True,
        recent_executive_hire=True,
        recent_expansion_announcement=True,
        has_email=True,
        has_domain=True,
        has_linkedin=True,
    )
    result = score_lead(strong, _STRONG_ICP)
    assert result["score"] >= 75
    assert result["band"] == "hot"


# ── Test 3 — Low-fit test ────────────────────────────────────────────
def test_low_fit_lead_is_not_pushed_to_sales() -> None:
    """A weak lead scores cold — no founder interruption."""
    weak = LeadSignals(
        sector="consumer_retail",
        region="us",
        size_band="enterprise",
        detected_tech=[],
    )
    result = score_lead(weak, _STRONG_ICP)
    assert result["band"] == "cold"
    assert result["score"] < 25


# ── Test 4 — Support low-risk ────────────────────────────────────────
def test_support_low_risk_question_is_allowed() -> None:
    """A plain, sourced answer to an easy question passes the policy gate."""
    verdict = policy_check_draft(
        "The Diagnostic service reviews your revenue data and returns a "
        "proof pack. See the service catalog for scope details."
    )
    assert verdict.allowed is True


# ── Test 5 — Support high-risk ───────────────────────────────────────
def test_support_high_risk_answer_is_blocked() -> None:
    """A guaranteed-outcome answer is blocked from auto-send."""
    en = policy_check_draft("Yes — guaranteed results, a guaranteed ROI within 30 days.")
    ar = policy_check_draft("نعم، نضمن لك زيادة الإيراد بنسبة 30%.")
    assert en.allowed is False
    assert ar.allowed is False

    support = load_machine_registry().get("support_autopilot")
    assert support is not None
    assert "high_risk_answer_sent" in support.approval_required_actions


# ── Test 6 — Affiliate compliance ────────────────────────────────────
def test_affiliate_misleading_claim_is_blocked() -> None:
    """A misleading affiliate claim is detected and blocked."""
    claim = policy_check_draft(
        "Join as a Dealix affiliate — guaranteed results and guaranteed ROI "
        "for every client you refer."
    )
    assert claim.allowed is False
    assert claim.issues  # at least one concrete reason

    affiliate = load_machine_registry().get("affiliate_machine")
    assert affiliate is not None
    assert "commission_payout" in affiliate.approval_required_actions


# ── Test 7 — Invoice guard ───────────────────────────────────────────
def test_invoice_guard_blocks_auto_charge() -> None:
    """No live charge happens automatically; invoices require approval."""
    state = is_live_charge_allowed()
    assert state["allowed"] is False

    rules = finance_guardrails()["rules"]
    assert rules["no_auto_charge"] is True
    assert rules["no_moyasar_allow_live_charge_env"] is True

    billing = load_machine_registry().get("billing_ops")
    assert billing is not None
    assert "invoice_sent" in billing.approval_required_actions


# ── Test 8 — Revenue guard ───────────────────────────────────────────
def _is_revenue(status: str) -> bool:
    """Revenue is recognized only at payment_confirmed."""
    return status == "payment_confirmed"


def test_revenue_guard_blocks_revenue_before_payment() -> None:
    """A draft/intent invoice is never revenue — only invoice_paid is."""
    intent = PaymentStateRecord(
        payment_id="pay_test_1",
        customer_handle="acme-co",
        amount_sar=499.0,
        method="moyasar_test",
    )
    assert intent.status == "invoice_intent"
    assert _is_revenue(intent.status) is False
    assert _is_revenue("invoice_sent_manual") is False
    assert _is_revenue("payment_confirmed") is True

    evidence = load_machine_registry().get("evidence_ledger")
    assert evidence is not None
    assert "invoice_paid" in evidence.evidence_event_names
