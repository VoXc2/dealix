#!/usr/bin/env python3
"""Verify Railway config-as-code + optional live /healthz on api.dealix.me."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_production import (  # noqa: E402
    analyze_railway_production,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--api-base",
        default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"),
        help="Production API base for /healthz probe",
    )
    p.add_argument("--skip-live", action="store_true", help="Repo checks only")
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--ui-start-command",
        default=os.getenv("RAILWAY_UI_START_COMMAND", ""),
        help="Pass current Railway UI start command to detect drift",
    )
    p.add_argument(
        "--ui-predeploy",
        default=os.getenv("RAILWAY_UI_PREDEPLOY", ""),
        help="Pass current Railway UI pre-deploy command to detect drift",
    )
    args = p.parse_args()

    api_base = None if args.skip_live else (args.api_base or "").strip()
    blob = analyze_railway_production(api_base=api_base)

    drift = parse_railway_ui_drift_hint(args.ui_start_command)
    if drift:
        blob["ui_start_command_drift"] = drift
    predeploy_drift = parse_railway_ui_predeploy_drift(args.ui_predeploy)
    if predeploy_drift:
        blob["ui_predeploy_drift"] = predeploy_drift

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== verify_railway_production_config ==")
        repo = blob["repo"]
        for w in repo.get("warnings", []):
            print(f"  WARN: {w}")
        for issue in repo.get("issues", []):
            print(f"  FAIL: {issue}")
        if repo.get("ok"):
            print("  ok: repo railway config")
        live = blob["live_healthz"]
        if live.get("probed"):
            status = live.get("status", live.get("error", "?"))
            print(f"  live /healthz: {live.get('url')} -> {status}")
        else:
            print("  live /healthz: skipped")
        trust = blob.get("live_trust_layer") or {}
        hint = trust.get("deploy_stale_hint_ar")
        if hint:
            print(f"  FOUNDER_ACTION (deploy): {hint}")
        for key, row in (trust.get("probes") or {}).items():
            if row.get("probed"):
                print(f"  live {key}: {row.get('url')} -> {row.get('status', row.get('error'))}")
        if drift:
            print(f"  FOUNDER_ACTION (start): {drift}")
        if predeploy_drift:
            print(f"  FOUNDER_ACTION (predeploy): {predeploy_drift}")
        print(f"  settings: {blob['settings_doc']}")

    print(f"RAILWAY_PRODUCTION_CONFIG_VERDICT={blob['verdict']}")
    if blob["verdict"] == "FAIL":
        return 1
    if blob["verdict"] == "WARN":
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
