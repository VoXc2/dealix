#!/usr/bin/env python3
"""Build one five-agent execution wave over all canonical Saudi sectors.

The wave deliberately creates five portfolio jobs, not one agent per sector and
not 100 disconnected jobs. Each permanent agent owns its canonical function
across the same 20-sector truth set. The session factory decides admission and
keeps global deep WIP <= 3.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "ops"))

from opencode_agent_allocator import select_deep_jobs
from session_factory import make_job, state_root, submit_job

from dealix.commercial.sector_commercial_factory import SectorCommercialFactory

OUT_DIR = "docs/company-os/sector-wave"

def _head_sha() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _sector_context() -> tuple[list[str], str]:
    packs = SectorCommercialFactory().build_all()
    sectors = [pack.sector_id for pack in packs]
    summary = ", ".join(sectors)
    return sectors, summary


def _artifact_prompt(role: str, target: str, sector_summary: str, work: str) -> str:
    return f"""DEALIX Ω∞ internal portfolio task. Role={role}.
Use the canonical SectorCommercialFactory and current repository evidence only.
Cover ALL canonical sectors exactly once: {sector_summary}.
{work}
Write a concise evidence-governed receipt to {target}.
Research is not relationship/pipeline/revenue. Do not invent customer facts,
ROI, consent, proof, price authority, or external action. No merge/deploy/send/
publish/payment/DNS/DB/secret mutation. Preserve one Company Machine and five
permanent agents. End the receipt with L5_EXECUTED=NONE.
"""

def build_jobs(base_sha: str | None = None) -> list[dict[str, Any]]:
    sectors, sector_summary = _sector_context()
    if len(sectors) != 20 or len(set(sectors)) != 20:
        raise RuntimeError("CANONICAL_SECTOR_COVERAGE_NOT_20")
    base = base_sha or _head_sha()
    specs = [
        (
            "dealix-sales", "COMMERCIAL_REASONING", 95.0,
            "SALES_PORTFOLIO_RECEIPT.md",
            "For every sector: extract ICP/buyers/problems/triggers, free diagnostic entry, canonical offer match, qualification gaps and next internal commercial action. Rank only as research hypotheses.",
        ),
        (
            "dealix-engineer", "ENGINEERING", 94.0,
            "ENGINEERING_PORTFOLIO_RECEIPT.md",
            "Verify the 20 sector packs, diagnostic paths, integration surfaces and website derivation contracts. Identify code/test gaps and apply only bounded L4-safe fixes with focused tests.",
        ),
        (
            "dealix-delivery", "DELIVERY", 93.0,
            "DELIVERY_PORTFOLIO_RECEIPT.md",
            "For every sector: map delivery module, acceptance evidence, proof requirements, customer-value measurement boundary, security/privacy constraints and delivery risks.",
        ),
    ]
    specs.extend(
        [
            (
                "dealix-pm", "RESEARCH", 86.0,
                "PM_PORTFOLIO_RECEIPT.md",
                "Review cross-sector economic ordering, evidence freshness, Deep-WIP conflicts, governance gaps and the smallest next safe action. Do not convert research into pipeline.",
            ),
            (
                "dealix-content", "RESEARCH", 82.0,
                "CONTENT_PORTFOLIO_RECEIPT.md",
                "For every sector: validate Arabic/English positioning, SEO themes and truthful free-diagnostic CTA. Produce draft-only content gaps; never publish.",
            ),
        ]
    )
    jobs: list[dict[str, Any]] = []
    for owner, job_class, priority, filename, work in specs:
        target = f"{OUT_DIR}/{filename}"
        scope = [target]
        tests: list[str] = []
        if owner == "dealix-engineer":
            scope += ["dealix/commercial", "scripts/ops", "tests"]
            tests = ["tests/test_sector_commercial_factory.py", "tests/test_session_factory.py"]
        job = make_job(
            owner_agent=owner,
            business_goal=f"20-sector portfolio execution: {owner}",
            economic_reason="Increase verified market coverage and execution readiness without multiplying company machinery.",
            job_class=job_class,
            authority_level="L4" if owner == "dealix-engineer" else "L3",
            priority=priority,
            urgency="high" if priority >= 93 else "normal",
            base_sha=base,
            modifying=True,
            executor={"prompt": _artifact_prompt(owner, target, sector_summary, work)},
            acceptance={"criteria": f"portfolio receipt exists: {target}", "checks": [{"kind": "file_exists", "path": target}]},
            tests=tests,
            files_in_scope=scope,
            context_refs=["dealix/commercial/sector_commercial_factory.py", "dealix/commercial/economic_cell.py"],
        )
        jobs.append(job)
    return jobs


def build_plan(base_sha: str | None = None) -> dict[str, Any]:
    factory = SectorCommercialFactory()
    coverage = factory.coverage_receipt()
    jobs = build_jobs(base_sha)
    return {
        "schema": "dealix.sector_portfolio_wave.v1",
        "coverage": coverage,
        "permanent_agents": [job["OWNER_AGENT"] for job in jobs],
        "job_count": len(jobs),
        "first_tick_intent": ["dealix-sales", "dealix-engineer", "dealix-delivery"],
        "followup_intent": ["dealix-pm", "dealix-content"],
        "deep_wip_max": 3,
        "jobs": jobs,
        "truth": {
            "research_is_relationship": False,
            "research_is_pipeline": False,
            "research_is_revenue": False,
            "external_action_authority": False,
        },
    }


def enqueue_plan(plan: dict[str, Any], root: Path) -> dict[str, Any]:
    submitted = [submit_job(root, job) for job in plan["jobs"]]
    return {
        "submitted": sum(bool(item.get("ok")) for item in submitted),
        "waiting_l5": sum(item.get("job", {}).get("STATUS") == "WAITING_L5" for item in submitted),
        "statuses": [item.get("job", {}).get("STATUS") for item in submitted],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-sha", default=None)
    parser.add_argument("--state-dir", type=Path, default=None)
    parser.add_argument("--enqueue", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    plan = build_plan(args.base_sha)
    result: dict[str, Any] = {"plan": plan}
    if args.enqueue:
        result["enqueue"] = enqueue_plan(plan, state_root(args.state_dir))
    if args.summary:
        coverage = plan["coverage"]
        print(f"SECTORS={coverage['sectors_covered']}/{coverage['canonical_sectors']}")
        print(f"ALL_DIAGNOSTICS_FREE={coverage['all_diagnostics_free']}")
        print(f"JOBS={plan['job_count']} DEEP_WIP_MAX={plan['deep_wip_max']}")
        print("FIRST_TICK=sales,engineer,delivery")
        print("FOLLOWUP=pm,content")
        if args.enqueue:
            print(f"SUBMITTED={result['enqueue']['submitted']}")
            print(f"WAITING_L5={result['enqueue']['waiting_l5']}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
