from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dealix.business_now.commercial_strategy import _next_best_actions, _ops_client_pack


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_commercial_authority_source_map_v1.py"
COMPANY_BRAIN_PACK_GENERATOR = ROOT / "scripts" / "commercial" / "generate_company_brain_pack.py"


def test_commercial_authority_source_map_matches_live_repository() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "COMMERCIAL_AUTHORITY_SOURCE_MAP_V1_PASS" in completed.stdout
    assert "closure_verdict=PASS" in completed.stdout
    assert "unresolved_count=0" in completed.stdout
    assert completed.stderr == ""


def test_business_now_client_pack_has_no_global_price_authority() -> None:
    pack = _ops_client_pack()

    assert "suggested_price_sar_range" not in pack
    assert "suggested_price_premium_sar" not in pack
    assert pack["public_fixed_price"] is False
    assert pack["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert pack["quote_requires_founder_approval"] is True
    assert "Revenue Command Pilot" in pack["primary_offer_pitch_ar"]
    assert "30-Day Revenue Command Pilot" not in pack["primary_offer_pitch_ar"]


def test_business_now_pilot_action_uses_canonical_paid_motion() -> None:
    actions = _next_best_actions({"stage": "pilot_execution"})
    primary = actions[0]["action_ar"]

    assert "Sprint 499" not in primary
    assert "Revenue Command Pilot" in primary
    assert "30 يوماً" in primary
    assert "إثبات الدفع" in primary


def test_company_brain_pack_generator_cannot_recreate_retired_offer_ladder() -> None:
    text = COMPANY_BRAIN_PACK_GENERATOR.read_text(encoding="utf-8")

    for forbidden in (
        "7-Day Operating Diagnostic",
        "7-Day Revenue Command Room Sprint",
        "Offer a 7-day proof sprint",
        "499 SAR",
        "999 SAR",
        "1,500 SAR",
        "monthly operating retainer",
    ):
        assert forbidden not in text

    for required in (
        'CANONICAL_ENTRY_OFFER = "Free Mini Diagnostic"',
        'CANONICAL_PAID_OFFER = "Revenue Command Pilot"',
        "Customer-Specific Quote",
        "Verified Payment",
        "Customer-Validated Proof",
        "Stop / Expand / Redesign",
        '"public_fixed_price": False',
        '"public_checkout": False',
        '"customer_specific_quote_only": True',
        '"live_send_allowed": False',
        '"live_charge_allowed": False',
    ):
        assert required in text
