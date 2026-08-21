from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/commercial/founder_money_truth.py"


def _run() -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_template_payment_seed_is_not_counted_as_real_cash() -> None:
    snapshot = _run()
    assert snapshot["verified_payment_event_count"] == 0
    assert snapshot["verified_cash_sar"] == "UNKNOWN"
    assert snapshot["source_schema_has_cash_amount"] is False


def test_current_public_commercial_surfaces_have_one_quote_only_authority() -> None:
    snapshot = _run()
    public = snapshot["public_commercial_truth"]
    assert public["status"] == "PASS", public["findings"]
    assert "Customer-specific Quote" in public["authority"]
    assert "30-Day Revenue Command Pilot" in public["authority"]


def test_money_truth_keeps_sensitive_actions_blocked() -> None:
    snapshot = _run()
    safety = snapshot["safety"]
    assert safety == {
        "live_send": False,
        "live_charge": False,
        "quote_authority": False,
        "production_mutation": False,
        "fake_proof": False,
    }


def test_finance_policy_is_advisory_and_approval_gated() -> None:
    snapshot = _run()
    finance = snapshot["commercial_finance_policy"]
    assert finance["status"] == "AVAILABLE"
    assert finance["approval_required"] is True
    assert finance["external_action_allowed"] is False
    assert finance["policies"]["managed"]["gross_margin_floor_pct"] == 50.0
    assert finance["policies"]["retainer"]["gross_margin_floor_pct"] == 60.0
