"""Wave 12.5 §33.2.4 (Engine 9) — Payment refund state machine + ZATCA wire tests.

Validates:
- 3-state refund path: refund_requested → refund_evidence_uploaded →
  refund_completed
- void_refund + transition rules (terminal states + invalid jumps)
- is_revenue_after_refund helper
- request_zatca_draft_on_payment_confirmed: returns None unless state=
  payment_confirmed; idempotency key deterministic; never auto-submits
- is_in_zatca_wave_24_bracket: 375K SAR threshold

All tests pure-function — no I/O, no HTTP, deterministic.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from auto_client_acquisition.payment_ops.refund_state_machine import (
    RefundEvent,
    RefundRecord,
    RefundTransitionError,
    ZATCADraftRequest,
    can_transition,
    complete_refund,
    is_in_zatca_wave_24_bracket,
    is_revenue_after_refund,
    request_refund,
    request_zatca_draft_on_payment_confirmed,
    upload_refund_evidence,
    void_refund,
)


# Test fixtures
def _initial_record() -> RefundRecord:
    return RefundRecord(
        customer_handle="acme",
        payment_id="pay_001",
        amount_sar=499.0,
        state="not_requested",
    )


# ─────────────────────────────────────────────────────────────────────
# 3-state refund path (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_refund_path_full_lifecycle() -> None:
    """not_requested → requested → evidence_uploaded → completed."""
    r0 = _initial_record()
    r1 = request_refund(r0, actor="founder", note="customer asked")
    assert r1.state == "refund_requested"
    assert len(r1.history) == 1

    r2 = upload_refund_evidence(r1, actor="founder", evidence_ref="bank_ref_xyz789")
    assert r2.state == "refund_evidence_uploaded"
    assert len(r2.history) == 2
    assert r2.history[1].evidence_ref == "bank_ref_xyz789"

    r3 = complete_refund(r2, actor="founder", ledger_entry_id="ledger_2026_05")
    assert r3.state == "refund_completed"
    assert len(r3.history) == 3


def test_refund_completed_flips_revenue() -> None:
    """is_revenue_after_refund returns False ONLY when refund_completed."""
    r = _initial_record()
    assert is_revenue_after_refund(r) is True  # not_requested → still revenue

    r1 = request_refund(r)
    assert is_revenue_after_refund(r1) is True  # requested but not done

    r2 = upload_refund_evidence(r1, evidence_ref="bank_x")
    assert is_revenue_after_refund(r2) is True  # evidence but not completed

    r3 = complete_refund(r2, ledger_entry_id="led_x")
    assert is_revenue_after_refund(r3) is False  # NOW revenue rolled back


def test_refund_void_mid_process_keeps_revenue() -> None:
    """void_refund stops the process; original payment stays revenue."""
    r = _initial_record()
    r1 = request_refund(r)
    r2 = void_refund(r1, note="customer changed mind")
    assert r2.state == "refund_voided"
    # Article 8: voided refund means original payment stays as revenue
    assert is_revenue_after_refund(r2) is True


def test_refund_void_after_evidence_uploaded() -> None:
    """Can void from refund_evidence_uploaded too."""
    r = _initial_record()
    r1 = request_refund(r)
    r2 = upload_refund_evidence(r1, evidence_ref="bank_x")
    r3 = void_refund(r2)
    assert r3.state == "refund_voided"


def test_refund_terminal_states_have_no_outgoing() -> None:
    """refund_completed and refund_voided have no outgoing transitions."""
    assert not can_transition("refund_completed", "refund_requested")
    assert not can_transition("refund_completed", "refund_voided")
    assert not can_transition("refund_voided", "refund_requested")


# ─────────────────────────────────────────────────────────────────────
# Invalid transitions raise (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_cannot_complete_without_evidence_upload() -> None:
    """Cannot jump from requested directly to completed."""
    r = _initial_record()
    r1 = request_refund(r)
    with pytest.raises(RefundTransitionError, match="cannot complete"):
        complete_refund(r1, ledger_entry_id="led_x")


def test_cannot_complete_without_ledger_id() -> None:
    """Article 8: completion requires ledger_entry_id (audit trail)."""
    r = _initial_record()
    r1 = request_refund(r)
    r2 = upload_refund_evidence(r1, evidence_ref="bank_x")
    with pytest.raises(RefundTransitionError, match="ledger_entry_id required"):
        complete_refund(r2, ledger_entry_id="")
    with pytest.raises(RefundTransitionError, match="ledger_entry_id required"):
        complete_refund(r2, ledger_entry_id="xx")  # too short


def test_cannot_upload_evidence_without_ref() -> None:
    """Article 8: evidence step requires non-empty evidence_ref."""
    r = _initial_record()
    r1 = request_refund(r)
    with pytest.raises(RefundTransitionError, match="evidence_ref required"):
        upload_refund_evidence(r1, evidence_ref="")
    with pytest.raises(RefundTransitionError, match="evidence_ref required"):
        upload_refund_evidence(r1, evidence_ref="ab")  # too short


def test_cannot_use_system_actor_for_refund() -> None:
    """Article 4: refund actor MUST be human (founder/csm/admin)."""
    r = _initial_record()
    with pytest.raises(RefundTransitionError, match="not human"):
        request_refund(r, actor="system")
    with pytest.raises(RefundTransitionError, match="not human"):
        request_refund(r, actor="auto")


# ─────────────────────────────────────────────────────────────────────
# ZATCA auto-draft helper (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_zatca_draft_returns_none_for_invoice_intent() -> None:
    """Article 8 revenue truth: invoice_intent ≠ payment_confirmed.
    No ZATCA draft for intent."""
    result = request_zatca_draft_on_payment_confirmed(
        payment_id="pay_001",
        customer_handle="acme",
        amount_sar=499,
        payment_state="invoice_intent_created",
    )
    assert result is None


def test_zatca_draft_returns_none_for_evidence_received() -> None:
    """evidence_received is NOT confirmed → no ZATCA draft."""
    for state in ("payment_pending", "evidence_received"):
        result = request_zatca_draft_on_payment_confirmed(
            payment_id="pay_001",
            customer_handle="acme",
            amount_sar=499,
            payment_state=state,
        )
        assert result is None, f"state={state} should NOT trigger ZATCA draft"


def test_zatca_draft_returns_request_for_payment_confirmed() -> None:
    """Only payment_confirmed triggers a ZATCA draft request."""
    result = request_zatca_draft_on_payment_confirmed(
        payment_id="pay_002",
        customer_handle="acme",
        amount_sar=499,
        payment_state="payment_confirmed",
    )
    assert result is not None
    assert result.payment_id == "pay_002"
    assert result.amount_sar == 499
    assert result.idempotency_key == "zatca_draft:pay_002"
    # Article 4: NEVER auto-submits
    assert result.would_submit is False


def test_zatca_idempotency_key_is_deterministic() -> None:
    """Same payment_id → same idempotency_key (caller-side dedup)."""
    r1 = request_zatca_draft_on_payment_confirmed(
        payment_id="pay_xyz", customer_handle="acme",
        amount_sar=100, payment_state="payment_confirmed",
    )
    r2 = request_zatca_draft_on_payment_confirmed(
        payment_id="pay_xyz", customer_handle="acme",
        amount_sar=100, payment_state="payment_confirmed",
    )
    assert r1.idempotency_key == r2.idempotency_key


def test_zatca_wave_24_threshold_is_375k_sar() -> None:
    """Wave 24 (June 30, 2026 deadline) applies to >SAR 375K turnover."""
    assert is_in_zatca_wave_24_bracket(500_000) is True
    assert is_in_zatca_wave_24_bracket(375_001) is True
    assert is_in_zatca_wave_24_bracket(375_000) is False  # exact threshold = no
    assert is_in_zatca_wave_24_bracket(100_000) is False
    assert is_in_zatca_wave_24_bracket(0) is False


# ─────────────────────────────────────────────────────────────────────
# Total: 14 tests (5 refund path + 4 invalid + 5 ZATCA)
# ─────────────────────────────────────────────────────────────────────
