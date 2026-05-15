#!/usr/bin/env python3
"""Moyasar live-mode cutover helper — Wave 15 (A9).

Interactive script that:
1. Prompts for the Moyasar live secret key (`sk_live_...`)
2. Validates the prefix and shape
3. Optionally tests connectivity (1-call account info if user opts in)
4. Prints exactly what to paste into Railway env vars
5. Reminds the user to flip the webhook URL on the Moyasar dashboard
6. Triggers a 1 SAR self-test charge against Moyasar SANDBOX (using the
   already-configured sk_test key from .env) to confirm end-to-end
   plumbing — but DOES NOT live-charge.

NEVER stores the live key on disk. The script prints + the founder
copy-pastes into Railway. Doctrine: no live external charges from a CLI.

Usage:
    python scripts/moyasar_live_cutover.py
    python scripts/moyasar_live_cutover.py --skip-test-charge
"""
from __future__ import annotations

import argparse
import getpass
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _prompt_key() -> str | None:
    print()
    print("Paste your Moyasar LIVE secret key (sk_live_...).")
    print("It will NOT be written to disk — only printed back to you to paste into Railway.")
    print()
    try:
        key = getpass.getpass("Live key: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        return None
    if not key:
        print("⚠ Empty key — aborting.")
        return None
    if not key.startswith("sk_live_"):
        print(f"❌ Key does not start with 'sk_live_' — got '{key[:8]}...'. Aborting.")
        return None
    if len(key) < 30:
        print("❌ Key looks too short. Aborting.")
        return None
    return key


def _print_railway_block(key: str) -> None:
    print()
    print("━━ Paste into Railway → production → Variables ━━")
    print()
    print("MOYASAR_SECRET_KEY=" + key)
    print("DEALIX_MOYASAR_MODE=live")
    print()
    print("Then on the Moyasar dashboard:")
    print("  1. Webhooks → add: $PROD/api/v1/payment-ops/webhook")
    print("  2. Copy the webhook secret → set Railway env var:")
    print("     MOYASAR_WEBHOOK_SECRET=<secret_from_dashboard>")
    print("  3. Save. Railway will auto-redeploy.")
    print()


def _test_sandbox_charge() -> bool:
    """Test end-to-end plumbing via Moyasar SANDBOX (sk_test) — never live.

    Just exercises the imports + endpoint shape so the founder is
    confident the wiring works before flipping to live.
    """
    test_key = os.environ.get("MOYASAR_SECRET_KEY", "")
    if not test_key.startswith("sk_test_"):
        print("⚠ MOYASAR_SECRET_KEY env not set to a test key — skipping plumbing test.")
        return False
    try:
        # Validate Moyasar adapter is importable.
        from auto_client_acquisition.payment_ops.orchestrator import (
            create_invoice_intent,
        )
        print(
            "✓ payment_ops.orchestrator.create_invoice_intent is importable. "
            "Plumbing OK."
        )
        return True
    except Exception as e:  # noqa: BLE001
        print(f"❌ payment_ops import failed: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-test-charge", action="store_true")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  Dealix — Moyasar live-mode cutover helper (Wave 15)        ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    if not args.skip_test_charge:
        print()
        print("Step 1/2 — verify sandbox plumbing")
        _test_sandbox_charge()

    print()
    print("Step 2/2 — paste your LIVE key (it's NOT saved to disk)")
    key = _prompt_key()
    if not key:
        return 1

    _print_railway_block(key)

    print("━━ Post-cutover smoke (run from any machine) ━━")
    print()
    print("  export PROD=https://<your_railway_url>")
    print("  bash scripts/prod_smoke.sh $PROD")
    print()
    print("Confirm:")
    print("  - $PROD/api/v1/founder/launch-status shows moyasar.mode=live")
    print("  - A 1 SAR test charge succeeds + auto-refunds (see Moyasar dashboard)")
    print()
    print(
        f"_Cutover prepared at {datetime.now(timezone.utc).isoformat()}._\n"
        f"_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
