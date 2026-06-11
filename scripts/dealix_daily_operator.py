"""Dealix daily operator — runs the full daily commercial sequence.

Usage:
    python3 scripts/dealix_daily_operator.py --mode demo
    python3 scripts/dealix_daily_operator.py --mode production --leads data/imports/leads.csv
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_step(label: str, fn) -> bool:
    print(f"[{dt.datetime.now().isoformat(timespec='seconds')}] {label}")
    try:
        fn()
        print("  OK")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  FAIL: {exc}")
        return False


def cmd_score():
    sys.path.insert(0, str(REPO_ROOT))
    import subprocess
    subprocess.check_call([sys.executable, str(REPO_ROOT / "scripts" / "score_leads.py")])


def cmd_drafts():
    import subprocess
    import sys as _s
    _s.path.insert(0, str(REPO_ROOT))
    subprocess.check_call(
        [
            _s.executable,
            str(REPO_ROOT / "scripts" / "generate_outreach_drafts.py"),
            "--top", "10",
            "--language", "both",
            "--channel", "whatsapp",
        ]
    )


def cmd_followups():
    import subprocess
    import sys as _s
    _s.path.insert(0, str(REPO_ROOT))
    subprocess.check_call([_s.executable, str(REPO_ROOT / "scripts" / "generate_followup_queue.py")])


def cmd_prospect_pack():
    import subprocess
    import sys as _s
    _s.path.insert(0, str(REPO_ROOT))
    subprocess.check_call([_s.executable, str(REPO_ROOT / "scripts" / "generate_prospect_pack.py")])


def cmd_proposal():
    import subprocess
    import sys as _s
    _s.path.insert(0, str(REPO_ROOT))
    subprocess.check_call(
        [
            _s.executable,
            str(REPO_ROOT / "scripts" / "generate_proposal.py"),
            "--account-id", "demo-acc-003",
            "--offer", "Command Center",
            "--lang", "both",
            "--timeline", "21 days",
        ]
    )


def cmd_ceo_brief():
    import subprocess
    import sys as _s
    _s.path.insert(0, str(REPO_ROOT))
    subprocess.check_call([_s.executable, str(REPO_ROOT / "scripts" / "generate_daily_ceo_brief.py")])


def cmd_pipeline_report():
    out = REPO_ROOT / "business" / "crm" / "exports" / f"dealix-pipeline-report-{dt.date.today().isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    leads_path = REPO_ROOT / "business" / "_data" / "leads.json"
    accounts = []
    if leads_path.exists():
        try:
            accounts = json.loads(leads_path.read_text(encoding="utf-8")).get("accounts", [])
        except json.JSONDecodeError:
            accounts = []
    if not accounts:
        # Use seed if exists
        seed = REPO_ROOT / "business" / "crm" / "prospects.seed.json"
        if seed.exists():
            accounts = json.loads(seed.read_text(encoding="utf-8")).get("accounts", [])

    lines: list[str] = []
    lines.append(f"# Dealix Pipeline Report — {dt.date.today().isoformat()}")
    lines.append("")
    lines.append(f"Total accounts: {len(accounts)}")
    by_stage: dict[str, int] = {}
    for a in accounts:
        by_stage[a.get("stage", "unknown")] = by_stage.get(a.get("stage", "unknown"), 0) + 1
    lines.append("")
    lines.append("## By stage")
    for k, v in by_stage.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("---")
    lines.append("Demo mode: no auto-send, no claims of traction.")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {out}")


def bootstrap_leads():
    """If leads.json is missing, seed it from prospects.seed.json (demo mode)."""
    leads_path = REPO_ROOT / "business" / "_data" / "leads.json"
    if leads_path.exists():
        return
    seed = REPO_ROOT / "business" / "crm" / "prospects.seed.json"
    if not seed.exists():
        return
    leads_path.parent.mkdir(parents=True, exist_ok=True)
    leads_path.write_text(seed.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"  bootstrapped {leads_path} from {seed}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--leads", help="Path to leads CSV (production only)")
    args = parser.parse_args()

    print(f"Dealix Daily Operator — mode={args.mode}")
    bootstrap_leads()
    steps = [
        ("1. Score leads", cmd_score),
        ("2. Generate drafts", cmd_drafts),
        ("3. Generate follow-ups", cmd_followups),
        ("4. Generate prospect pack", cmd_prospect_pack),
        ("5. Generate proposal (demo account)", cmd_proposal),
        ("6. Generate daily CEO brief", cmd_ceo_brief),
        ("7. Generate pipeline report", cmd_pipeline_report),
    ]
    ok = 0
    for label, fn in steps:
        if run_step(label, fn):
            ok += 1
    print(f"\n{ok}/{len(steps)} steps OK")

    summary = REPO_ROOT / "reports" / "operator" / f"dealix-daily-operator-{dt.date.today().isoformat()}.md"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        f"""# Dealix Daily Operator Summary — {dt.date.today().isoformat()}

**Mode:** {args.mode}
**Steps passed:** {ok}/{len(steps)}

## Files generated
- `business/_data/scored_leads.json`
- `business/_data/outreach_review_queue.json`
- `business/crm/exports/dealix-followup-queue.md`
- `business/crm/exports/dealix-daily-prospect-pack.md`
- `business/crm/exports/dealix-pipeline-report-{dt.date.today().isoformat()}.md`
- `business/proposals/generated/...`
- `business/reports/exports/dealix-daily-ceo-brief-{dt.date.today().isoformat()}.txt`

## Safety reminder
- No draft was sent.
- All drafts have `reviewStatus = "draft_pending_human_review"`.
- Founder must run `approve_outreach_draft.py` before any send.
""",
        encoding="utf-8",
    )
    print(f"Wrote summary: {summary}")
    return 0 if ok == len(steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
