"""Generate an ops health report.

Usage:
    python3 scripts/generate_ops_health_report.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "reports" / "ops"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    leads_path = REPO_ROOT / "business" / "_data" / "leads.json"
    queue_path = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"
    proof_path = REPO_ROOT / "business" / "_data" / "proof_vault.json"

    accounts = 0
    if leads_path.exists():
        try:
            accounts = len(json.loads(leads_path.read_text(encoding="utf-8")).get("accounts", []))
        except json.JSONDecodeError:
            pass
    pending = 0
    if queue_path.exists():
        try:
            drafts = json.loads(queue_path.read_text(encoding="utf-8")).get("drafts", [])
            pending = sum(1 for d in drafts if d.get("reviewStatus") == "draft_pending_human_review")
        except json.JSONDecodeError:
            pass
    proof = 0
    if proof_path.exists():
        try:
            proof = len(json.loads(proof_path.read_text(encoding="utf-8")).get("items", []))
        except json.JSONDecodeError:
            pass

    body = f"""# Ops Health Report — {today}

- Accounts in CRM: {accounts}
- Drafts pending review: {pending}
- Proof items logged: {proof}

## Health
"""
    body += "- OK" if pending == 0 else "- WARN: review queue has pending drafts"
    body += "\n\n---\n*Draft only.*\n"

    out = EXPORT_DIR / f"ops-health-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
