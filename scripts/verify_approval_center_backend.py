#!/usr/bin/env python3
"""Emit a redacted read-only receipt for Approval Center backend readiness.

Approval state may be durable in Postgres while founder pre-approval rules still
live in a node-local JSONL file. Active local rules are therefore a production
consistency HOLD: different workers/restarts must not gain different automatic
approval authority. A deployment with no active founder rules can still pass the
backend gate and use normal action-bound approvals.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.approval_center import approval_store_backend_status
from auto_client_acquisition.approval_center.founder_rules import FounderRuleEngine


def _founder_rule_storage_status() -> dict[str, object]:
    """Return a redacted read-only posture for founder pre-approval rules."""
    engine = FounderRuleEngine()
    try:
        configured_count = len(engine.list_rules())
        active_count = len(engine.list_active_rules())
    except Exception:
        return {
            "founder_rules_storage": "local_jsonl",
            "founder_rules_configured_count": None,
            "founder_rules_active_count": None,
            "founder_rules_auto_approval_ready": False,
            "founder_rules_reason": "founder_rules_read_failed",
        }

    if active_count:
        return {
            "founder_rules_storage": "local_jsonl",
            "founder_rules_configured_count": configured_count,
            "founder_rules_active_count": active_count,
            "founder_rules_auto_approval_ready": False,
            "founder_rules_reason": "active_founder_rules_not_shared_durable",
        }

    return {
        "founder_rules_storage": "local_jsonl",
        "founder_rules_configured_count": configured_count,
        "founder_rules_active_count": 0,
        "founder_rules_auto_approval_ready": False,
        "founder_rules_reason": "no_active_founder_rules_manual_approval_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    receipt = {
        "schema": "dealix.approval-center-backend-readiness.v1",
        **approval_store_backend_status(),
        **_founder_rule_storage_status(),
        "table": "approval_center_snapshots",
        "migration": "20260905_022_approval_center_snapshots",
        "read_only": True,
        "contains_secret": False,
    }

    # Durable approval state is not enough to call production authority ready if
    # node-local founder rules can grant execution authority. Fail closed until
    # rule state itself has a shared durable source of truth. Zero active rules
    # is safe: the system simply falls back to action-bound/manual approval.
    if receipt.get("founder_rules_active_count") not in {0, None}:
        receipt["verdict"] = "HOLD"
        receipt["reason"] = "active_founder_rules_not_shared_durable"
    elif receipt.get("founder_rules_active_count") is None:
        receipt["verdict"] = "HOLD"
        receipt["reason"] = "founder_rules_read_failed"

    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for key, value in receipt.items():
            print(f"{key}={value}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
