#!/usr/bin/env python3
"""Dealix 20-sector Hermes fabric.

One scheduler, five permanent agents, twenty temporary sector cells. The fabric
creates deterministic patrol packets for every canonical sector and may submit
bounded internal jobs to the already-running Hermes Session Factory. It never
creates external-send, publish, payment, tender, DNS, deploy, or merge authority.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTES = REPO_ROOT / "data/commercial/op2_sector_diagnostic_routes_v1.json"
DEFAULT_STATE = Path("/opt/dealix/control/state/sector_hermes_fabric")
DEFAULT_FACTORY_STATE = Path("/opt/dealix/control/state/session_factory")
DEFAULT_FACTORY = Path("/opt/dealix/control/runtime/session-factory-819c73e9f4be76ee252059ddef9d6a7c316f3ada/scripts/ops/session_factory.py")
PERMANENT_AGENTS = ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"]
DEEP_WIP_MAX = 3
PATROL_TTL = timedelta(hours=6)
LOCAL_AI_TTL = timedelta(hours=12)
ACTIVE_FACTORY_STATES = {"READY", "CLAIMED", "RUNNING", "VERIFYING", "RECOVERABLE", "WAITING_L5"}
MATERIAL_AUTHORITY = {"external_send": False, "publish": False, "payment": False, "tender": False, "merge": False, "deploy": False, "dns": False, "db": False, "secret": False}
AGENT_ROLES = {
    "dealix-pm": "economic ordering, authority guard, Deep-WIP selection",
    "dealix-sales": "qualify problem, free diagnostic, discovery and quote draft inputs",
    "dealix-delivery": "baseline, acceptance criteria, delivery and proof gaps",
    "dealix-engineer": "automation feasibility and internal implementation planning",
    "dealix-content": "evidence-safe sector content drafts and distribution hypotheses",
}


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def route_hash(route: dict[str, Any]) -> str:
    raw = json.dumps(route, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def build_packet(route: dict[str, Any], rank: int) -> dict[str, Any]:
    top3 = rank <= DEEP_WIP_MAX
    return {
        "schema": "dealix.sector-hermes-cell.v1",
        "generated_at": now_iso(),
        "sector_id": route["sector_id"],
        "research_rank": rank,
        "deep_wip_selected": top3,
        "market_evidence_scope": route.get("market_evidence_scope", "PUBLIC_MARKET_SIGNAL_ONLY_NOT_BUYER_DEMAND"),
        "buyer_demand_status": route.get("buyer_demand_status", "UNKNOWN_NOT_EVIDENCE_BACKED"),
        "buyer": route["buyer"],
        "problem": route["problem"],
        "diagnostic": route["diagnostic_entry"],
        "commercial_pattern": route["commercial_pattern"],
        "agents": [{"agent": agent, "duty": AGENT_ROLES[agent]} for agent in PERMANENT_AGENTS],
        "authority": dict(MATERIAL_AUTHORITY),
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "next_internal_actions": [
            "refresh public market evidence",
            "prepare free diagnostic hypothesis",
            "prepare discovery questions and acceptance criteria",
            "prepare customer-specific proposal inputs only after a real interaction",
            "record proof gaps without fabricating outcomes",
        ],
        "route_hash": route_hash(route),
    }


def build_fabric() -> dict[str, Any]:
    payload = load_json(ROUTES)
    routes = payload["routes"]
    packets = [build_packet(route, index) for index, route in enumerate(routes, start=1)]
    return {
        "schema": "dealix.sector-hermes-fabric.v1",
        "generated_at": now_iso(),
        "sector_count": len(packets),
        "permanent_agents": list(PERMANENT_AGENTS),
        "deep_wip_max": DEEP_WIP_MAX,
        "deep_wip_sectors": [packet["sector_id"] for packet in packets[:DEEP_WIP_MAX]],
        "scheduler_model": "ONE_HERMES_CRON_PLUS_EXISTING_SESSION_FACTORY",
        "opencode_promotion": "DENIED_UNTIL_EXECUTION_PLANE_GREEN",
        "material_authority": dict(MATERIAL_AUTHORITY),
        "cells": packets,
    }


def write_fabric(state_dir: Path) -> dict[str, Any]:
    fabric = build_fabric()
    packets_dir = state_dir / "packets"
    packets_dir.mkdir(parents=True, exist_ok=True)
    for packet in fabric["cells"]:
        (packets_dir / f"{packet['sector_id']}.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False), encoding="utf-8")
    (state_dir / "SECTOR_FABRIC_STATUS.json").write_text(json.dumps(fabric, indent=2, ensure_ascii=False), encoding="utf-8")
    return fabric


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _factory_jobs(factory_state: Path) -> list[dict[str, Any]]:
    jobs_dir = factory_state / "jobs"
    jobs: list[dict[str, Any]] = []
    if not jobs_dir.exists():
        return jobs
    for path in jobs_dir.glob("*.json"):
        try:
            jobs.append(load_json(path))
        except (OSError, json.JSONDecodeError):
            continue
    return jobs


def _sector_job_recent(jobs: list[dict[str, Any]], sector_id: str, kind: str, ttl: timedelta) -> bool:
    marker = f"sector:{sector_id}:{kind}"
    cutoff = datetime.now(UTC) - ttl
    for job in jobs:
        refs = [str(ref) for ref in (job.get("CONTEXT_REFS") or [])]
        if marker not in refs:
            continue
        if job.get("STATUS") in ACTIVE_FACTORY_STATES:
            return True
        created = _parse_time(job.get("CREATED_AT"))
        if created and created >= cutoff and job.get("STATUS") == "SUCCEEDED":
            return True
    return False


def _load_factory_module(path: Path):
    spec = importlib.util.spec_from_file_location("dealix_session_factory_runtime", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load session factory: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def patrol_sector(sector_id: str, state_dir: Path) -> dict[str, Any]:
    fabric = build_fabric()
    cell = next((item for item in fabric["cells"] if item["sector_id"] == sector_id), None)
    if cell is None:
        raise ValueError(f"unknown sector: {sector_id}")
    receipt_dir = state_dir / "receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "dealix.sector-patrol-receipt.v1",
        "generated_at": now_iso(),
        "sector_id": sector_id,
        "route_hash": cell["route_hash"],
        "deep_wip_selected": cell["deep_wip_selected"],
        "agents": cell["agents"],
        "authority": cell["authority"],
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "verdict": "INTERNAL_PATROL_READY",
    }
    path = receipt_dir / f"{sector_id}.json"
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"ok": True, "receipt": str(path), "sector_id": sector_id}


def submit_due_jobs(fabric: dict[str, Any], state_dir: Path, factory_state: Path, factory_script: Path) -> dict[str, Any]:
    factory = _load_factory_module(factory_script)
    jobs = _factory_jobs(factory_state)
    submitted: list[dict[str, Any]] = []
    script = Path(__file__).resolve()
    python_bin = os.environ.get("DEALIX_PYTHON", "/opt/dealix/workspace/dealix/.venv/bin/python")
    for cell in fabric["cells"]:
        sector_id = cell["sector_id"]
        if _sector_job_recent(jobs, sector_id, "patrol", PATROL_TTL):
            continue
        receipt = state_dir / "receipts" / f"{sector_id}.json"
        job = factory.make_job(
            owner_agent="dealix-pm",
            business_goal=f"SECTOR_PATROL::{sector_id} refresh internal commercial readiness packet",
            job_class="MONITORING",
            authority_level="L3",
            economic_reason="Maintain all 20 sectors without creating fake pipeline or duplicate schedulers",
            priority=max(40.0, 90.0 - float(cell["research_rank"])),
            modifying=False,
            executor={"argv": [python_bin, str(script), "--state-dir", str(state_dir), "--patrol-sector", sector_id, "--json"]},
            acceptance={"criteria": "sector patrol receipt written", "checks": [{"kind": "file_contains", "path": str(receipt), "text": "INTERNAL_PATROL_READY"}]},
            context_refs=[f"sector:{sector_id}:patrol", f"route_hash:{cell['route_hash']}"],
            next_action="continue internal patrol; external effects remain gated",
        )
        result = factory.submit_job(factory_state, job)
        if result.get("ok"):
            submitted.append({"sector_id": sector_id, "kind": "patrol", "job_id": job["JOB_ID"]})
    for cell in fabric["cells"][:DEEP_WIP_MAX]:
        sector_id = cell["sector_id"]
        if _sector_job_recent(jobs, sector_id, "local_ai", LOCAL_AI_TTL):
            continue
        prompt = (
            "You are an internal Dealix sector analyst. Return a compact Arabic-first internal brief only. "
            f"Sector={sector_id}. Buyer={cell['buyer']}. Problem={cell['problem']}. "
            f"Diagnostic families={','.join(cell['diagnostic']['priority_families'][:5])}. "
            "Output: 3 diagnostic questions, 3 automation hypotheses, 3 proof requirements, and 1 safe next internal action. "
            "Do not claim buyer demand, relationship, consent, ROI, revenue, or permission to send/publish."
        )
        job = factory.make_job(
            owner_agent="dealix-sales",
            business_goal=f"SECTOR_LOCAL_AI::{sector_id} bounded diagnostic and commercial reasoning",
            job_class="LOCAL_AI",
            authority_level="L2",
            economic_reason="Use cheap local intelligence on only the Top-3 research sectors",
            priority=max(70.0, 100.0 - float(cell["research_rank"])),
            modifying=False,
            executor={"prompt": prompt, "timeout_seconds": 60, "num_predict": 160},
            acceptance={"criteria": "bounded local sector analysis returned"},
            context_refs=[f"sector:{sector_id}:local_ai", f"route_hash:{cell['route_hash']}"],
            next_action="attach analysis to free-diagnostic preparation; do not send externally",
        )
        result = factory.submit_job(factory_state, job)
        if result.get("ok"):
            submitted.append({"sector_id": sector_id, "kind": "local_ai", "job_id": job["JOB_ID"]})
    factory.write_queue_snapshot(factory_state)
    factory.factory_status(factory_state)
    return {"submitted": submitted, "submitted_count": len(submitted)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix 20-sector Hermes fabric")
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--factory-state", type=Path, default=DEFAULT_FACTORY_STATE)
    parser.add_argument("--factory-script", type=Path, default=DEFAULT_FACTORY)
    parser.add_argument("--patrol-sector")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    args.state_dir.mkdir(parents=True, exist_ok=True)
    if args.patrol_sector:
        result = patrol_sector(args.patrol_sector, args.state_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else f"SECTOR_PATROL=PASS {args.patrol_sector}")
        return 0
    fabric = write_fabric(args.state_dir)
    result: dict[str, Any] = {"fabric": fabric, "submit": {"submitted_count": 0, "submitted": []}}
    if args.submit:
        result["submit"] = submit_due_jobs(fabric, args.state_dir, args.factory_state, args.factory_script)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("DEALIX_SECTOR_HERMES_FABRIC=PASS")
        print(f"SECTORS={fabric['sector_count']}")
        print(f"DEEP_WIP={','.join(fabric['deep_wip_sectors'])}")
        print(f"SUBMITTED={result['submit']['submitted_count']}")
        print("EXTERNAL_AUTHORITY=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
