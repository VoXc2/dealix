"""Proof to market — gates and forbidden claims."""
from __future__ import annotations

from auto_client_acquisition.proof_to_market import build_proof_to_market_plan


def test_plan_requires_approval_for_public() -> None:
    plan = build_proof_to_market_plan(
        [{"event_type": "diagnostic_delivered"}],
        sector="saas",
        has_written_approval=False,
    )
    assert plan["approval_gate"]["public_snippet_allowed"] is False
    assert "logo_without_consent" in plan["forbidden"]


def test_plan_allows_when_signed_off() -> None:
    plan = build_proof_to_market_plan(
        [{"event_type": "delivered_ok"}],
        has_written_approval=True,
    )
    assert plan["approval_gate"]["public_snippet_allowed"] is True
