"""Generate a campaign pack.

Usage:
    python3 scripts/generate_campaign_pack.py --campaign revenue-os --lang both
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "campaigns" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


CAMPAIGNS = {
    "revenue-os": {
        "target": "Marketing agencies, B2B services in KSA",
        "pain": "Inbound leads fall through the cracks",
        "post": "If your lead response is wide, your close rate is invisible. Dealix installs the response flow with human-reviewed drafts. No spam, no auto-send.",
        "whatsapp": "مرحبًا، شفت إن فريقكم يستقبل ليدز لكن المتابعة تتأخر. Dealix يحلّها بمسوّدات مولّدة + مراجعة بشرية.",
        "email": "Subject: 20-min Workflow Review\n\nHi [Name],\n\nI noticed [Company] ships strong work but inbound response is slow.\n\nDealix installs the response flow with human-reviewed drafts — no spam, no auto-send.\n\n20-min diagnostic?",
        "linkedin": "Hi [Name], I came across [Company] and noticed your inbound response window. Dealix closes it with a draft + human-review flow. 20-min call?",
        "followup": "Day 3: light followup. Day 7: case card. Day 14: pass.",
    },
    "review-os": {
        "target": "Clinics, real estate, local services in KSA",
        "pain": "Google reviews are silent",
        "post": "If your Google reviews get no replies, you are losing trust without knowing. Dealix installs Review OS with human-approved replies + a monthly report.",
        "whatsapp": "السلام عليكم، لاحظت إن تقييمات Google عندكم ما عليها رد. Dealix يركّب نظام ردود بموافقة بشرية.",
        "email": "Subject: Your Google reviews\n\nHi [Name],\n\nI noticed your Google reviews get no replies.\n\nDealix installs Review OS with human-approved replies + a monthly report.\n\n20-min diagnostic?",
        "linkedin": "Hi [Name], I noticed your Google reviews aren't being replied to. Dealix installs Review OS with human-approved replies.",
        "followup": "Day 3: case study. Day 7: pass.",
    },
    "command-center": {
        "target": "Multi-entity groups, 20+ employees",
        "pain": "Founder is the bottleneck",
        "post": "If you take a 2-week vacation, the company slows. Dealix installs Command Center OS — 5 KPIs, 1 owner each, weekly review.",
        "whatsapp": "السلام عليكم، شفت إنكم في مرحلة توسع والمؤسس يدخل في كل قرار. Dealix يركّب غرفة قيادة بخمسة مؤشرات فقط.",
        "email": "Subject: One-page decision view\n\nHi [Name],\n\nI noticed [Company] is scaling but the founder is in every decision.\n\nDealix installs Command Center OS — 5 KPIs, 1 owner each, weekly review.\n\n20-min diagnostic?",
        "linkedin": "Hi [Name], I noticed [Company] is scaling and the founder is in every decision. Dealix installs Command Center OS.",
        "followup": "Day 3: agenda. Day 7: 1-page sample.",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", required=True, choices=list(CAMPAIGNS.keys()))
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    c = CAMPAIGNS[args.campaign]
    today = dt.date.today().isoformat()
    body = f"""# Campaign Pack — {args.campaign} ({today})

## Target segment
{c['target']}

## Pain angle
{c['pain']}

## Post copy
{c['post']}

"""
    if args.lang in ("ar", "both"):
        body += f"""## WhatsApp (AR)
{c['whatsapp']}

"""
    if args.lang in ("en", "both"):
        body += f"""## Email (EN)
{c['email']}

## LinkedIn (EN)
{c['linkedin']}

"""

    body += f"""## Follow-up cadence
{c['followup']}

## Landing page CTA
Visit /book for a 20-min diagnostic.

## Review checklist
- [ ] All posts reviewed by founder
- [ ] No fake claims
- [ ] No guaranteed outcomes
- [ ] Review status = approved before send
"""
    out = EXPORT_DIR / f"{args.campaign}-campaign-pack-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
