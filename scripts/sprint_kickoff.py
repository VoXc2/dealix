#!/usr/bin/env python3
"""Sprint Kickoff — the founder's pre-flight before sending Invoice #1.

Walks the 8-action cascade from docs/ops/FIRST_INVOICE_UNLOCK.md and
produces a signed scope JSON the founder can review with the buyer
before invoicing.

The 8 actions:
  1. Register Capital Asset first.
  2. Generate or queue Trust Pack.
  3. Confirm buyer, scope, and owner.
  4. Confirm exclusions (no scraping / no cold WA / no LI auto / no
     guaranteed sales / no external action without approval).
  5. Confirm data boundary and Source Passport requirement.
  6. Send invoice.   ← THIS SCRIPT STOPS BEFORE THIS STEP.
  7. Activate sprint or retainer scheduler.
  8. Record proof target and value ledger expectation.

This script produces the scope JSON for steps 1-5 + 8 (proof target).
Step 6 (sending the invoice) is a deliberate human action, performed
afterwards via scripts/log_invoice_event.py.

Usage:
    python scripts/sprint_kickoff.py \\
        --buyer "Saudi B2B services client X" \\
        --scope "Revenue Intelligence Sprint" \\
        --proof-target "1 Proof Pack + 1 Value Ledger entry" \\
        --owner "Sami" \\
        --capital-asset-id <existing-asset-id>

If --capital-asset-id is omitted, the script suggests running
scripts/register_capital_asset.py first.

Output:
    data/_state/sprints/sprint_<id>.json   (signed scope)
    data/_state/sprints/sprint_<id>.md     (founder/buyer review doc)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SPRINT_DIR = REPO_ROOT / "data" / "_state" / "sprints"
CAPITAL_INDEX = REPO_ROOT / "data" / "capital_asset_index.json"


EXCLUSIONS_STANDARD = [
    "No scraping of third-party surfaces.",
    "No cold WhatsApp automation. WhatsApp use is human-initiated only.",
    "No LinkedIn automation. Messages are human-initiated only.",
    "No guaranteed sales / revenue claims.",
    "No external action without recorded human approval.",
    "No source-less AI runs. Source Passport required for every dataset.",
]


def _git_author() -> str:
    try:
        out = subprocess.run(
            ["git", "config", "user.email"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _capital_asset_exists(asset_id: str) -> bool:
    if not CAPITAL_INDEX.exists():
        return False
    try:
        data = json.loads(CAPITAL_INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return any(str(e.get("entry_id")) == asset_id for e in (data.get("entries") or []))


def build_scope(
    buyer: str,
    scope: str,
    proof_target: str,
    owner: str,
    capital_asset_id: str | None,
    data_boundary: str,
    governance_boundary: str,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    sprint_id = uuid.uuid4().hex[:12]

    capital_asset_status = "missing"
    if capital_asset_id:
        if _capital_asset_exists(capital_asset_id):
            capital_asset_status = "registered"
        else:
            capital_asset_status = "id-provided-but-not-found"

    return {
        "sprint_id": sprint_id,
        "generated_at": now,
        "owner": owner.strip(),
        "buyer": buyer.strip(),
        "scope": scope.strip(),
        "proof_target": proof_target.strip(),
        "capital_asset_id": capital_asset_id or "",
        "capital_asset_status": capital_asset_status,
        "data_boundary": data_boundary.strip(),
        "governance_boundary": governance_boundary.strip(),
        "exclusions": EXCLUSIONS_STANDARD,
        "doctrine_anchors": {
            "source_passport_required": True,
            "human_approval_required_for_external_action": True,
            "proof_pack_required_before_claims": True,
            "capital_asset_registered_before_invoice": True,
            "no_celebration_rule_until_proof_delivered": True,
        },
        "next_action": (
            "Review with buyer. When buyer accepts scope, run "
            "scripts/log_invoice_event.py to record Invoice #1."
        ),
        "runbook": "docs/ops/FIRST_INVOICE_UNLOCK.md",
        "git_author": _git_author(),
    }


def _render_md(scope_doc: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Sprint Kickoff — `{scope_doc['sprint_id']}`")
    lines.append("")
    lines.append(f"_Buyer:_ **{scope_doc['buyer']}**  ")
    lines.append(f"_Scope:_ **{scope_doc['scope']}**  ")
    lines.append(f"_Owner:_ **{scope_doc['owner']}**  ")
    lines.append(f"_Generated:_ {scope_doc['generated_at']}")
    lines.append("")
    lines.append("## Proof Target")
    lines.append(f"> {scope_doc['proof_target']}")
    lines.append("")
    lines.append("## Capital Asset")
    if scope_doc["capital_asset_status"] == "registered":
        lines.append(f"- Registered. `entry_id = {scope_doc['capital_asset_id']}`")
    elif scope_doc["capital_asset_status"] == "id-provided-but-not-found":
        lines.append(f"- ⚠ Provided `{scope_doc['capital_asset_id']}` was NOT found in")
        lines.append("  `data/capital_asset_index.json`. Register first via:")
        lines.append("  `python scripts/register_capital_asset.py ...`")
    else:
        lines.append("- ⚠ Not registered yet. Run before invoicing:")
        lines.append("  `python scripts/register_capital_asset.py ...`")
    lines.append("")
    lines.append("## Data Boundary")
    lines.append(f"- {scope_doc['data_boundary']}")
    lines.append("")
    lines.append("## Governance Boundary")
    lines.append(f"- {scope_doc['governance_boundary']}")
    lines.append("")
    lines.append("## Exclusions (Buyer Confirms)")
    for x in scope_doc["exclusions"]:
        lines.append(f"- [ ] {x}")
    lines.append("")
    lines.append("## Doctrine Anchors")
    for k, v in scope_doc["doctrine_anchors"].items():
        lines.append(f"- `{k}` = `{v}`")
    lines.append("")
    lines.append("## Next Action")
    lines.append(f"> {scope_doc['next_action']}")
    lines.append("")
    lines.append("---")
    lines.append(f"_Runbook:_ `{scope_doc['runbook']}`  ")
    lines.append(f"_Recorded by:_ `{scope_doc['git_author']}`")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sprint kickoff — produce a signed scope before Invoice #1.",
    )
    parser.add_argument("--buyer", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--proof-target", required=True)
    parser.add_argument("--owner", default="Founder")
    parser.add_argument("--capital-asset-id", default=None)
    parser.add_argument(
        "--data-boundary",
        default=(
            "Client-owned and client-introduced data only. No third-party "
            "scraping. Source Passport required for every dataset."
        ),
    )
    parser.add_argument(
        "--governance-boundary",
        default=(
            "All outputs pass through Governance Runtime. No external action "
            "without recorded human approval."
        ),
    )
    args = parser.parse_args(argv)

    SPRINT_DIR.mkdir(parents=True, exist_ok=True)
    scope_doc = build_scope(
        buyer=args.buyer,
        scope=args.scope,
        proof_target=args.proof_target,
        owner=args.owner,
        capital_asset_id=args.capital_asset_id,
        data_boundary=args.data_boundary,
        governance_boundary=args.governance_boundary,
    )

    json_path = SPRINT_DIR / f"sprint_{scope_doc['sprint_id']}.json"
    md_path = SPRINT_DIR / f"sprint_{scope_doc['sprint_id']}.md"
    json_path.write_text(
        json.dumps(scope_doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_render_md(scope_doc), encoding="utf-8")

    print(f"sprint kickoff: {scope_doc['sprint_id']}")
    print(f"  buyer:   {scope_doc['buyer']}")
    print(f"  scope:   {scope_doc['scope']}")
    print(f"  capital_asset: {scope_doc['capital_asset_status']}")
    print(f"  next:    review with buyer, then log_invoice_event.py")
    print(f"  wrote:   {md_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
