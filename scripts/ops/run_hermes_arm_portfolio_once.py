#!/usr/bin/env python3
"""ONE-SHOT Hermes arm portfolio runner.

Runs the controller exactly once: plan -> write plan -> (optional) enqueue safe
jobs into the canonical session factory queue. It never loops, never installs a
cron/systemd unit, and never executes a job itself — the single canonical
scheduler (``scripts/ops/session_factory.py`` + its watchdog) remains the only
runner. L5 material effects stay ``WAITING_L5``.

Usage:
    python3 scripts/ops/run_hermes_arm_portfolio_once.py
    python3 scripts/ops/run_hermes_arm_portfolio_once.py --enqueue
    python3 scripts/ops/run_hermes_arm_portfolio_once.py --evidence data/ops/x.json --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import hermes_arm_portfolio_controller as controller

DEFAULT_STATE_DIR = controller.session_factory().STATE_DIR
PLAN_FILENAME = "HERMES_ARM_PORTFOLIO_PLAN.json"


def run_once(
    *,
    evidence_path: Path | None = None,
    plan_path: Path | None = None,
    state_dir: Path | None = None,
    enqueue: bool = False,
    max_jobs: int = 5,
    repo_root: Path | None = None,
    generated_at: str | None = None,
) -> dict:
    """One planning pass plus optional enqueue into the canonical queue."""
    state_dir = Path(state_dir or DEFAULT_STATE_DIR)
    registry = controller.load_registry()
    playbooks = controller.load_playbooks()
    allowed_ids = {
        str(arm.get("id")) for arm in (registry.get("arms") or []) if isinstance(arm, dict)
    }
    evidence = controller.load_evidence(evidence_path, allowed_ids=allowed_ids)
    plan = controller.plan_portfolio(
        registry=registry,
        playbooks=playbooks,
        evidence=evidence,
        evidence_path=evidence_path,
        generated_at=generated_at,
    )
    target = Path(plan_path) if plan_path else state_dir / PLAN_FILENAME
    controller.write_plan(plan, target)

    result: dict = {
        "plan_path": str(target),
        "overall": plan.get("overall"),
        "counts": plan.get("counts"),
        "top3": plan.get("top3"),
        "deep_wedge_ids": plan.get("deep_wedge_ids"),
        "enqueued": [],
        "skipped": [],
        "scheduler": "canonical:scripts/ops/session_factory.py",
        "external_effect": controller.EXTERNAL_EFFECT,
        "l5_policy": controller.L5_POLICY,
    }
    if not enqueue:
        return result
    if plan.get("overall") != "PLAN_READY":
        result["enqueue_error"] = f"refused:{plan.get('overall')}"
        return result

    factory = controller.session_factory()
    root = Path(state_dir)
    for record in plan.get("records") or []:
        if len(result["enqueued"]) >= max_jobs:
            result["skipped"].append({"arm_id": record["arm_id"], "reason": "MAX_JOBS"})
            continue
        job_class = record["model_job_class"]
        if not job_class["auto_executable"] and not record["l5_required"]:
            result["skipped"].append(
                {"arm_id": record["arm_id"], "reason": record["classification"]}
            )
            continue
        marker = f"arm_portfolio:{record['arm_id']}"
        if controller.already_enqueued(root, marker):
            result["skipped"].append({"arm_id": record["arm_id"], "reason": "ALREADY_ENQUEUED"})
            continue
        job = controller.build_job(record, repo_root=repo_root)
        submitted = factory.submit_job(root, job)
        result["enqueued"].append(
            {
                "arm_id": record["arm_id"],
                "job_id": job["JOB_ID"],
                "status": submitted.get("job", {}).get("STATUS"),
                "authority_level": record["model_job_class"]["authority_level"],
            }
        )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One-shot Hermes arm portfolio runner")
    parser.add_argument("--evidence", type=Path, default=None)
    parser.add_argument("--plan-out", type=Path, default=None)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    parser.add_argument(
        "--enqueue", action="store_true", help="submit safe jobs to the canonical queue"
    )
    parser.add_argument("--max-jobs", type=int, default=5)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--summary", action="store_true", help="print the compact human summary")
    parser.add_argument("--json", action="store_true", help="print the runner result as JSON")
    args = parser.parse_args(argv)

    result = run_once(
        evidence_path=args.evidence,
        plan_path=args.plan_out,
        state_dir=args.state_dir,
        enqueue=args.enqueue,
        max_jobs=args.max_jobs,
        repo_root=args.repo_root,
    )
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        plan = controller.read_json(Path(result["plan_path"]), {})
        print(controller.render_summary(plan))
        print(f"PLAN_PATH={result['plan_path']}")
        print(f"ENQUEUED={len(result['enqueued'])} SKIPPED={len(result['skipped'])}")
        for item in result["enqueued"]:
            print(
                f"  JOB {item['arm_id']} {item['job_id']} {item['status']} authority={item['authority_level']}"
            )
    if result.get("enqueue_error"):
        return 2
    if result["overall"] == "BLOCKED":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
