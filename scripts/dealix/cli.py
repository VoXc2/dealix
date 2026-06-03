"""Dealix factory CLI. Invoked via the root launcher: `python dealix.py <cmd>`.

Commands:
  seed                          regenerate all schemas + data + site catalog + reports
  factory-run    [--dry-run]    run the full pipeline (summary; --dry-run writes nothing)
  account-packs  --limit N [--dry-run]
  quality-check                 run email/proposal/delivery quality gates
  security-check                run security + privacy gates
  delivery-status               print delivery pipeline status
  founder-command [--dry-run]   generate the founder daily super command
  launch-score                  compute + write the Ready-to-Launch scorecard
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import (
    build_schemas,
    generate_account_packs,
    generate_business_os_catalog,
    generate_call_briefs,
    generate_contacts,
    generate_delivery,
    generate_docs,
    generate_email_drafts,
    generate_founder_command,
    generate_mini_proposals,
    generate_need_intelligence,
    generate_site_catalog,
    seeds,
)
from .lib import ROOT, load_jsonl, write_text


# ---------------------------------------------------------------- full pipeline
def seed_all(limit=400, dry_run=False):
    """Generate the entire data layer from seeds, in dependency order."""
    build_schemas.main()
    generate_business_os_catalog.main()
    generate_need_intelligence.main()
    generate_site_catalog.main()
    generate_account_packs.build(limit, dry_run=dry_run)
    if not dry_run:
        generate_contacts.build(limit=limit)
        generate_email_drafts.build(limit=limit)
        generate_call_briefs.build()
        generate_mini_proposals.build()
        generate_delivery.build()
        generate_founder_command.build()
        generate_docs.build()
        write_scorecard()


def cmd_seed(args):
    seed_all(limit=args.limit)
    print("\nSeed complete. Run `python dealix.py launch-score` to grade readiness.")
    return 0


def cmd_factory_run(args):
    print(f"== Dealix factory-run (dry_run={args.dry_run}) ==")
    if args.dry_run:
        # Re-derive in memory without writing anything.
        build_schemas.main()
        generate_business_os_catalog.build()
        generate_need_intelligence.build()
        packs, _ = generate_account_packs.build(args.limit, dry_run=True)
        print(f"factory-run dry: would produce {len(packs)} packs and downstream drafts/briefs/proposals.")
        return 0
    seed_all(limit=args.limit)
    return 0


def cmd_account_packs(args):
    return generate_account_packs.main(
        ["--limit", str(args.limit)] + (["--dry-run"] if args.dry_run else [])
    )


def cmd_founder_command(args):
    return generate_founder_command.main(["--dry-run"] if args.dry_run else [])


def _run_check(module_rel):
    """Run a check script as a subprocess; return (ok, output)."""
    path = ROOT / module_rel
    if not path.exists():
        return False, f"missing check: {module_rel}"
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout + proc.stderr


def cmd_quality_check(args):
    checks = [
        "scripts/checks/check_email_quality_gate.py",
        "scripts/checks/check_proposal_gate.py",
        "scripts/checks/check_delivery_gate.py",
    ]
    failed = 0
    for c in checks:
        ok, out = _run_check(c)
        print(out.rstrip())
        if not ok:
            failed += 1
    print(f"\nquality-check: {len(checks) - failed}/{len(checks)} gates passed.")
    return 1 if failed else 0


def cmd_security_check(args):
    ok, out = _run_check("scripts/checks/check_security_privacy_gates.py")
    print(out.rstrip())
    return 0 if ok else 1


def cmd_delivery_status(args):
    path = ROOT / "data/delivery/pipelines.jsonl"
    if not path.exists():
        print("No delivery pipelines yet. Run `python dealix.py seed` first.")
        return 0
    pipelines = load_jsonl("data/delivery/pipelines.jsonl")
    print(f"Delivery pipelines: {len(pipelines)}")
    for p in pipelines:
        blocked = "" if p.get("inputs_received") else "  [BLOCKED: awaiting client inputs]"
        print(f"  - {p['client']} | {p['selected_system']} | stage={p['stage']}{blocked}")
    return 0


# ------------------------------------------------------------------ launch score
DOMAIN_WEIGHTS = [
    ("Website routes", 10, ["data/site/site_routes.yaml", "src/marketing/catalog.ts"]),
    ("Core systems", 10, ["docs/commercial/FOCUS_5_SYSTEMS_MARKET_ENTRY_AR.md"]),
    ("Business OS Catalog", 10, ["data/business_os_catalog/systems.yaml"]),
    ("Business Need Intelligence", 15, [
        "data/business_need_intelligence/need_taxonomy_25.yaml",
        "data/business_need_intelligence/specialized_sprint_library_50.yaml",
        "data/business_need_intelligence/sector_need_matrix_20.yaml",
    ]),
    ("Account Packs", 15, ["data/account_intelligence/account_packs.jsonl"]),
    ("Contact Discovery", 8, ["data/contacts/contact_discovery.jsonl"]),
    ("Email/Call/Proposal", 10, [
        "data/outreach/email_drafts.jsonl",
        "data/acquisition/call_briefs.jsonl",
        "data/proposals/mini_proposals.jsonl",
    ]),
    ("Delivery Automation", 10, ["data/delivery/pipelines.jsonl"]),
    ("Finance/Metrics", 5, ["data/finance/cash_priority_scores.jsonl"]),
    ("Security/Privacy", 7, [
        "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY.md",
        "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
    ]),
]


def compute_launch_score():
    rows, total = [], 0.0
    for name, weight, files in DOMAIN_WEIGHTS:
        present = sum(1 for f in files if (ROOT / f).exists())
        earned = round(weight * present / len(files), 1)
        total += earned
        rows.append((name, earned, weight, present, len(files)))
    return rows, round(total, 1)


def band(score):
    if score >= 90:
        return "Launch Ready"
    if score >= 75:
        return "Soft Launch Ready"
    if score >= 60:
        return "Internal Dry Run"
    return "Not Ready"


def write_scorecard():
    rows, total = compute_launch_score()
    lines = ["# Dealix — Ready-to-Launch Scorecard", "", f"Score: **{total} / 100** → **{band(total)}**", ""]
    lines.append("| المجال | المحقق | الوزن | الملفات |")
    lines.append("| --- | ---: | ---: | --- |")
    for name, earned, weight, present, n in rows:
        lines.append(f"| {name} | {earned} | {weight} | {present}/{n} |")
    lines += ["", "## Bands", "- 90–100 = Launch Ready", "- 75–89 = Soft Launch Ready",
              "- 60–74 = Internal Dry Run", "- <60 = Not Ready", ""]
    text = "\n".join(lines) + "\n"
    write_text("reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md", text)
    return text, total


def cmd_launch_score(args):
    text, total = write_scorecard()
    print(text)
    print("Wrote reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md")
    return 0


# ------------------------------------------------------------------------ parser
def build_parser():
    p = argparse.ArgumentParser(prog="dealix", description="Dealix Revenue Factory CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("seed"); s.add_argument("--limit", type=int, default=400); s.set_defaults(func=cmd_seed)
    s = sub.add_parser("factory-run"); s.add_argument("--limit", type=int, default=400); s.add_argument("--dry-run", action="store_true"); s.set_defaults(func=cmd_factory_run)
    s = sub.add_parser("account-packs"); s.add_argument("--limit", type=int, default=400); s.add_argument("--dry-run", action="store_true"); s.set_defaults(func=cmd_account_packs)
    s = sub.add_parser("quality-check"); s.set_defaults(func=cmd_quality_check)
    s = sub.add_parser("security-check"); s.set_defaults(func=cmd_security_check)
    s = sub.add_parser("delivery-status"); s.set_defaults(func=cmd_delivery_status)
    s = sub.add_parser("founder-command"); s.add_argument("--dry-run", action="store_true"); s.set_defaults(func=cmd_founder_command)
    s = sub.add_parser("launch-score"); s.set_defaults(func=cmd_launch_score)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)
