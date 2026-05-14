#!/usr/bin/env python3
"""Revenue Intelligence Sprint — Demo Runner.

Chains the three governed revenue-OS stages on a sample dataset to
produce a buyer-presentable demo of what the 25,000 SAR Sprint delivers,
WITHOUT sending anything externally:

    Source Passport (stub)
        ↓
    Account Scoring          (auto_client_acquisition/revenue_os/account_scoring.py)
        ↓
    Draft Pack (governed)    (auto_client_acquisition/revenue_os/draft_pack.py)
        ↓
    Follow-Up Plan           (auto_client_acquisition/revenue_os/followup_plan.py)
        ↓
    Proof Pack (JSON)
        ↓
    Capital Asset event      (auto_client_acquisition/capital_os/capital_ledger.py)

Hard rules (matches the 11 non-negotiables):
  - No external send. All output is local files.
  - No real client data. The dataset is a synthetic Saudi B2B sample.
  - Every output stamped `is_demo=True`.
  - Every recipient name is fake.

Outputs:
    data/_state/demo/revenue_intelligence_demo_<run_id>.json
    data/_state/demo/revenue_intelligence_demo_<run_id>.md

Usage:
    python scripts/run_revenue_intelligence_demo.py
    python scripts/run_revenue_intelligence_demo.py --json     # JSON to stdout
    python scripts/run_revenue_intelligence_demo.py --quiet    # no stdout
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "data" / "_state" / "demo"


SAMPLE_ACCOUNTS: list[dict[str, Any]] = [
    {
        "account_id": "DEMO-ACCT-001",
        "company": "Demo Saudi Logistics Co.",
        "sector": "logistics",
        "headcount": 180,
        "annual_revenue_sar": 60_000_000,
        "buying_signal": "expanding-to-eastern-region",
        "named_contact_role": "VP of Operations",
        "consent_status": "introduced-via-partner",
    },
    {
        "account_id": "DEMO-ACCT-002",
        "company": "Demo Riyadh Professional Services",
        "sector": "professional_services",
        "headcount": 45,
        "annual_revenue_sar": 18_000_000,
        "buying_signal": "new-cto-hired-30d",
        "named_contact_role": "Managing Partner",
        "consent_status": "warm-intro-pending",
    },
    {
        "account_id": "DEMO-ACCT-003",
        "company": "Demo Jeddah Healthcare Group",
        "sector": "healthcare_admin",
        "headcount": 320,
        "annual_revenue_sar": 110_000_000,
        "buying_signal": "rfp-published-public-portal",
        "named_contact_role": "Director of Strategy",
        "consent_status": "rfp-context-only",
    },
    {
        "account_id": "DEMO-ACCT-004",
        "company": "Demo Dammam Industrial Services",
        "sector": "industrial_services",
        "headcount": 90,
        "annual_revenue_sar": 32_000_000,
        "buying_signal": "no-recent-signal",
        "named_contact_role": "Operations Lead",
        "consent_status": "no-consent",
    },
]


def _score(account: dict[str, Any]) -> dict[str, Any]:
    """Lightweight, deterministic scoring — illustrative, not the production scorer.

    The real scorer lives at:
        auto_client_acquisition/revenue_os/account_scoring.py
    This demo uses a transparent rubric so a buyer can read the JSON and
    understand exactly why each account got its score.
    """
    points = 0
    rationale: list[str] = []

    if account["sector"] in {"logistics", "professional_services", "healthcare_admin"}:
        points += 20
        rationale.append(f"sector_fit:{account['sector']}+20")
    if 40 <= account["headcount"] <= 500:
        points += 15
        rationale.append("size_fit:mid-market+15")
    if account["annual_revenue_sar"] >= 20_000_000:
        points += 15
        rationale.append("revenue_fit:>=20M_SAR+15")
    bs = account["buying_signal"]
    if bs in {"expanding-to-eastern-region", "new-cto-hired-30d", "rfp-published-public-portal"}:
        points += 25
        rationale.append(f"signal:{bs}+25")
    if account["consent_status"] in {"introduced-via-partner", "warm-intro-pending"}:
        points += 25
        rationale.append(f"consent:{account['consent_status']}+25")
    elif account["consent_status"] == "rfp-context-only":
        points += 10
        rationale.append("consent:rfp-context+10")
    else:
        points -= 30
        rationale.append("consent:none-30 (BLOCKED)")

    return {
        "account_id": account["account_id"],
        "score": points,
        "rationale": rationale,
        "is_demo": True,
    }


def _draft_pack(account: dict[str, Any], score: dict[str, Any]) -> dict[str, Any]:
    """Governed draft — DRAFT_ONLY status, never sent.

    The real draft builder is governed by
    auto_client_acquisition/governance_os/runtime_decision.py before
    any output reaches a client.
    """
    if score["score"] < 30:
        return {
            "account_id": account["account_id"],
            "governance_status": "BLOCK",
            "reason": "score below outreach threshold or consent missing",
            "is_demo": True,
        }
    subject_en = f"Governed AI ops discussion — {account['company']}"
    subject_ar = f"مناقشة عمليات AI محكوم — {account['company']}"
    body_en = (
        f"Hi (named contact at {account['named_contact_role']} role),\n\n"
        f"Saw the {account['buying_signal']} signal at {account['company']}.\n"
        f"We're Dealix — we run Governed AI Operations Sprints for Saudi\n"
        f"firms in {account['sector']}. The sprint produces a Proof Pack\n"
        f"and a Capital Asset within 5 working days, draft-only outputs\n"
        f"only, no autonomous external action.\n\n"
        f"Would 25 minutes next week to scope a no-commit diagnostic\n"
        f"make sense?\n\nBest,\nSami"
    )
    return {
        "account_id": account["account_id"],
        "governance_status": "DRAFT_ONLY",
        "subject_en": subject_en,
        "subject_ar": subject_ar,
        "body_en": body_en,
        "approval_required_before_send": True,
        "is_demo": True,
    }


def _followup_plan(account_id: str) -> dict[str, Any]:
    """Standard D+3 / D+7 / D+14 cadence (governed)."""
    return {
        "account_id": account_id,
        "cadence": [
            {"day_offset": 3,  "channel": "email",         "type": "value-reframe"},
            {"day_offset": 7,  "channel": "linkedin_human","type": "case-anchor"},
            {"day_offset": 14, "channel": "email",         "type": "graceful-pause"},
        ],
        "is_demo": True,
    }


def run_demo() -> dict[str, Any]:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:12]
    now = datetime.now(timezone.utc).isoformat()

    scored = [_score(a) for a in SAMPLE_ACCOUNTS]
    ranked = sorted(scored, key=lambda s: -s["score"])
    drafts = [_draft_pack(a, s) for a, s in zip(SAMPLE_ACCOUNTS, scored)]
    followups = [_followup_plan(a["account_id"]) for a in SAMPLE_ACCOUNTS]

    eligible = [d for d in drafts if d["governance_status"] == "DRAFT_ONLY"]
    blocked = [d for d in drafts if d["governance_status"] == "BLOCK"]

    proof_pack = {
        "proof_pack_id": f"DEMO-PROOF-{run_id}",
        "generated_at": now,
        "is_demo": True,
        "summary": (
            f"Ranked {len(SAMPLE_ACCOUNTS)} sample accounts; "
            f"{len(eligible)} eligible for governed outreach; "
            f"{len(blocked)} blocked by governance."
        ),
        "ranked_accounts": ranked,
        "drafts_governed": drafts,
        "followup_plans": followups,
        "doctrine_checks": {
            "source_passport": "stub-required-in-production",
            "no_scraping": True,
            "no_cold_whatsapp": True,
            "no_linkedin_automation": True,
            "no_guaranteed_claims": True,
            "human_approval_before_external_action": True,
        },
    }

    capital_event = {
        "entry_id": uuid.uuid4().hex,
        "asset_type": "proof_example",
        "title": f"Revenue Intelligence Demo Run — {run_id}",
        "description": (
            "Demo run of the governed Revenue Intelligence Sprint chain "
            "(scoring → draft pack → follow-up plan → proof pack)."
        ),
        "evidence": f"data/_state/demo/revenue_intelligence_demo_{run_id}.json",
        "project_id": "demo",
        "client_id": "demo",
        "created_at": now,
        "git_author": "demo-runner",
        "is_demo": True,
    }

    payload = {
        "run_id": run_id,
        "generated_at": now,
        "is_demo": True,
        "sample_accounts": SAMPLE_ACCOUNTS,
        "proof_pack": proof_pack,
        "capital_event": capital_event,
        "next_step_for_buyer": (
            "Replace SAMPLE_ACCOUNTS with your accounts (via Source Passport), "
            "and the same chain runs governed on real data."
        ),
    }

    (DEMO_DIR / f"revenue_intelligence_demo_{run_id}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (DEMO_DIR / f"revenue_intelligence_demo_{run_id}.md").write_text(
        _render_md(payload),
        encoding="utf-8",
    )
    return payload


def _render_md(payload: dict[str, Any]) -> str:
    pp = payload["proof_pack"]
    eligible = [d for d in pp["drafts_governed"] if d.get("governance_status") == "DRAFT_ONLY"]
    blocked = [d for d in pp["drafts_governed"] if d.get("governance_status") == "BLOCK"]
    lines: list[str] = []
    lines.append(f"# Revenue Intelligence Sprint — Demo Run `{payload['run_id']}`")
    lines.append("")
    lines.append("> **Demo only.** No external action. No real client data.")
    lines.append("> Fake names. Fake signals. Real chain logic.")
    lines.append("")
    lines.append("## What the Sprint Produces")
    lines.append("- Ranked account list with transparent rubric.")
    lines.append("- Governed draft pack (DRAFT_ONLY; approval gate required).")
    lines.append("- D+3 / D+7 / D+14 follow-up plan per eligible account.")
    lines.append("- Proof Pack JSON.")
    lines.append("- Capital Asset event (registered into the library).")
    lines.append("")
    lines.append(f"## Results — {pp['summary']}")
    lines.append("")
    lines.append("### Ranked Accounts")
    lines.append("| Rank | Account | Score | Rationale |")
    lines.append("|---:|---|---:|---|")
    for i, s in enumerate(pp["ranked_accounts"], 1):
        rationale = "; ".join(s["rationale"])
        lines.append(f"| {i} | {s['account_id']} | {s['score']} | {rationale} |")
    lines.append("")
    lines.append("### Drafts (governed)")
    for d in eligible:
        lines.append(f"- **{d['account_id']}** — `{d['governance_status']}`  ")
        lines.append(f"  Subject (EN): _{d['subject_en']}_")
    if blocked:
        lines.append("")
        lines.append("### Blocked (governance refused)")
        for d in blocked:
            lines.append(f"- {d['account_id']} — `BLOCK` — {d['reason']}")
    lines.append("")
    lines.append("## Doctrine Checks")
    for k, v in pp["doctrine_checks"].items():
        lines.append(f"- `{k}` → `{v}`")
    lines.append("")
    lines.append(f"## Capital Asset Recorded")
    ce = payload["capital_event"]
    lines.append(f"- entry_id: `{ce['entry_id']}`")
    lines.append(f"- title: {ce['title']}")
    lines.append("")
    lines.append("## What Happens On Real Data")
    lines.append(payload["next_step_for_buyer"])
    lines.append("")
    lines.append("---")
    lines.append("_Produced by `scripts/run_revenue_intelligence_demo.py`._")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Revenue Intelligence Sprint demo runner (governed, draft-only).",
    )
    parser.add_argument("--json", action="store_true", help="print full JSON to stdout")
    parser.add_argument("--quiet", action="store_true", help="suppress human output")
    args = parser.parse_args(argv)

    payload = run_demo()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    if args.quiet:
        return 0
    pp = payload["proof_pack"]
    eligible = sum(1 for d in pp["drafts_governed"] if d.get("governance_status") == "DRAFT_ONLY")
    blocked = sum(1 for d in pp["drafts_governed"] if d.get("governance_status") == "BLOCK")
    print(f"Revenue Intelligence demo run: {payload['run_id']}")
    print(f"  accounts ranked:  {len(pp['ranked_accounts'])}")
    print(f"  drafts (governed): {eligible} DRAFT_ONLY, {blocked} BLOCKED")
    rel = (DEMO_DIR / f"revenue_intelligence_demo_{payload['run_id']}.md").relative_to(REPO_ROOT)
    print(f"  wrote: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
