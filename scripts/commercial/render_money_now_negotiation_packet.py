#!/usr/bin/env python3
"""DEALIX_MONEY_NOW_NEGOTIATION_PACKET — draft-only, evidence-bound, no invention.

Reads the canonical company work queue and renders a founder-facing negotiation
packet for the nearest-to-cash relationships.

Firewalls enforced here:
* never sends, charges, publishes, quotes, or mutates production;
* never invents a price or economic amount — amounts are absent unless supplied
  by the source queue evidence;
* never promotes a negotiation item to revenue or pipeline (``counts_as_*``
  must be false in the source; otherwise the packet is marked INVALID);
* the final action hash stays PENDING until the exact draft payload exists, so
  no hash is fabricated for an action that has not been authored.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_QUEUE = Path("/opt/dealix/company-os/founder-os/queues/COMPANY_WORK_QUEUE.json")
DEFAULT_REPORT_DIR = Path("reports/commercial/money_now")

ACTION_TYPE = "send_gmail"
ENVIRONMENT = "external"
NEGOTIATION_STATUSES = frozenset({"NEGOTIATION", "REPLY_READY", "COUNTER_READY"})


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "unknown"


def load_queue(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"schema": "company_work_queue_v1", "generated_at": None, "items": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"schema": "company_work_queue_v1", "generated_at": None, "items": []}


def select_negotiation_items(queue: dict[str, Any]) -> list[dict[str, Any]]:
    items = queue.get("items") or []
    selected = [
        item
        for item in items
        if str(item.get("status", "")).upper() in NEGOTIATION_STATUSES
        or str(item.get("next_action", "")).upper() == "NEGOTIATION"
    ]
    return sorted(selected, key=lambda item: float(item.get("priority", 0)), reverse=True)


def build_packet_item(item: dict[str, Any]) -> dict[str, Any]:
    counts_revenue = bool(item.get("counts_as_revenue"))
    counts_pipeline = bool(item.get("counts_as_pipeline"))
    target = str(item.get("target") or item.get("id") or "UNKNOWN")
    return {
        "id": item.get("id"),
        "target": target,
        "owner": item.get("owner"),
        "area": item.get("area"),
        "status": item.get("status"),
        "priority": item.get("priority"),
        "evidence": list(item.get("evidence") or []),
        "counts_as_revenue": counts_revenue,
        "counts_as_pipeline": counts_pipeline,
        "truth_ok": not counts_revenue and not counts_pipeline,
        "approval_required": True,
        "external_send": False,
        "approval_hash_input": {
            "action_type": ACTION_TYPE,
            "target": slugify(target),
            "environment": ENVIRONMENT,
            "payload": "PENDING_EXACT_DRAFT_PAYLOAD",
        },
        "action_hash": "PENDING_EXACT_DRAFT_PAYLOAD",
        "amount": "UNKNOWN_NOT_INVENTED",
        "next_action": item.get("next_action"),
        "founder_minutes": item.get("founder_minutes"),
    }


def build_packet(queue: dict[str, Any], *, generated_at: str | None = None) -> dict[str, Any]:
    items = [build_packet_item(item) for item in select_negotiation_items(queue)]
    return {
        "schema": "dealix.money-now.negotiation-packet.v1",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "source": {
            "queue_schema": queue.get("schema"),
            "queue_generated_at": queue.get("generated_at"),
            "queue_fingerprint": queue.get("fingerprint"),
        },
        "item_count": len(items),
        "items": items,
        "firewalls": {
            "external_send": False,
            "live_charge": False,
            "quote_authority": False,
            "production_mutation": False,
            "amounts_invented": False,
        },
        "approval_note": "Final ACTION_HASH requires the exact draft payload authored by the founder.",
    }


def verify_packet(packet: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for item in packet.get("items", []):
        if item.get("counts_as_revenue") or item.get("counts_as_pipeline"):
            failures.append(f"{item.get('id')}: negotiation item promoted to revenue/pipeline")
        if item.get("external_send") is not False:
            failures.append(f"{item.get('id')}: external_send must be false")
        if item.get("action_hash") != "PENDING_EXACT_DRAFT_PAYLOAD":
            failures.append(f"{item.get('id')}: fabricated action hash")
        if item.get("amount") != "UNKNOWN_NOT_INVENTED":
            failures.append(f"{item.get('id')}: invented amount")
    return failures


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# Money Now — Negotiation Packet (draft-only)",
        "",
        f"- generated_at: `{packet['generated_at']}`",
        f"- items: `{packet['item_count']}`",
        f"- external_send: `{packet['firewalls']['external_send']}`",
        f"- approval: {packet['approval_note']}",
        "",
    ]
    for item in packet["items"]:
        lines.extend(
            [
                f"## {item['target']} (`{item['id']}`)",
                f"- status: `{item['status']}` · priority `{item['priority']}` · owner `{item['owner']}`",
                f"- counts_as_revenue: `{item['counts_as_revenue']}` · counts_as_pipeline: `{item['counts_as_pipeline']}`",
                f"- amount: `{item['amount']}`",
                f"- next_action: `{item['next_action']}` · founder_minutes: `{item['founder_minutes']}`",
                "- evidence:",
            ]
        )
        evidence = item.get("evidence") or []
        lines.extend(f"  - {entry}" for entry in evidence) if evidence else lines.append("  - (none)")
        lines.extend(
            [
                f"- approval_hash_input: `{json.dumps(item['approval_hash_input'], ensure_ascii=False)}`",
                f"- action_hash: `{item['action_hash']}`",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Money Now negotiation packet (draft-only)")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    packet = build_packet(load_queue(args.queue))
    failures = verify_packet(packet)

    args.report_dir.mkdir(parents=True, exist_ok=True)
    (args.report_dir / "latest.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.report_dir / "latest.md").write_text(render_markdown(packet), encoding="utf-8")

    if args.json:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        print(f"MONEY_NOW_PACKET_ITEMS={packet['item_count']}")
        print(f"MONEY_NOW_EXTERNAL_SEND={packet['firewalls']['external_send']}")
        print(f"REPORT_JSON={args.report_dir / 'latest.json'}")
        print(f"REPORT_MD={args.report_dir / 'latest.md'}")
    for failure in failures:
        print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
