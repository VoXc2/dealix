#!/usr/bin/env python3
"""Emit a redacted read-only receipt for Approval Center backend readiness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.approval_center import approval_store_backend_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    receipt = {
        "schema": "dealix.approval-center-backend-readiness.v1",
        **approval_store_backend_status(),
        "table": "approval_center_snapshots",
        "migration": "20260905_022_approval_center_snapshots",
        "read_only": True,
        "contains_secret": False,
    }
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for key, value in receipt.items():
            print(f"{key}={value}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
