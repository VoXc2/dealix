"""Generate the founder dashboard data (JSON).

Usage:
    python3 scripts/generate_founder_dashboard_data.py --mode demo
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "business" / "_generated" / "founder-dashboard.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    args = parser.parse_args()

    leads_path = REPO_ROOT / "business" / "_data" / "leads.json"
    queue_path = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"

    accounts: list[dict] = []
    if leads_path.exists():
        try:
            accounts = json.loads(leads_path.read_text(encoding="utf-8")).get("accounts", [])
        except json.JSONDecodeError:
            accounts = []
    if not accounts:
        seed = REPO_ROOT / "business" / "crm" / "prospects.seed.json"
        if seed.exists():
            accounts = json.loads(seed.read_text(encoding="utf-8")).get("accounts", [])

    review_pending = 0
    if queue_path.exists():
        try:
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            review_pending = sum(1 for d in queue.get("drafts", []) if d.get("reviewStatus") == "draft_pending_human_review")
        except json.JSONDecodeError:
            review_pending = 0

    today = dt.date.today()
    followups_due = 0
    for a in accounts:
        nd = a.get("nextActionDate")
        if not nd:
            continue
        try:
            if dt.date.fromisoformat(nd) <= today:
                followups_due += 1
        except ValueError:
            pass

    proposal_ready = sum(1 for a in accounts if a.get("stage") in ("proposal", "meeting"))
    pipeline_value_sar = 0
    for a in accounts:
        if a.get("stage") in ("won", "lost"):
            continue
        pipeline_value_sar += (a.get("setupValue") or 0) + (a.get("monthlyValue") or 0) * 3
    segment_counts: dict[str, int] = {}
    for a in accounts:
        s = a.get("segment", "—")
        segment_counts[s] = segment_counts.get(s, 0) + 1
    top_segment = max(segment_counts.items(), key=lambda x: x[1])[0] if segment_counts else "—"

    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": args.mode,
        "summary": {
            "total_accounts": len(accounts),
            "review_pending": review_pending,
            "followups_due": followups_due,
            "proposal_ready": proposal_ready,
            "pipeline_value_sar": pipeline_value_sar,
            "top_segment": top_segment,
        },
        "top_accounts": [
            {
                "id": a["id"],
                "name": a["name"],
                "segment": a.get("segment", ""),
                "score": a.get("score", 0),
                "stage": a.get("stage", ""),
                "reviewStatus": a.get("reviewStatus", ""),
            }
            for a in sorted(accounts, key=lambda x: x.get("score", 0), reverse=True)[:5]
        ],
        "risks": [
            "Review queue has drafts pending — clear before any new outreach.",
            "Pipeline value is concentrated in top accounts — diversify the top of funnel.",
            "Demo accounts should never be reported as real traction.",
        ],
        "today_actions": [
            "Approve or reject pending drafts",
            "Send the highest-priority proposal",
            "Log 1 proof item from any active delivery",
            "Generate today's CEO brief",
        ],
        "assets_to_create": [
            "Daily CEO brief (.txt)",
            "Outreach draft (top scored lead)",
            "Proposal (highest-value demo account)",
        ],
        "next_ceo_decision": "Approve the review queue and ship the proposal to the highest-value demo account.",
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
