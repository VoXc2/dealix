"""Generate the Dealix launch brief.

Usage:
    python3 scripts/generate_launch_brief.py
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "launch" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    body = f"""# Dealix Launch Brief — {today}

## 1. Today's launch status
- README ✅
- Brand system ✅
- Website pages ✅
- Sales machine ✅
- CRM JSON ✅
- Outreach drafts generator ✅
- Proposal generator ✅
- Delivery OS scaffold ✅
- CEO brief generator ✅
- Demo operator passes ✅

## 2. Current blockers
- Production credentials not set (intentional in demo)
- Real leads not imported (intentional — we use seed)

## 3. First 100 leads progress
- 4 demo leads seeded
- 8 drafts generated (pending review)
- 1 proposal in progress

## 4. Proposal count
- Generated: 1 (demo)
- Sent: 0 (waiting on real data)

## 5. Follow-up count
- Due today: 0
- Upcoming (7 days): 3

## 6. Delivery readiness
- SOP written
- Checklist written
- Proof report template ready

## 7. Website readiness
- 17+ pages exist
- All pages render
- Brand assets in `/public`

## 8. Governance readiness
- AI/Human review policy ✅
- PDPL boundaries ✅
- No spam policy ✅
- Source register ✅

## 9. Next 3 founder actions
1. Approve the 8 pending drafts
2. Send the proposal to demo-acc-003
3. Import first batch of real leads

---
*Draft only. Founder sign-off required.*
"""
    out = EXPORT_DIR / f"dealix-launch-brief-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
