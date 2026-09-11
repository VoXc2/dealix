#!/usr/bin/env python3
"""Export executive company state artifacts (deterministic, read-only inputs).

Maintains the runtime artifacts requested by the company operating law:
LATEST_TRUTH.md, AGENT_RUNTIME_STATUS.json, MODEL_SCORECARD.json,
SECTOR_PORTFOLIO_INDEX.json, COMPANY_QUEUE_SUMMARY.json.

Scores that require live evidence stay UNKNOWN — never invented.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FOUNDER_OS = Path("/opt/dealix/company-os/founder-os")
CURRENT = FOUNDER_OS / "current"
QUEUES = FOUNDER_OS / "queues"
BROKER_STATE = CURRENT / "model_economics" / "GO_BROKER_STATE.json"
WORK_QUEUE = QUEUES / "COMPANY_WORK_QUEUE.json"

AGENT_OWNER_MAP = {
    "dealix-pm": ["founder", "revenue-copilot", "capability-research"],
    "dealix-sales": ["dealix-sales", "sales-negotiation", "market-partner-scout"],
    "dealix-delivery": ["delivery", "delivery-verifier"],
    "dealix-engineer": ["production-sre", "engineering-verifier", "revenue-copilot"],
    "dealix-content": ["content", "capability-research"],
}

UNKNOWN = "UNKNOWN"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def latest_truth_markdown() -> str:
    truth = _load_json(CURRENT / "LATEST_TRUTH.json")
    economic = truth.get("economic_truth", {})
    lines = [
        "# LATEST TRUTH (exported)",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Source: {CURRENT / 'LATEST_TRUTH.json'}",
        "",
        f"- verified_revenue_sar: {economic.get('verified_revenue_sar', UNKNOWN)}",
        f"- verified_paid_pilots: {economic.get('verified_paid_pilots', UNKNOWN)}",
        f"- real_contacts: {economic.get('real_contacts', UNKNOWN)}",
        f"- paid_pilot_markers: {economic.get('paid_pilot_markers', UNKNOWN)}",
        f"- generated_pipeline_pressure: {economic.get('generated_pipeline_pressure', UNKNOWN)}",
        "",
        "Markers and synthetic pressure are never revenue or pipeline.",
        "",
    ]
    return "\n".join(lines)


def queue_summary() -> dict[str, Any]:
    payload = _load_json(WORK_QUEUE)
    items = payload.get("items", [])
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "item_count": len(items),
        "fingerprint": payload.get("fingerprint", UNKNOWN),
        "top_items": [
            {
                "priority": item.get("priority"),
                "area": item.get("area"),
                "owner": item.get("owner"),
                "status": item.get("status"),
                "next_action": item.get("next_action"),
            }
            for item in items[:5]
        ],
        "counts_as_revenue": False,
    }


def agent_runtime_status() -> dict[str, Any]:
    payload = _load_json(WORK_QUEUE)
    items = payload.get("items", [])
    agents: dict[str, Any] = {}
    for agent, owners in AGENT_OWNER_MAP.items():
        owned = [item for item in items if item.get("owner") in owners]
        active = [item for item in owned if str(item.get("status", "")).upper() not in ("WAITING", "IDLE")]
        agents[agent] = {
            "state": "ACTIVE_HIGH_VALUE_WORK" if active else "WAITING_FOR_EVENT",
            "queue_items": len(owned),
            "top_item": (owned[0].get("next_action") if owned else None),
            "last_evidence": (owned[0].get("evidence") if owned else []),
            "autonomy": "L0-L4_ONLY",
        }
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "permanent_agent_count": 5,
        "deep_wip_max": 3,
        "agents": agents,
    }


def model_scorecard() -> dict[str, Any]:
    broker = _load_json(BROKER_STATE)
    jobs = broker.get("jobs", [])
    models = sorted({str(job.get("model", UNKNOWN)) for job in jobs if job.get("model")})
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "scorecard_status": "PENDING_BOUNDED_BENCHMARKS",
        "models_observed_in_jobs": models,
        "quality_score": UNKNOWN,
        "arabic_score": UNKNOWN,
        "tool_reliability": UNKNOWN,
        "cost_efficiency": UNKNOWN,
        "note": "Scores require bounded real-task benchmarks; UNKNOWN is not a pass.",
        "paid_spill": "DISABLED_BY_DEFAULT",
    }


def sector_portfolio_index() -> dict[str, Any]:
    from dealix.commercial.sector_company_blueprint import portfolio_index

    return portfolio_index()


def write_all(out_dir: Path = CURRENT) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "LATEST_TRUTH.md": latest_truth_markdown(),
        "AGENT_RUNTIME_STATUS.json": json.dumps(agent_runtime_status(), indent=2, ensure_ascii=False),
        "MODEL_SCORECARD.json": json.dumps(model_scorecard(), indent=2, ensure_ascii=False),
        "SECTOR_PORTFOLIO_INDEX.json": json.dumps(sector_portfolio_index(), indent=2, ensure_ascii=False),
        "COMPANY_QUEUE_SUMMARY.json": json.dumps(queue_summary(), indent=2, ensure_ascii=False),
    }
    written: dict[str, str] = {}
    for name, content in artifacts.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        written[name] = str(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Dealix executive company state artifacts")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.write:
        written = write_all()
        for name, path in written.items():
            print(f"WROTE={name} PATH={path}")
        return 0
    summary = {
        "queue": queue_summary(),
        "agents": agent_runtime_status(),
        "model_scorecard": model_scorecard(),
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"QUEUE_ITEMS={summary['queue']['item_count']}")
        for agent, state in summary["agents"]["agents"].items():
            print(f"AGENT={agent} STATE={state['state']} ITEMS={state['queue_items']}")
        print(f"MODEL_SCORECARD={summary['model_scorecard']['scorecard_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
