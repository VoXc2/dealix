"""Tests for the pure-computation readiness gate."""
from __future__ import annotations

from auto_client_acquisition.customer_readiness.readiness_gate import (
    THRESHOLD_DECISIONS_OK,
    compute_readiness_gate,
    public_projection,
)


def test_proceed_when_all_gates_met():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="present",
        governance_decisions_7d=THRESHOLD_DECISIONS_OK + 1,
        proof_pack_count=1,
        capital_asset_count=1,
        has_signed_scope=True,
    )
    assert g.recommendation == "PROCEED"
    assert g.rationale == ()


def test_hold_for_governance_when_passport_missing():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="missing",
        governance_decisions_7d=20,
        proof_pack_count=2,
        capital_asset_count=2,
        has_signed_scope=True,
    )
    assert g.recommendation == "HOLD_FOR_GOVERNANCE"
    assert "source_passport_not_present" in g.rationale


def test_hold_for_governance_when_few_decisions():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="present",
        governance_decisions_7d=0,
        proof_pack_count=2,
        capital_asset_count=2,
        has_signed_scope=True,
    )
    assert g.recommendation == "HOLD_FOR_GOVERNANCE"


def test_hold_for_scope_when_no_signed_scope():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="present",
        governance_decisions_7d=THRESHOLD_DECISIONS_OK + 5,
        proof_pack_count=1,
        capital_asset_count=1,
        has_signed_scope=False,
    )
    assert g.recommendation == "HOLD_FOR_SCOPE"
    assert "scope_not_signed" in g.rationale


def test_unknown_passport_status_normalized():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="weird-value",
        governance_decisions_7d=10,
        proof_pack_count=1,
        capital_asset_count=1,
        has_signed_scope=True,
    )
    assert g.source_passport_status == "unknown"
    assert g.recommendation == "HOLD_FOR_GOVERNANCE"


def test_public_projection_drops_numeric_fields():
    g = compute_readiness_gate(
        handle="acme",
        source_passport_status="present",
        governance_decisions_7d=99,
        proof_pack_count=42,
        capital_asset_count=7,
        has_signed_scope=True,
    )
    proj = public_projection(g, as_of="2026-05-14T00:00:00+00:00")
    keys = set(proj.keys())
    assert keys == {"handle", "recommendation", "as_of", "doctrine"}
    # No leaked numerics anywhere in the projection (incl. nested).
    text = repr(proj)
    for bad in ("99", "42", "governance_decisions", "proof_pack_count", "capital_asset_count"):
        assert bad not in text
