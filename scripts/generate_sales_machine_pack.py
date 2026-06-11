"""Generate the daily Dealix Sales Machine Pack (Markdown + JSON).

Usage:
    python3 scripts/generate_sales_machine_pack.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "sales-automation" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


LEAD_SOURCES = [
    ("open_data", "Saudi Open Data (Official)", "No auto-send"),
    ("csv_import", "Local CSV Import", "No auto-send"),
    ("manual_research", "Manual Research", "No auto-send"),
    ("website_signal", "Website Signal Analyzer (Local File)", "No auto-send"),
    ("google_places_official", "Google Places API (Official Plan)", "No auto-send"),
    ("hubspot_official", "HubSpot CRM (Official Plan)", "No auto-send"),
    ("whatsapp_business_official", "WhatsApp Business (Official Plan)", "No auto-send"),
    ("referral_warm", "Referral (Warm Intro)", "No auto-send"),
]

PERSUASION_ANGLES = [
    ("leakage_to_revenue", "From leakage to revenue", "Slow follow-up on inbound leads"),
    ("reputation_to_trust", "From scattered reviews to a trust wall", "Reviews on Google/Maps are inconsistent"),
    ("delivery_to_proof", "From delivery to proof", "No weekly report shared with client base"),
    ("data_to_decision", "From data to a one-page decision", "Many dashboards, no daily decision"),
    ("ops_to_growth", "From operational chaos to growth capacity", "Founder is the bottleneck on most decisions"),
]

OFFERS = [
    ("diagnostic_sprint", "Free", "60-min workflow review"),
    ("revenue_os", "SAR 18,000 setup + 5,000/mo", "Lead flow + outreach drafts + proof"),
    ("command_center", "SAR 35,000 setup + 9,000/mo", "One-page decision view"),
    ("delivery_os", "SAR 25,000 setup + 6,000/mo", "Workflow map + automation build"),
    ("review_reputation", "SAR 12,000 setup + 3,500/mo", "Review monitoring + replies"),
    ("custom_enterprise", "SAR 80,000+", "Architecture + custom modules"),
    ("managed_retainer", "SAR 4,000–12,000/mo", "Ongoing ops + reviews"),
]

OPENERS_AR = [
    "مرحبًا [الاسم]، شفت إن [الشركة] تنشر محتوى قوي في [القطاع] بس الاستجابة على الليدز تأخذ وقت. Dealix يحلّه — مسوّدات مولّدة + مراجعة بشرية.",
    "السلام عليكم، لاحظت إن موقعكم ما عنده مسار حجز واضح. Dealix يركّب المسار ويولّد المسوّدات، وأنتم توافقون قبل ما تنرسل.",
]

OPENERS_EN = [
    "Hi [Name], I noticed [Company] publishes strong work in [sector] but inbound response time is wide. Dealix closes that window — no spam, no auto-send.",
    "Hello, I saw your site doesn't surface a clear booking path. Dealix installs the path and drafts the messages; your team approves what goes out.",
]


def render_markdown(date: dt.date) -> str:
    lines: list[str] = []
    lines.append(f"# Dealix Daily Sales Machine Pack — {date.isoformat()}")
    lines.append("")
    lines.append("## Lead sources")
    for sid, label, guardrail in LEAD_SOURCES:
        lines.append(f"- **{label}** — {guardrail}")
    lines.append("")
    lines.append("## Persuasion angles")
    for sid, title, signal in PERSUASION_ANGLES:
        lines.append(f"- **{title}** — signal: {signal}")
    lines.append("")
    lines.append("## Offer ladder")
    for oid, price, scope in OFFERS:
        lines.append(f"- **{oid}** — {price} — {scope}")
    lines.append("")
    lines.append("## Arabic opener (safe template)")
    lines.append("> " + OPENERS_AR[0])
    lines.append("")
    lines.append("## English opener (safe template)")
    lines.append("> " + OPENERS_EN[0])
    lines.append("")
    lines.append("---")
    lines.append("Drafts only. Human review required before any send.")
    return "\n".join(lines) + "\n"


def render_json(date: dt.date) -> dict:
    return {
        "date": date.isoformat(),
        "lead_sources": [{"id": s[0], "label": s[1], "guardrail": s[2]} for s in LEAD_SOURCES],
        "persuasion_angles": [{"id": s[0], "title": s[1], "signal": s[2]} for s in PERSUASION_ANGLES],
        "offer_ladder": [{"id": s[0], "price": s[1], "scope": s[2]} for s in OFFERS],
        "openers": {"ar": OPENERS_AR, "en": OPENERS_EN},
        "safety": {"auto_send": False, "human_review": True, "no_scraping": True},
    }


def main() -> None:
    today = dt.date.today()
    md = EXPORT_DIR / f"dealix-sales-machine-pack-{today.isoformat()}.md"
    js = EXPORT_DIR / f"dealix-sales-machine-pack-{today.isoformat()}.json"
    md.write_text(render_markdown(today), encoding="utf-8")
    js.write_text(json.dumps(render_json(today), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {md}")
    print(f"wrote {js}")


if __name__ == "__main__":
    main()
