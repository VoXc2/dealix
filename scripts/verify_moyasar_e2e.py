#!/usr/bin/env python3
"""Moyasar sandbox E2E checklist — webhook route + side-effects (no live charge)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "http://localhost:8000"))
    args = p.parse_args()

    checks: list[tuple[str, bool, str]] = []

    moyasar_key = bool((os.getenv("MOYASAR_SECRET_KEY") or "").strip())
    webhook_secret = bool((os.getenv("MOYASAR_WEBHOOK_SECRET") or "").strip())
    checks.append(("MOYASAR_SECRET_KEY", moyasar_key, "sk_test_* or sk_live_*"))
    checks.append(("MOYASAR_WEBHOOK_SECRET", webhook_secret, "matches Moyasar dashboard"))

    try:
        from dealix.commercial_ops.railway_production import probe_get

        route = probe_get(args.api_base.rstrip("/"), "/api/v1/webhooks/moyasar", timeout_sec=8.0)
        route_ok = route.get("status") not in (404, None)
        checks.append(("webhook_route_live", route_ok, f"status={route.get('status')}"))
    except Exception as exc:
        checks.append(("webhook_route_live", False, str(exc)))

    try:
        from dealix.commercial_ops.moyasar_payment_sync import process_moyasar_payment_side_effects

        dry = process_moyasar_payment_side_effects(
            payment={"status": "pending", "metadata": {"email": "x@y.com"}},
            event_type="payment_created",
        )
        checks.append(("side_effects_import", True, str(dry.get("hubspot_sync", {}).get("skipped"))))
    except Exception as exc:
        checks.append(("side_effects_import", False, str(exc)))

    print("== Moyasar E2E checklist ==")
    failed = 0
    for name, ok, detail in checks:
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark}] {name}: {detail}")
        if not ok:
            failed += 1

    print(f"MOYASAR_E2E_VERDICT={'PASS' if failed == 0 else 'FAIL'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
