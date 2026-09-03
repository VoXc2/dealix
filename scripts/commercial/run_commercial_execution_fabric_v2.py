#!/usr/bin/env python3
"""Render Dealix Commercial Execution Fabric V2 state without external effects."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _read(path: Path | None) -> dict[str, Any]:
    if path is None or not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def build_snapshot(*, command: dict[str, Any], queue: dict[str, Any]) -> dict[str, Any]:
    activation = command.get("activation_policy") if isinstance(command.get("activation_policy"), dict) else {}
    authority = queue.get("authority") if isinstance(queue.get("authority"), dict) else {}
    items = queue.get("work_items") if isinstance(queue.get("work_items"), list) else []
    return {
        "schema": "dealix.commercial-execution-fabric.snapshot.v2",
        "generated_at": datetime.now(UTC).isoformat(),
        "objective": "VERIFIED_ECONOMIC_MOVEMENT_PER_FOUNDER_MINUTE_PER_COST_PER_RISK",
        "factories": [
            "signal_factory",
            "research_browser_factory",
            "document_tender_factory",
            "conversation_negotiation_factory",
            "external_execution_gate",
            "learning_capability_factory",
        ],
        "canonical_agents": ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"],
        "new_scheduler": False,
        "new_permanent_agent": False,
        "new_truth_store": False,
        "queue_items": len(items),
        "external_effect_defaults": {
            "external_send": bool(activation.get("external_send", False)),
            "public_publish": bool(activation.get("public_publish", False)),
            "paid_spend": bool(activation.get("paid_spend", False)),
            "payment_or_refund": bool(activation.get("payment_or_refund", False)),
            "router_can_send_external": bool(authority.get("router_can_send_external", False)),
        },
        "research": {
            "first_web_adapter": "TAVILY_READ_ONLY_DIRECT_HTTP",
            "stagehand": "PILOT_ISOLATED_OBSERVE_EXTRACT_ONLY",
            "docling": "PILOT_ISOLATED_PROVENANCE_DOCUMENTS",
            "promptfoo": "PILOT_ISOLATED_TRUSTED_CONFIG_ONLY",
            "firecrawl": "DEFER_OVERLAP_AND_LICENSE_SURFACE",
            "crawl4ai": "DEFER_UNTIL_SELF_HOST_CONTROL_OR_COST_GAP_PROVEN",
        },
        "provider_execution": {
            "gmail_api_adapter_present": True,
            "live_provider_default": "QUARANTINED",
            "canonical_action_hash_required": True,
            "packet_integrity_recomputed": True,
            "fresh_canonical_authority_resolver_required": True,
            "durable_idempotency_required": True,
            "unknown_provider_outcome_requires_reconciliation": True,
            "caller_supplied_approval_is_execution_authority": False,
            "current_snapshot_executes_provider": False,
        },
        "truth_firewall": [
            "research!=relationship",
            "public_contact!=consent",
            "draft!=sent",
            "quote!=invoice",
            "invoice!=payment",
            "provider_acceptance!=customer_outcome",
            "synthetic!=customer_proof",
            "cached_approval!=fresh_execution_authority",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", type=Path)
    parser.add_argument("--queue", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        payload = build_snapshot(command=_read(args.command), queue=_read(args.queue))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"DEALIX_COMMERCIAL_EXECUTION_FABRIC_V2=FAIL: {exc}")
        return 1
    _atomic(args.out, payload)
    print(f"DEALIX_COMMERCIAL_EXECUTION_FABRIC_SNAPSHOT={args.out}")
    print("DEALIX_COMMERCIAL_EXECUTION_FABRIC_V2=PASS")
    print("LIVE_PROVIDER_DEFAULT=QUARANTINED")
    print("NEW_SCHEDULER=NO")
    print("NEW_PERMANENT_AGENT=NO")
    print("EXTERNAL_EFFECTS_EXECUTED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
