from pathlib import Path
from datetime import datetime, timezone
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "company_os" / "daily"
OUT.mkdir(parents=True, exist_ok=True)

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "decision": "Sell P1 today. Do not build new features before outreach.",
    "targets": {
        "manual_messages": 5,
        "discovery_calls": 1,
        "proposal": 1
    },
    "links": {
        "demo": "https://web-production-380c3.up.railway.app/ar/demo",
        "revenue_os": "https://web-production-380c3.up.railway.app/revenue-os",
        "zatca": "https://web-production-380c3.up.railway.app/ar/zatca-readiness"
    },
    "guardrails": [
        "no auto-send",
        "no scraping",
        "approval required",
        "no ROI claim without baseline"
    ]
}

(OUT / "STRATEGIC_BRIEF_TODAY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "STRATEGIC_BRIEF_TODAY.md").write_text(f"""# Strategic Brief Today

Generated: {payload['generated_at']}

## Decision

{payload['decision']}

## Targets

- 5 warm manual messages
- 1 discovery call
- 1 proposal

## Links

- Demo: {payload['links']['demo']}
- Revenue OS: {payload['links']['revenue_os']}
- ZATCA: {payload['links']['zatca']}

## Guardrails

- No auto-send
- No scraping
- Approval required
- No ROI claim without baseline
""", encoding="utf-8")

print("DEALIX_STRATEGIC_BRIEF=PASS")
