from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "reports" / "company_os" / "weekly"
out.mkdir(parents=True, exist_ok=True)

text = f"""# Dealix Growth Scorecard

Generated: {datetime.now(UTC).isoformat()}

| Metric | Target |
|---|---:|
| Warm manual messages | 5/day |
| Replies | 1/day |
| Discovery calls | 3/week |
| P1 proposals | 2/week |
| Closed P1 | 1/week |
| P2 candidates | 1/week |

CEO rule: if messages sent today = 0, stop building and send manually.
"""
(out / "GROWTH_SCORECARD.md").write_text(text, encoding="utf-8")
print("DEALIX_GROWTH_SCORECARD=PASS")
