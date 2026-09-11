#!/usr/bin/env python3
"""COMPANY_WORK_QUEUE — canonical prioritized work with change detection.

Read-only ingest of Founder OS queues and the latest V18 portfolio command.
Deterministic; no LLM. Approvals stay pending; nothing counts as revenue or
pipeline unless the canonical source already says so.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

FOUNDER_OS = Path("/opt/dealix/company-os/founder-os")
QUEUES = FOUNDER_OS / "queues"
STATE_PATH = QUEUES / "COMPANY_WORK_QUEUE_STATE.json"
OUT_JSON = QUEUES / "COMPANY_WORK_QUEUE.json"
OUT_MD = QUEUES / "COMPANY_WORK_QUEUE.md"

REPORT_CANDIDATES = (
    Path("/opt/dealix/workspace/dealix/reports/founder"),
    Path("/opt/dealix/workspace/dealix-diag-v2/reports/founder"),
    Path("/opt/dealix/workspace/dealix-ops/reports/founder"),
)

RELATIONSHIP_PROBABILITY = {
    "real_relationship": 0.7,
    "negotiation": 0.6,
    "inbound": 0.5,
    "warm": 0.4,
    "no_relationship_yet": 0.2,
    "outbound_sent": 0.1,
    "research": 0.05,
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return []
    header = lines[0].split("\t")
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        values = line.split("\t")
        rows.append({header[i]: (values[i] if i < len(values) else "") for i in range(len(header))})
    return rows


def latest_v18_command() -> dict[str, Any]:
    best: tuple[float, Path] | None = None
    for reports_dir in REPORT_CANDIDATES:
        if not reports_dir.exists():
            continue
        for candidate in reports_dir.glob("V18_PORTFOLIO_COMMAND_*.json"):
            mtime = candidate.stat().st_mtime
            if best is None or mtime > best[0]:
                best = (mtime, candidate)
    if best is None:
        return {}
    try:
        return json.loads(best[1].read_text(encoding="utf-8")).get("command", {})
    except json.JSONDecodeError:
        return {}


def priority_score(item: dict[str, Any]) -> float:
    numerator = (
        0.35 * float(item.get("economic_probability", 0.3))
        + 0.25 * float(item.get("value", 0.5))
        + 0.20 * float(item.get("urgency", 0.5))
        + 0.10 * float(item.get("strategic_fit", 0.7))
        + 0.10 * (0.5 * float(item.get("customer_value", 0.5)) + 0.5 * float(item.get("learning_value", 0.3)))
    )
    founder_factor = max(0.5, float(item.get("founder_minutes", 15)) / 15.0)
    cost_factor = max(0.5, float(item.get("estimated_cost", 0.2)) / 0.2)
    risk_factor = max(0.5, float(item.get("risk", 0.3)) / 0.3)
    deps = len(item.get("dependencies", []) or [])
    denominator = founder_factor * cost_factor * risk_factor * (1.0 + 0.5 * deps)
    return round(numerator / denominator * 100, 2)


def items_from_action_queue() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in read_tsv(QUEUES / "ACTION_QUEUE.tsv"):
        priority = int(row.get("priority", "5") or 5)
        score = float(row.get("score", "50") or 50)
        owner = row.get("owner", "dealix-pm")
        items.append(
            {
                "id": f"action-{priority}-{row.get('domain', 'general').lower().replace(' ', '-')}",
                "area": row.get("domain", "GENERAL"),
                "owner": owner,
                "source": "ACTION_QUEUE",
                "status": row.get("status", "READY"),
                "autonomy": row.get("autonomy", "L0-L3_INTERNAL"),
                "urgency": max(0.1, (11 - priority) / 10.0),
                "value": min(1.0, score / 100.0),
                "economic_probability": 0.3,
                "risk": 0.2,
                "founder_minutes": 15,
                "estimated_cost": 0.1,
                "dependencies": [],
                "evidence": [f"ACTION_QUEUE priority={priority} score={score}"],
                "next_action": "execute internal work within autonomy envelope",
                "counts_as_revenue": False,
                "counts_as_pipeline": False,
            }
        )
    return items


def items_from_approval_queue() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for index, row in enumerate(read_tsv(QUEUES / "APPROVAL_QUEUE.tsv")):
        label = row.get("action") or row.get("title") or row.get("id") or f"approval-{index}"
        items.append(
            {
                "id": f"approval-{index}-{abs(hash(label)) % 10000}",
                "area": "APPROVALS",
                "owner": "founder",
                "source": "APPROVAL_QUEUE",
                "status": "PENDING_FOUNDER",
                "autonomy": "L5",
                "urgency": 0.9,
                "value": 0.8,
                "economic_probability": 0.5,
                "risk": 0.5,
                "founder_minutes": 5,
                "estimated_cost": 0.0,
                "dependencies": [],
                "evidence": [f"APPROVAL_QUEUE: {label}"],
                "next_action": "founder decision required",
                "counts_as_revenue": False,
                "counts_as_pipeline": False,
            }
        )
    return items


def items_from_v18(command: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for move in command.get("top_moves", []) or []:
        relationship = str(move.get("relationship_state", "research")).lower()
        probability = RELATIONSHIP_PROBABILITY.get(relationship, 0.1)
        evidence_strength = float(move.get("evidence_strength", 1) or 1)
        items.append(
            {
                "id": f"v18-{move.get('item_id', 'move')}",
                "area": f"COMMERCIAL/{move.get('lane', 'GENERAL')}",
                "owner": "dealix-sales",
                "source": "V18_PORTFOLIO_COMMAND",
                "status": move.get("current_stage", "UNKNOWN"),
                "autonomy": "L0-L4",
                "urgency": 0.8,
                "value": min(1.0, evidence_strength / 5.0),
                "economic_probability": probability,
                "risk": 0.3,
                "founder_minutes": 10,
                "estimated_cost": 0.1,
                "dependencies": [],
                "evidence": [str(move.get("expected_next_evidence") or move.get("buyability_gap") or "V18_TOP_MOVE")],
                "next_action": str(move.get("current_stage") or "prepare internal next step"),
                "target": move.get("company", "UNKNOWN"),
                "counts_as_revenue": False,
                "counts_as_pipeline": False,
            }
        )
    return items


def build_queue() -> list[dict[str, Any]]:
    command = latest_v18_command()
    items = items_from_action_queue() + items_from_approval_queue() + items_from_v18(command)
    for item in items:
        item["priority"] = priority_score(item)
    return sorted(items, key=lambda item: item["priority"], reverse=True)


def source_paths() -> list[Path]:
    paths = [QUEUES / "ACTION_QUEUE.tsv", QUEUES / "APPROVAL_QUEUE.tsv"]
    for reports_dir in REPORT_CANDIDATES:
        paths.extend(sorted(reports_dir.glob("V18_PORTFOLIO_COMMAND_*.json"))[-1:])
    return paths


def fingerprint(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(set(paths)):
        digest.update(str(path).encode("utf-8"))
        if path.exists():
            digest.update(path.read_bytes()[:500_000])
            digest.update(str(path.stat().st_mtime_ns).encode("utf-8"))
        else:
            digest.update(b"MISSING")
    return digest.hexdigest()


def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_artifacts(items: list[dict[str, Any]], fingerprint_value: str) -> None:
    QUEUES.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "company_work_queue_v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "fingerprint": fingerprint_value,
        "item_count": len(items),
        "items": items,
        "counts_as_revenue": False,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# COMPANY WORK QUEUE",
        "",
        f"Generated: {payload['generated_at']}",
        f"Items: {len(items)}",
        "",
    ]
    for index, item in enumerate(items[:20], start=1):
        lines.append(
            f"{index}. [{item['priority']}] {item['area']} | {item['owner']} | {item['status']} | {item['next_action']}"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATE_PATH.write_text(
        json.dumps({"fingerprint": fingerprint_value, "updated_at": payload["generated_at"]}, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the canonical company work queue (read-only sources)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--force", action="store_true", help="recompute even when inputs are unchanged")
    parser.add_argument("--write", action="store_true", help="write runtime queue artifacts")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    current = fingerprint(source_paths())
    previous = load_state().get("fingerprint")
    if current == previous and not args.force:
        print("COMPANY_WORK_QUEUE=NO_MATERIAL_CHANGE")
        print(f"FINGERPRINT={current}")
        return 0

    items = build_queue()
    print("COMPANY_WORK_QUEUE=OK")
    print(f"ITEM_COUNT={len(items)}")
    print(f"FINGERPRINT={current}")
    for item in items[: args.top]:
        print(f"TOP[{item['priority']}] {item['area']} owner={item['owner']} status={item['status']} :: {item['next_action']}")
    if args.write:
        save_artifacts(items, current)
        print(f"WROTE {OUT_JSON}")
    if args.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
