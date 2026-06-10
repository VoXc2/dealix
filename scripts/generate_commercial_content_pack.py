#!/usr/bin/env python3
"""Weekly content pack — delegates to generate_weekly_content_drafts + exports markdown."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

DRAFTS_MD = REPO_ROOT / "docs/commercial/operations/drafts"
WEEKLY_DIR = REPO_ROOT / "var/content_drafts"

SOAEN = [
    "مصدر الفكرة موثّق",
    "مالك النشر محدد",
    "مراجعة قبل النشر (Approval)",
    "Truth Label لأي رقم",
    "CTA: Risk Score / Sample Proof / ديمو 10 دقائق",
]


def outreach_targets_md() -> str:
    lines = ["# Outreach targets · أعلى 10", ""]
    try:
        from dealix.revenue_ops_autopilot.store import get_autopilot_store
        from dealix.revenue_ops_autopilot.war_room import build_daily_summary

        summary = build_daily_summary(get_autopilot_store().list_leads(limit=600))
        for row in summary.get("top_targets") or []:
            if isinstance(row, dict):
                name = row.get("company") or row.get("name") or "—"
                lines.append(f"- {name} · score={row.get('lead_score')} · {row.get('status')}")
    except Exception as exc:
        lines.append(f"(store: {exc})")
    lines.append("")
    lines.append("أو: `data/war_room_today.json` بعد war_room_sync")
    return "\n".join(lines)


def export_markdown(payload: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    for i, draft in enumerate(payload.get("drafts") or [], 1):
        body = draft.get("body") or ""
        md = f"""# LinkedIn · {draft.get('title_ar', draft.get('id'))}

## SOAEN
{chr(10).join(f'- [ ] {c}' for c in SOAEN)}

## نص
{body}

---
**لا تنشر تلقائياً** — انسخ بعد الموافقة.
"""
        path = out_dir / f"{stamp}_linkedin_{i}.md"
        path.write_text(md, encoding="utf-8")
        print(f"WROTE · {path.relative_to(REPO_ROOT)}")

    outline = f"""# Newsletter outline · {payload.get('iso_week', '')}

- رؤية الأسبوع
- خطأ شائع في المتابعة
- إطار SOAEN
- CTA موحّد

عدد مسودات LinkedIn: {payload.get('draft_count', 0)}
"""
    (out_dir / f"{stamp}_newsletter_outline.md").write_text(outline, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--week", type=int, default=None)
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--skip-weekly-json", action="store_true")
    args = p.parse_args()

    if not args.skip_weekly_json:
        cmd = [sys.executable, str(REPO_ROOT / "scripts/generate_weekly_content_drafts.py"), "--count", str(args.count)]
        if args.week is not None:
            cmd.extend(["--week", str(args.week)])
        proc = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
        if proc.returncode != 0:
            return proc.returncode

    json_files = sorted(WEEKLY_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not json_files:
        print("FAIL: no var/content_drafts/*.json", file=sys.stderr)
        return 1
    payload = json.loads(json_files[0].read_text(encoding="utf-8"))
    export_markdown(payload, DRAFTS_MD)

    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    out_path = DRAFTS_MD / f"{stamp}_outreach_targets.md"
    out_path.write_text(outreach_targets_md(), encoding="utf-8")
    print(f"WROTE · {out_path.relative_to(REPO_ROOT)}")
    print("\nانسخ إلى LinkedIn بعد الموافقة — لا نشر تلقائي.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
