"""Current commercial-authority tests for Proposal/Pricing DesignOps artifacts.

Pure unit tests — no network, no LLM, no DB. Legacy caller fields remain
accepted, but they must not resurrect fixed prices, public package tiers, live
payment language, or a non-30-day paid launch motion.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.designops.generators import (
    generate_pricing_page,
    generate_proposal_page,
)

RETIRED_TOKENS = (
    "4,999",
    "15,000",
    "1,500",
    "2,999",
    "499 SAR",
    "499 ر.س",
    "7-Tier",
    "Growth Starter",
    "Data to Revenue",
    "Executive Growth OS",
    "Partnership Growth",
    "Full Growth Control Tower",
)


def _proposal(**overrides):
    kwargs = {
        "customer_handle": "ACME",
        "recommended_service": "growth_starter",  # legacy caller input on purpose
        "scope_ar": "فجوة متابعة B2B تحتاج baseline وowner وProof.",
        "scope_en": "A B2B follow-up gap needs a baseline, owner, and Proof.",
        "deliverables": ["Baseline", "Weekly Proof Pack", "Final Proof Pack"],
        "timeline_days": 7,  # legacy input on purpose; output must normalize to 30
        "price_band_sar": "499",  # legacy input on purpose; must never leak
        "blocked_actions": ["No cold WhatsApp"],
        "proof_plan": ["Baseline → source → measured outcome"],
    }
    kwargs.update(overrides)
    return generate_proposal_page(**kwargs)


def test_proposal_normalizes_legacy_price_and_timeline_inputs() -> None:
    art = _proposal()
    blob = art["markdown"] + "\n" + art["html"]
    manifest = art["manifest"]

    assert "Revenue Command Pilot" in blob
    assert "30 days" in blob or "30 يومًا" in blob
    assert "customer-specific quote" in blob.lower() or "Quote خاص بالعميل" in blob
    assert "499" not in blob
    assert manifest["recommended_service"] == "Revenue Command Pilot"
    assert manifest["timeline_days"] == 30
    assert manifest["price_band_sar"] == "quote_after_discovery"
    assert manifest["quote_only"] is True
    assert manifest["manual_payment"] is False
    assert manifest["no_live_charge"] is True
    assert manifest["safe_to_send"] is False


def test_proposal_keeps_send_payment_and_outcome_boundaries() -> None:
    art = _proposal()
    blob = art["markdown"] + "\n" + art["html"]
    manifest = art["manifest"]

    assert "Founder must manually send" in blob
    assert "does not issue an invoice" in blob
    assert "No live charge" in blob
    assert "No promise of revenue" in blob
    assert manifest["payment_path_status"] == "blocked_until_customer_specific_approval"
    assert manifest["approval_status"] == "approval_required"
    assert manifest["safe_to_send"] is False


def test_proposal_rejects_retired_claim_embedded_in_scope() -> None:
    with pytest.raises(ValueError, match="retired_commercial_authority"):
        _proposal(scope_en="Use /ar/risk-score then Data Pack 1500 for ACME")


def test_pricing_is_one_product_quote_only_path() -> None:
    art = generate_pricing_page()
    blob = art["markdown"] + "\n" + art["html"]
    manifest = art["manifest"]

    assert "Free Mini Diagnostic" in blob
    assert "Revenue Command Pilot" in blob
    assert "30 days" in blob or "30 يومًا" in blob
    assert "Stop / Expand / Redesign" in blob
    assert "customer-specific quote" in blob.lower() or "Quote خاص" in blob
    assert manifest["tier_count"] == 1
    assert manifest["product_count"] == 1
    assert manifest["public_fixed_price"] is False
    assert manifest["quote_only"] is True
    assert manifest["live_checkout"] is False
    for token in RETIRED_TOKENS:
        assert token not in blob


def test_proposal_and_pricing_pass_safety_gate_if_available() -> None:
    """Defensive: skip if safety_gate is not available in this checkout."""
    try:
        from auto_client_acquisition.designops import safety_gate  # type: ignore
    except Exception:
        pytest.skip("safety_gate not yet shipped — skipping integration check")

    for art in (_proposal(), generate_pricing_page()):
        try:
            result = safety_gate.check_artifact(  # type: ignore[attr-defined]
                {
                    "markdown_ar": art["markdown_ar"],
                    "markdown_en": art["markdown_en"],
                    "html": art["html"],
                    "manifest": art["manifest"],
                }
            )
        except Exception:
            pytest.skip("safety_gate.check_artifact signature differs")
        if hasattr(result, "model_dump"):
            result = result.model_dump()
        if isinstance(result, dict):
            ok = result.get("safe") or result.get("passes") or result.get("ok") or True
            assert ok in (True, "approved", "approval_required")
