#!/usr/bin/env python3
"""Dealix command-line control surface.

Commands:
  factory-run     --dry-run            simulate the daily revenue loop (no external sends)
  account-packs   --limit N --dry-run  preview the nightly account packs
  quality-check                        run email + proposal + delivery quality gates
  launch-score    [--min N]            compute the weighted Launch Score + scorecard
  founder-command [--dry-run]          print today's founder super-command
  delivery-status                      print delivery pipeline status
  security-check                       run the security + privacy gates

Every command is read-only and never contacts an external service. Outreach,
proposals and contact actions always require explicit human approval.
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "scripts", "checks"))

from _common import load_jsonl, run_check  # noqa: E402


def _run_checks(names: list[str]) -> int:
    rc = 0
    for name in names:
        mod = importlib.import_module(name)
        rc |= run_check(mod.check())
    return rc


def cmd_launch_score(args) -> int:
    if args.min is not None:
        os.environ["LAUNCH_MIN"] = str(args.min)
    sc_mod = importlib.import_module("check_ready_to_launch_scorecard")
    sc = sc_mod.compute_scorecard()
    print(f"Launch Score: {sc['score']}/100")
    print(f"  Soft Launch Ready (>=75): {sc['soft_launch_ready']}")
    print(f"  Full Launch Ready (>=90): {sc['full_launch_ready']}")
    for row in sc["rows"]:
        flag = "PASS" if row["passed"] else "FAIL"
        print(f"  [{flag}] {row['label']} ({row['weight']})")
    return run_check(sc_mod.check())


def cmd_quality_check(_args) -> int:
    return _run_checks(["check_email_quality_gate", "check_proposal_gate", "check_delivery_gate"])


def cmd_security_check(_args) -> int:
    return _run_checks(["check_security_privacy_gates"])


def cmd_delivery_status(_args) -> int:
    pipelines = load_jsonl("data/delivery/pipelines.jsonl")
    print(f"Delivery pipelines: {len(pipelines)}")
    for p in pipelines:
        ok = "ready" if p.get("required_inputs_satisfied") else "BLOCKED(no inputs)"
        print(f"  {p['pipeline_id']:>8}  {p['status']:<8} {ok:<18} {p['owner']:<14} {p['client']} — {p['system']}")
    blocked = [p for p in pipelines if not p.get("required_inputs_satisfied")]
    print(f"Blocked (missing inputs): {len(blocked)}")
    return 0


def cmd_account_packs(args) -> int:
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    limit = args.limit or len(packs)
    mode = "DRY-RUN (no external sends)" if args.dry_run else "preview"
    print(f"Account packs: {len(packs)} available — showing top {min(limit, len(packs))} [{mode}]")
    for i, p in enumerate(packs[:limit], 1):
        print(f"  {i:>3}. {p['company_name']} | {p['sector']} | need={p['primary_need']} "
              f"| sys={p['recommended_core_system']} | final={p['final_account_score']} "
              f"| contact={p['contact_confidence']}")
    if args.limit and args.limit >= 400:
        print("Note: production target is 400 packs/night; sample dataset is smaller.")
    return 0


def cmd_factory_run(args) -> int:
    if not args.dry_run:
        print("Refusing to run the factory without --dry-run (no live sends are wired). "
              "Re-run with --dry-run.")
        return 2
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    drafts = load_jsonl("data/outreach/email_drafts.jsonl")
    queue = load_jsonl("data/outreach/top_100_approval_queue.jsonl")
    proposals = load_jsonl("data/proposals/mini_proposals.jsonl")
    print("Dealix factory run — DRY RUN (no external service is contacted)")
    print(f"  1. Account packs prepared : {len(packs)}")
    print(f"  2. System drafts produced : {len(drafts)} (one system each, approval required)")
    print(f"  3. Top approval queue     : {len(queue)}")
    print(f"  4. Mini proposals staged  : {len(proposals)} (status=draft, approval required)")
    print("  5. Sends                  : 0 (all outreach awaits human approval)")
    print("Quality gates:")
    return cmd_quality_check(args)


def cmd_founder_command(args) -> int:
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    top = packs[:5]
    when = "DRY-RUN" if args.dry_run else "today"
    print(f"Founder Super-Command ({when}) — top 5 accounts:")
    for i, p in enumerate(top, 1):
        print(f"  {i}. {p['company_name']} | {p['sector']} | {p['primary_need']} -> {p['next_action']}")
    print("Top 3 decisions:")
    print("  1) اعتمد مسودات أعلى 100")
    print("  2) اعتمد العروض المعلّقة")
    print("  3) راجع بوابات التسليم")
    print("See reports/founder/DAILY_SUPER_COMMAND.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix", description="Dealix launch control surface")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("factory-run"); p.add_argument("--dry-run", action="store_true"); p.set_defaults(func=cmd_factory_run)
    p = sub.add_parser("account-packs"); p.add_argument("--limit", type=int, default=None); p.add_argument("--dry-run", action="store_true"); p.set_defaults(func=cmd_account_packs)
    p = sub.add_parser("quality-check"); p.set_defaults(func=cmd_quality_check)
    p = sub.add_parser("launch-score"); p.add_argument("--min", type=int, default=None); p.set_defaults(func=cmd_launch_score)
    p = sub.add_parser("founder-command"); p.add_argument("--dry-run", action="store_true"); p.set_defaults(func=cmd_founder_command)
    p = sub.add_parser("delivery-status"); p.set_defaults(func=cmd_delivery_status)
    p = sub.add_parser("security-check"); p.set_defaults(func=cmd_security_check)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
