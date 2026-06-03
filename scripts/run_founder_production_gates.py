#!/usr/bin/env python3
"""Founder production gates — Railway + live trust layer + GTM repo + weekly blockers."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_production_gates import (
    build_founder_production_gates,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--ui-start-command", default=os.getenv("RAILWAY_UI_START_COMMAND", ""))
    p.add_argument("--ui-predeploy", default=os.getenv("RAILWAY_UI_PREDEPLOY", ""))
    args = p.parse_args()

    blob = build_founder_production_gates(
        api_base=args.api_base,
        skip_live=args.skip_live,
        ui_start_command=args.ui_start_command,
        ui_predeploy=args.ui_predeploy,
    )

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== Founder production gates ==")
        print(f"  api: {blob.get('api_base') or 'skipped'}")
        print(f"  railway: {blob['railway']['verdict']}")
        print(f"  gtm_surfaces_repo: {'ok' if blob['gtm_surfaces_repo'].get('ok') else 'FAIL'}")
        print(f"  weekly_metrics: {blob['weekly_metrics']['verdict']}")
        trust = blob["railway"].get("live_trust_layer") or {}
        for key, row in (trust.get("probes") or {}).items():
            if row.get("probed"):
                print(f"  live {key}: {row.get('url')} -> {row.get('status', row.get('error'))}")
        for action in blob.get("founder_actions_ar") or []:
            print(f"  ACTION: {action}")

    print(f"FOUNDER_PRODUCTION_GATES_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] in ("PASS", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
