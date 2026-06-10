from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dealix.company_brain.policy import CompanyPolicy

DATA = ROOT / "data" / "company_os"
REPORTS = ROOT / "reports" / "company_os"

def now():
    return datetime.now(UTC).isoformat()

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def append_queue():
    q = DATA / "approval_queue" / "manual_outreach_queue.csv"
    q.parent.mkdir(parents=True, exist_ok=True)
    exists = q.exists()
    row = {
        "date": now()[:10],
        "priority": "1",
        "segment": "warm_network",
        "company": "REPLACE_WITH_REAL_COMPANY",
        "contact": "REPLACE_WITH_DECISION_MAKER",
        "channel": "manual_linkedin_or_whatsapp",
        "draft": "I am building Dealix as a Revenue Ops system. In 5-7 days we can produce a Proof Pack showing where revenue leaks, who to follow up with first, and what offer angle to use. Worth a quick demo?",
        "status": "draft",
        "approved": "no",
        "sent_at": "",
        "response": "",
    }
    with q.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)

def main():
    CompanyPolicy.from_env().assert_safe()

    payload = {
        "generated_at": now(),
        "mode": "approval_first_company_brain",
        "rule": "AI drafts. Founder approves. Human sends.",
        "today": {
            "sell": "P1 Revenue Intelligence Sprint",
            "manual_messages_target": 5,
            "discovery_calls_target": 1,
            "proposal_target": 1,
            "links": {
                "demo": "https://web-production-380c3.up.railway.app/ar/demo",
                "revenue_os": "https://web-production-380c3.up.railway.app/revenue-os",
                "zatca": "https://web-production-380c3.up.railway.app/ar/zatca-readiness",
            },
            "do_not_do": ["no auto-send", "no scraping", "no spam", "no ROI claims without baseline"],
        },
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    write(REPORTS / "daily" / "ceo_brain_today.json", json.dumps(payload, ensure_ascii=False, indent=2))
    write(REPORTS / "daily" / "CEO_BRAIN_TODAY.md", """# Dealix CEO Brain Today

Decision: sell P1 Revenue Intelligence Sprint today.

Targets:
- 5 warm manual messages
- 1 discovery call
- 1 P1 proposal
- 0 auto-send

Links:
- Demo: https://web-production-380c3.up.railway.app/ar/demo
- Revenue OS: https://web-production-380c3.up.railway.app/revenue-os
- ZATCA: https://web-production-380c3.up.railway.app/ar/zatca-readiness

Rule: AI drafts. Founder approves. Human sends.
""")
    append_queue()
    print("DEALIX_COMPANY_BRAIN_DAILY=PASS")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
