"""Generate a health snapshot.

Usage:
    python3 scripts/generate_health_snapshot.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "reports" / "health"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
QUEUE_PATH = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"
PROOF_PATH = REPO_ROOT / "business" / "_data" / "proof_vault.json"
AUDIT_DIR = REPO_ROOT / "reports" / "audit"
BACKUP_DIR = REPO_ROOT / "reports" / "backups"


def _read_json_count(p: Path, list_key: str | None) -> int:
    if not p.exists():
        return 0
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if list_key:
            return len(data.get(list_key, []))
        return len(data) if isinstance(data, list) else 0
    except json.JSONDecodeError:
        return -1


def main() -> int:
    today = dt.date.today().isoformat()
    accounts = _read_json_count(LEADS_PATH, "accounts")
    drafts = _read_json_count(QUEUE_PATH, "drafts")
    proof = _read_json_count(PROOF_PATH, "items")
    pending = 0
    if QUEUE_PATH.exists():
        try:
            drafts_list = json.loads(QUEUE_PATH.read_text(encoding="utf-8")).get("drafts", [])
            pending = sum(1 for d in drafts_list if d.get("reviewStatus") == "draft_pending_human_review")
        except json.JSONDecodeError:
            pass

    audit_files = list(AUDIT_DIR.glob("*.jsonl")) if AUDIT_DIR.exists() else []
    audit_total = sum(f.stat().st_size for f in audit_files)
    last_audit = max((f.name for f in audit_files), default="(none)")

    backup_zips = sorted(BACKUP_DIR.glob("dealix-business-data-*.zip")) if BACKUP_DIR.exists() else []
    last_backup = backup_zips[-1].name if backup_zips else "(none)"

    body = f"""# Health Snapshot — {today}

## Counts
- Accounts in CRM: {accounts}
- Drafts total: {drafts}
- Drafts pending review: {pending}
- Proof items logged: {proof}

## Audit
- Total size: {audit_total} bytes
- Last file: {last_audit}

## Backup
- Last zip: {last_backup}

## Status
"""
    body += "- OK\n" if pending == 0 else f"- WARN: {pending} drafts pending review\n"
    body += "- OK (audit running)\n" if audit_total > 0 else "- INFO: no audit logs yet\n"
    body += "- OK (backups found)\n" if backup_zips else "- INFO: no manual backups yet\n"

    out = OUT_DIR / f"health-snapshot-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
