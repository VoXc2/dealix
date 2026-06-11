"""Test that no scripts auto-send outreach without explicit review.

Usage:
    python3 -m pytest tests/test_no_auto_send.py
"""
from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATTERNS = [
    re.compile(r"send_email\s*\("),
    re.compile(r"send_whatsapp\s*\("),
    re.compile(r"send_sms\s*\("),
    re.compile(r"send_template\s*\("),
    re.compile(r"auto_send\s*=\s*True"),
    re.compile(r"auto_send\s*=\s*\"yes\""),
]

# Files where these terms may legitimately appear (docs, plans, allowlist)
ALLOWLIST_PREFIXES = (
    "docs/",
    "business/governance/",
    "business/sales-automation/",
    "business/sales-machine/HUMAN_REVIEW_POLICY.md",
    "scripts/check_no_secrets.py",
    "scripts/dealix_daily_operator.py",
    "scripts/generate_outreach_drafts.py",  # generates drafts only
    "scripts/approve_outreach_draft.py",
    "scripts/reject_outreach_draft.py",
    "tests/test_no_auto_send.py",
)

# Paths that should NEVER contain send() calls
SCAN_PATHS = [
    "scripts/import_leads_csv.py",
    "scripts/score_leads.py",
    "scripts/generate_prospect_pack.py",
    "scripts/generate_followup_queue.py",
    "scripts/generate_proposal.py",
    "scripts/generate_client_brief.py",
    "scripts/generate_delivery_plan.py",
    "scripts/generate_weekly_command_report.py",
    "scripts/generate_daily_ceo_brief.py",
    "scripts/generate_ultimate_sales_os_pack.py",
    "scripts/generate_sales_machine_pack.py",
    "scripts/dealix_v3_run_all.sh",
    "scripts/dealix_v4_run_all.sh",
    "scripts/dealix_v5_run_all.sh",
]


def test_no_auto_send() -> None:
    bad: list[str] = []
    for rel in SCAN_PATHS:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in FORBIDDEN_PATTERNS:
            for m in pat.finditer(text):
                bad.append(f"{rel}:{m.start()}  matched {pat.pattern}")
    assert not bad, "Found forbidden send patterns:\n" + "\n".join(bad)


if __name__ == "__main__":
    test_no_auto_send()
    print("test_no_auto_send passed")
