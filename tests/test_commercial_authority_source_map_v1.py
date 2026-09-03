from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dealix.business_now.commercial_strategy import _next_best_actions, _ops_client_pack


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "verify_commercial_authority_source_map_v1.py"


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
    assert "30-Day Revenue Command Pilot" in pack["primary_offer_pitch_ar"]


def test_business_now_pilot_action_uses_canonical_paid_motion() -> None:
    actions = _next_best_actions({"stage": "pilot_execution"})
    primary = actions[0]["action_ar"]

    assert "Sprint 499" not in primary
    assert "Revenue Command Pilot" in primary
    assert "30 يوماً" in primary
    assert "إثبات الدفع" in primary
