import json
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "company_os" / "daily"
OUT.mkdir(parents=True, exist_ok=True)

payload = {
    "generated_at": datetime.now(UTC).isoformat(),
    "strategic_decision": "Convert working production into repeatable sales and delivery machine.",
    "today": [
        "Open /ar/demo",
        "Pick 5 warm targets",
        "Send 5 manual approved messages",
        "Book 1 discovery",
        "Prepare 1 P1 proposal"
    ],
    "do_not_do": [
        "Do not add new features before outreach",
        "Do not auto-send",
        "Do not scrape",
        "Do not offer P3 before proof"
    ],
    "links": {
        "demo": "https://web-production-380c3.up.railway.app/ar/demo",
        "revenue_os": "https://web-production-380c3.up.railway.app/revenue-os",
        "zatca": "https://web-production-380c3.up.railway.app/ar/zatca-readiness"
    }
}

(OUT / "SCALE_BRIEF_TODAY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "SCALE_BRIEF_TODAY.md").write_text(f'''# Dealix Scale Brief Today

Generated: {payload["generated_at"]}

## Strategic Decision

{payload["strategic_decision"]}

## Today

- Open /ar/demo
- Pick 5 warm targets
- Send 5 manual approved messages
- Book 1 discovery
- Prepare 1 P1 proposal

## Do Not Do

- No new features before outreach
- No auto-send
- No scraping
- No P3 before proof

## Links

- Demo: {payload["links"]["demo"]}
- Revenue OS: {payload["links"]["revenue_os"]}
- ZATCA: {payload["links"]["zatca"]}
''', encoding="utf-8")

print("DEALIX_SCALE_BRIEF=PASS")
