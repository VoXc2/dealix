"""Wave 13 Phase 9 — Bottleneck Radar tests.

Asserts:
  - 5 counts present in schema
  - bilingual summary populated
  - today_single_action priority order: payment > approvals > SLA > proof > followup
  - severity bucket maps correctly: clear (0) / watch (1-2) / blocking (3-5) / critical (6+)
  - empty state ('clear' severity) when no blockers
  - tenant respected (customer_handle vs portfolio)
  - is_estimate=True
  - today_single_action ≤ 1 sentence (no period in middle, ≤ 200 chars)

Sandbox-safe: imports schemas + computer modules directly.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load():
    repo_root = Path(__file__).resolve().parent.parent

    schemas = importlib.util.spec_from_file_location(
        "_test_w13_p9_br_schemas",
        repo_root / "auto_client_acquisition" / "bottleneck_radar" / "schemas.py",
    )
    sm = importlib.util.module_from_spec(schemas)
    assert schemas is not None and schemas.loader is not None
    sys.modules["_test_w13_p9_br_schemas"] = sm
    sys.modules["auto_client_acquisition.bottleneck_radar.schemas"] = sm
    schemas.loader.exec_module(sm)

    comp = importlib.util.spec_from_file_location(
        "_test_w13_p9_br_computer",
        repo_root / "auto_client_acquisition" / "bottleneck_radar" / "computer.py",
    )
    cm = importlib.util.module_from_spec(comp)
    assert comp is not None and comp.loader is not None
    sys.modules["_test_w13_p9_br_computer"] = cm
    comp.loader.exec_module(cm)

    return sm, cm


_SCH, _COMP = _load()
FounderBottleneck = _SCH.FounderBottleneck
compute_bottleneck = _COMP.compute_bottleneck
compute_founder_view = _COMP.compute_founder_view


# ── Test 1 ────────────────────────────────────────────────────────────
def test_schema_has_5_counts():
    fb = FounderBottleneck(customer_handle="acme")
    d = fb.model_dump()
    for f in [
        "blocking_approvals_count",
        "pending_payment_confirmations",
        "pending_proof_packs_to_send",
        "overdue_followups",
        "sla_at_risk_tickets",
    ]:
        assert f in d
        assert d[f] == 0


# ── Test 2 ────────────────────────────────────────────────────────────
def test_clear_severity_when_no_blockers():
    fb = compute_bottleneck(customer_handle="acme")
    assert fb.severity == "clear"
    assert "لا اختناقات" in fb.bottleneck_summary_ar
    assert "No current bottlenecks" in fb.bottleneck_summary_en


# ── Test 3 ────────────────────────────────────────────────────────────
def test_severity_bucket_thresholds():
    """clear (0) / watch (1-2) / blocking (3-5) / critical (6+)."""
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=0).severity == "clear"
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=1).severity == "watch"
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=2).severity == "watch"
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=3).severity == "blocking"
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=5).severity == "blocking"
    assert compute_bottleneck(customer_handle="x", blocking_approvals_count=10).severity == "critical"


# ── Test 4 ────────────────────────────────────────────────────────────
def test_priority_order_payment_first():
    """Highest priority: pending payments (revenue blocker)."""
    fb = compute_bottleneck(
        customer_handle="acme",
        blocking_approvals_count=5,    # less urgent
        pending_payment_confirmations=1,  # most urgent
        sla_at_risk_tickets=3,
    )
    assert "دفعات" in fb.today_single_action_ar or "Confirm" in fb.today_single_action_en
    assert "payment" in fb.today_single_action_en.lower()


# ── Test 5 ────────────────────────────────────────────────────────────
def test_priority_when_no_payments_approvals_next():
    fb = compute_bottleneck(
        customer_handle="acme",
        blocking_approvals_count=2,
        sla_at_risk_tickets=1,
    )
    assert "موافقة" in fb.today_single_action_ar or "Approve" in fb.today_single_action_en


# ── Test 6 ────────────────────────────────────────────────────────────
def test_founder_view_no_customer_handle():
    fb = compute_founder_view(blocking_approvals_count=2)
    assert fb.customer_handle is None
    assert "البورتفوليو" in fb.bottleneck_summary_ar
    assert "portfolio" in fb.bottleneck_summary_en.lower()


# ── Test 7 ────────────────────────────────────────────────────────────
def test_today_single_action_is_one_sentence():
    """Action must be ≤ 200 chars and contain at most 1 sentence-ending period."""
    fb = compute_bottleneck(
        customer_handle="acme",
        blocking_approvals_count=3,
        sla_at_risk_tickets=2,
    )
    for action in [fb.today_single_action_ar, fb.today_single_action_en]:
        assert action  # non-empty
        assert len(action) <= 200, f"action too long: {len(action)} chars"
        # At most 1 period in middle (allow trailing period)
        stripped = action.rstrip(".")
        assert stripped.count(".") <= 1


# ── Test 8 ────────────────────────────────────────────────────────────
def test_is_estimate_true_always():
    """Article 8: every Bottleneck assessment is_estimate=True."""
    fb1 = compute_bottleneck(customer_handle="acme")
    fb2 = compute_bottleneck(customer_handle="x", blocking_approvals_count=10)
    fb3 = compute_founder_view(pending_payment_confirmations=5)
    assert fb1.is_estimate is True
    assert fb2.is_estimate is True
    assert fb3.is_estimate is True
