import json
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
day = datetime.now(UTC).date().isoformat()
out = ROOT / "reports" / "company_os" / "daily"
out.mkdir(parents=True, exist_ok=True)

posts = [
    "Most companies do not need more leads first. They need to know where current opportunities leak: slow follow-up, unclear offer, or no weekly decision rhythm.",
    "AI Sales Ops should not auto-send. The safe operating model is: AI drafts, founder reviews, human sends.",
    "Dealix starts with a Proof Pack before big implementation: leakage map, top follow-ups, objections, and weekly scorecard.",
]

(out / "CONTENT_DRAFTS_TODAY.md").write_text(
    "# Dealix Content Drafts Today\n\n" + "\n\n".join(f"## Draft {i+1}\n\n{p}" for i, p in enumerate(posts)),
    encoding="utf-8",
)
(out / f"content_drafts_{day}.json").write_text(json.dumps({"date": day, "posts": posts}, indent=2), encoding="utf-8")
print("DEALIX_CONTENT_FACTORY_DAILY=PASS")
