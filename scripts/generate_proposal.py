"""Generate a proposal (bilingual) for a given account + offer.

Usage:
    python3 scripts/generate_proposal.py --account-id demo-acc-003 --offer "Command Center" --lang both --timeline "21 days"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
INDEX_PATH = REPO_ROOT / "business" / "_data" / "proposals.index.json"
EXPORT_DIR = REPO_ROOT / "business" / "proposals" / "generated"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


OFFER_SETUP = {
    "Revenue OS": 18000,
    "Command Center": 35000,
    "Delivery OS": 25000,
    "Review & Reputation": 12000,
    "Custom Enterprise": 80000,
    "Managed Retainer": 0,
}
OFFER_MONTHLY = {
    "Revenue OS": 5000,
    "Command Center": 9000,
    "Delivery OS": 6000,
    "Review & Reputation": 3500,
    "Custom Enterprise": 18000,
    "Managed Retainer": 8000,
}


def render(account: dict, offer: str, lang: str, timeline: str) -> str:
    setup = OFFER_SETUP.get(offer, 0)
    monthly = OFFER_MONTHLY.get(offer, 0)
    lines: list[str] = []
    if lang in ("ar", "both"):
        lines.append(f"# عرض {offer} — {account['name']}")
        lines.append("")
        lines.append("## 1. الملخص التنفيذي")
        lines.append(f"عرض {offer} مخصص لـ {account['name']} بناءً على الإشارة المرئية: {account.get('visibleSignal', '')}.")
        lines.append("")
        lines.append("## 2. فرضية وضع العميل")
        lines.append(f"الضعف المفترض: {account.get('weaknessHypothesis', '')}.")
        lines.append("سيتم التحقق منها في الأسبوع الأول.")
        lines.append("")
        lines.append("## 3. النطاق")
        lines.append("يشمل: Workflow Map، Command Center Setup، أتمتة، تقرير إثبات أسبوعي.")
        lines.append("لا يشمل: أتمتة لقرار مالي أو قانوني، أو scraping لبيانات خاصة.")
        lines.append("")
        lines.append(f"## 4. الجدول الزمني: {timeline}")
        lines.append("")
        lines.append("## 5. الأسعار")
        lines.append(f"- Setup: SAR {setup:,}")
        lines.append(f"- Monthly: SAR {monthly:,}")
        lines.append("")
        lines.append("## 6. الخطوة التالية")
        lines.append("توقيع العقد، ثم مكالمة Day 0 — Intake (60 دقيقة).")
        lines.append("")
        lines.append("---")
        lines.append("Draft only. Requires founder + client sign-off.")
        lines.append("")
    if lang in ("en", "both"):
        lines.append(f"# {offer} Proposal — {account['name']}")
        lines.append("")
        lines.append("## 1. Executive Summary")
        lines.append(f"{offer} for {account['name']} based on visible signal: {account.get('visibleSignal', '')}.")
        lines.append("")
        lines.append("## 2. Client Situation Hypothesis")
        lines.append(f"Assumed weakness: {account.get('weaknessHypothesis', '')}.")
        lines.append("Will be validated in week 1.")
        lines.append("")
        lines.append("## 3. Scope")
        lines.append("Includes: Workflow Map, Command Center Setup, automations, weekly proof report.")
        lines.append("Excludes: financial/legal decision automation, private data scraping.")
        lines.append("")
        lines.append(f"## 4. Timeline: {timeline}")
        lines.append("")
        lines.append("## 5. Pricing")
        lines.append(f"- Setup: SAR {setup:,}")
        lines.append(f"- Monthly: SAR {monthly:,}")
        lines.append("")
        lines.append("## 6. Next Step")
        lines.append("Sign the contract, then a 60-min Day 0 — Intake call.")
        lines.append("")
        lines.append("---")
        lines.append("Draft only. Requires founder + client sign-off.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--timeline", default="21 days")
    args = parser.parse_args()

    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    account = next((a for a in data.get("accounts", []) if a["id"] == args.account_id), None)
    if not account:
        print(f"account not found: {args.account_id}")
        return 1

    body = render(account, args.offer, args.lang, args.timeline)
    today = dt.date.today().isoformat()
    out_file = EXPORT_DIR / f"{account['id']}-{args.offer.lower().replace(' ', '-')}-{today}.md"
    out_file.write_text(body, encoding="utf-8")

    # update index
    index: dict = {"proposals": [], "version": "1.0"}
    if INDEX_PATH.exists():
        try:
            index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    index.setdefault("proposals", []).append(
        {
            "id": f"prop-{account['id']}-{today}",
            "accountId": account["id"],
            "offer": args.offer,
            "lang": args.lang,
            "timeline": args.timeline,
            "setupPrice": OFFER_SETUP.get(args.offer, 0),
            "monthlyPrice": OFFER_MONTHLY.get(args.offer, 0),
            "status": "draft",
            "createdAt": today,
        }
    )
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {out_file}")
    print(f"updated {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
