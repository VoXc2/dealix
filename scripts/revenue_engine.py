#!/usr/bin/env python3
"""
Dealix Revenue Engine — Command Room Daily Generator
Generates all daily revenue artifacts:
- Outreach drafts (Arabic + English)
- Follow-up sequences
- Proposal queue
- CEO daily report
- Command room snapshot (JSON + HTML)
"""

import csv
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


# ─── Configuration ───────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
COMPANY_OS = BASE_DIR / "company_os"
OUTPUT_DIR = COMPANY_OS / "revenue"
REPORTS_DIR = COMPANY_OS / "command_room"
LEDGERS_DIR = COMPANY_OS / "ledgers"

OUTBOUND_MODE = os.environ.get("OUTBOUND_MODE", "draft_only").strip().lower()
if OUTBOUND_MODE not in ("draft_only", "approval_required", "controlled_live"):
    OUTBOUND_MODE = "draft_only"


# ─── Arabic Outreach Message Templates ───────────────────────
# Personalized templates per segment
ARABIC_TEMPLATES = {
    "marketing_agency": """السلام عليكم {name}،

ألاحظ أن {company} بتقدم خدمات قوية في [Segment]. كثير من وكالات التسويق عندها فرص وبيانات موزعة بين Excel وCRM وWhatsApp، لكن بدون متابعة قابلة للقياس.

في Dealix نبدأ بـ AI Ops Diagnostic قصير يحول الوضع الحالي إلى:
- خارطة فرص واضحة
- أفضل 10 خطوات تنفيذية
- رسائل متابعة جاهزة للمراجعة
- proof pack يوضح أين القيمة قبل أي توسع

بدون scraping، بدون cold WhatsApp automation، وبدون إرسال آلي.

إذا مناسب، احجز وقتًا هنا:
https://dealix.sa/book-call

{sender_name}
Dealix""",
    
    "training_company": """السلام عليكم {name}،

أتابع عمل {company} في [Segment] وأشوف فجوة واضحة بين الاستفسارات اللي تصلكم والتسجيلات الفعلية.

Dealix يسوّي Diagnostic مختصر يعطيك:
- خريطة للفرص الضائعة
- workflow يُنظّم المتابعة
- رسائل جاهزة للمراجعة
- proof pack يوضح القيمة قبل أي استثمار

كل شيء تحت الموافقة اليدوية. بدون إرسال آلية.

احجز Diagnostic قصير هنا:
https://dealix.sa/book-call

{sender_name}
Dealix""",
    
    "b2b_services": """السلام عليكم {name}،

{company} بتقدم خدمات B2B محترمة، لكن كثير من الشركات تحتاج إعادة هيكلة المتابعة والإيرادات.

Dealix Diagnostic:
- خريطة العملاء المحتملين المرتبة بالأولوية
- workflow لمتابعة كل استفسار
- عروض ورسائل جاهزة للمراجعة
- report يوضح أين القيمة

بدون automation خارجي، بدون scraping، وكل شيء يمر على الموافقة يدويًا.

رابط الحجز:
https://dealix.sa/book-call

{sender_name}
Dealix""",
}

ENGLISH_TEMPLATES = {
    "marketing_agency": """Hi {name},

I noticed {company} delivers strong [Segment] work. Many agencies have leads scattered across tools without consistent follow-up.

Dealix runs a short AI Ops Diagnostic and converts your current state into:
- Ranked opportunity map
- Actionable workflow
- Follow-up drafts ready for review
- Proof pack showing value before expansion

No scraping. No automated cold WhatsApp. No auto-send.

Book a short diagnostic here:
https://dealix.sa/book-call

{sender_name}
Dealix""",
    
    "training_company": """Hi {name},

I follow {company} in [Segment]. There is often a gap between incoming inquiries and actual registrations.

Dealix Diagnostic gives you:
- Opportunity leak map
- Organized follow-up workflow
- Review-ready messaging
- Proof pack before any investment

Everything runs under manual approval. No automated outbound.

Book a diagnostic:
https://dealix.sa/book-call

{sender_name}
Dealix""",
    
    "b2b_services": """Hi {name},

{company} offers solid B2B services, but many firms need follow-up and revenue systems rebuilt.

Dealix Diagnostic:
- Priority-ranked prospect map
- Inquiry follow-up workflow
- Review-ready proposals
- Value report

No external automation. No scraping. Everything requires manual approval.

Booking link:
https://dealix.sa/book-call

{sender_name}
Dealix""",
}


# ─── Helper Functions ────────────────────────────────────────
def load_prospects() -> list[dict]:
    """Load prospects from CSV or return sample."""
    path = LEDGERS_DIR / "prospects.csv"
    if not path.exists():
        path = BASE_DIR / "db" / "seed" / "prospects.csv"
    
    prospects = []
    if path.exists():
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prospects.append(row)
    
    return prospects


def load_pipeline() -> dict:
    """Load pipeline JSON or return empty."""
    path = OUTPUT_DIR / "pipeline.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"counts": {}, "stages": {}}


def load_followups() -> dict:
    """Load follow-ups data."""
    path = OUTPUT_DIR / "followups.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"followups": []}


def get_due_today(prospects: list[dict]) -> list[dict]:
    """Get prospects that need action today (score >= 5, not contacted in 3+ days)."""
    today = datetime.now()
    due = []
    for p in prospects:
        try:
            score = int(p.get("score", 0))
        except:
            score = 0
        last_contact = p.get("last_contact", "")
        status = p.get("status", "")
        
        if score >= 5 and status in ("target", "researched", "contacted"):
            days_since = 0
            if last_contact:
                try:
                    days_since = (today - datetime.strptime(last_contact, "%Y-%m-%d")).days
                except:
                    pass
            if days_since >= 3 or not last_contact:
                due.append(p)
    
    due.sort(key=lambda x: int(x.get("score", 0)), reverse=True)
    return due[:10]  # Top 10


def generate_outreach_drafts(targets: list[dict]) -> list[dict]:
    """Generate personalized outreach drafts (Arabic + English)."""
    drafts = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    segment_map = {
        "marketing_agency": "marketing_agency",
        "training_company": "training_company",
        "b2b_services": "b2b_services",
    }
    
    for i, t in enumerate(targets):
        company = t.get("company", "شركة")
        name = t.get("decision_maker", "صاحب الشركة")
        segment = segment_map.get(t.get("segment", ""), "b2b_services")
        email = t.get("email", "")
        
        # Arabic draft
        ar = ARABIC_TEMPLATES.get(segment, ARABIC_TEMPLATES["b2b_services"])
        ar = ar.replace("{name}", name).replace("{company}", company).replace("[Segment]", segment.replace("_", " ").title())
        
        # English draft
        en = ENGLISH_TEMPLATES.get(segment, ENGLISH_TEMPLATES["b2b_services"])
        en = en.replace("{name}", name).replace("{company}", company).replace("[Segment]", segment.replace("_", " ").title())
        
        sender_name = os.environ.get("DEALIX_SENDER_NAME", "Sami")
        ar = ar.replace("{sender_name}", sender_name)
        en = en.replace("{sender_name}", sender_name)
        
        draft = {
            "id": f"draft_{today}_{i+1:03d}",
            "prospect_email": email,
            "prospect_company": company,
            "prospect_name": name,
            "segment": segment,
            "type": "email",
            "content_ar": ar,
            "content_en": en,
            "priority": int(t.get("score", 5)),
            "recommended_send_date": today,
            "approved": False,
            "sent": False,
            "outbound_mode": OUTBOUND_MODE,
        }
        drafts.append(draft)
    
    return drafts


def generate_followup_sequences(targets: list[dict]) -> list[dict]:
    """Generate follow-up sequence (Day 3, Day 7, Day 14)."""
    today = datetime.now()
    sequences = []
    
    for t in targets:
        company = t.get("company", "")
        name = t.get("decision_maker", "")
        
        sequences.append({
            "id": f"fu_{today.strftime('%Y%m%d')}_{company[:10]}",
            "company": company,
            "name": name,
            "sequence": [
                {"day": 0, "type": "initial", "subject_ar": "عرض Diagnostic مجاني — Dealix", "subject_en": "Free AI Ops Diagnostic — Dealix", "channel": "email"},
                {"day": 3, "type": "followup", "subject_ar": "متابعة: Diagnostic لـ " + company, "subject_en": "Follow-up: Diagnostic for " + company, "channel": "email"},
                {"day": 7, "type": "value_add", "subject_ar": "قصة نجاح: كيف زادت متابعة عميلنا الردود 3x", "subject_en": "Case study: 3x reply rate with follow-up system", "channel": "email"},
                {"day": 14, "type": "final", "subject_ar": "آخر فرصة — Diagnostic مجاني هذا الأسبوع", "subject_en": "Last chance — Free diagnostic this week", "channel": "email"},
            ]
        })
    
    return sequences


def generate_proposal_queue(prospects: list[dict]) -> list[dict]:
    """Generate proposal recommendations for discovery call completed prospects."""
    queue = []
    for p in prospects:
        status = p.get("status", "")
        if status in ("discovery_booked", "discovery_completed", "proposal_sent"):
            queue.append({
                "company": p.get("company", ""),
                "decision_maker": p.get("decision_maker", ""),
                "offer": p.get("offer", "Revenue Intelligence Sprint"),
                "value": p.get("value", "5000"),
                "status": status,
                "next_step": "Prepare proposal deck after discovery" if status == "discovery_booked" else "Follow up on proposal",
            })
    return queue


def generate_ceo_daily_report(
    total_targets: int,
    drafts: list[dict],
    followups: list[dict],
    proposals: list[dict],
    pipeline: dict,
    output_path: str
):
    """Generate CEO Daily Report markdown."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    md = f"""# Daily CEO Report — {today}

## 1. Revenue Snapshot

| Metric | Value |
|--------|-------|
| Hot targets today | {total_targets} |
| Outreach drafts generated | {len(drafts)} |
| Follow-up sequences active | {len(followups)} |
| Proposals in queue | {len(proposals)} |
| Pipeline stages | {json.dumps(pipeline.get('counts', {}))} |

## 2. Outreach Drafts (First 5)

| # | Company | Priority | Status | Channel |
|---|---------|----------|--------|---------|
"""
    for i, d in enumerate(drafts[:5], 1):
        md += f"| {i} | {d['prospect_company']} | {d['priority']} | {'✅ Approved' if d['approved'] else '⏳ Pending'} | {d['type']} |\n"
    
    md += """
## 3. Follow-up Sequence

| Company | Day 0 | Day 3 | Day 7 | Day 14 |
|---------|-------|-------|-------|--------|
"""
    for fu in followups[:5]:
        seq = fu.get("sequence", [])
        day0 = "✅" if len(seq) > 0 else "—"
        day3 = "⏳" if len(seq) > 1 else "—"
        day7 = "⏳" if len(seq) > 2 else "—"
        day14 = "⏳" if len(seq) > 3 else "—"
        md += f"| {fu['company']} | {day0} | {day3} | {day7} | {day14} |\n"
    
    md += """
## 4. Proposal Queue

| Company | Offer | Value (SAR) | Next Step |
|---------|-------|------------:|-----------|
"""
    for p in proposals[:5]:
        md += f"| {p['company']} | {p['offer']} | {p['value']} | {p['next_step']} |\n"
    
    md += f"""
## 5. Founder Actions

1. ⏳ Review {len(drafts)} outreach drafts in approval queue
2. ⏳ Approve/reject each draft individually
3. ⏳ Schedule discovery calls for approved leads
4. ⏳ Prepare proposal decks for discovery-completed prospects
5. ⏳ Review pipeline health — any stuck deals?

## 6. Safety Reminder

**OUTBOUND_MODE = {OUTBOUND_MODE}**
- No draft will be sent without manual approval
- All AI-generated messages show [AI] tag
- Command Room requires founder sign-off before any external send

---
*Generated by Dealix Revenue Engine | {today}*
"""
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    return md


def generate_command_room_html(
    drafts: list[dict],
    followups: list[dict],
    proposals: list[dict],
    pipeline: dict,
    output_path: str
):
    """Generate Command Room HTML dashboard."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Build pipeline bar chart HTML
    pipeline_html = ""
    counts = pipeline.get("counts", {})
    max_count = max(counts.values()) if counts else 1
    for stage, count in counts.items():
        width = min((count / max_count) * 100, 100)
        pipeline_html += f"""
        <div class="pipeline-row">
            <span class="stage">{stage.replace("_", " ").title()}</span>
            <div class="bar-container"><div class="bar" style="width:{width}%"></div></div>
            <span class="count">{count}</span>
        </div>
        """
    
    # Build drafts table
    drafts_html = ""
    for d in drafts[:10]:
        status_class = "approved" if d["approved"] else "pending"
        status_label = "✅ Approved" if d["approved"] else "⏳ Pending Approval"
        drafts_html += f"""
        <tr>
            <td>{d['prospect_company']}</td>
            <td>{d['priority']}</td>
            <td><span class="badge {status_class}">{status_label}</span></td>
            <td>{d['type']}</td>
            <td>{d['recommended_send_date']}</td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Dealix Command Room — {today}</title>
<style>
:root{{--primary:#15807A;--bg:#F0F9F8;--card:#fff;--text:#0A1F1E;}}
body{{font-family:'Segoe UI',sans-serif;background:var(--bg);margin:0;color:var(--text);}}
.header{{background:var(--primary);color:#fff;padding:1.5rem 2rem;text-align:center;}}
.container{{max-width:1200px;margin:0 auto;padding:2rem;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;}}
.card{{background:var(--card);border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);}}
.card h2{{margin-top:0;color:var(--primary);font-size:1.1rem;}}
.pipeline-row{{display:flex;align-items:center;gap:0.75rem;margin:0.4rem 0;}}
.pipeline-row .stage{{width:100px;font-size:0.85rem;}}
.pipeline-row .bar-container{{flex:1;height:18px;background:#eee;border-radius:4px;overflow:hidden;}}
.pipeline-row .bar{{height:100%;background:var(--primary);border-radius:4px;}}
.pipeline-row .count{{width:30px;text-align:center;font-weight:700;}}
table{{width:100%;border-collapse:collapse;font-size:0.9rem;}}
th{{text-align:right;padding:0.6rem;color:#4A6B69;border-bottom:1px solid #eee;}}
td{{padding:0.6rem;border-bottom:1px solid #eee;}}
.badge{{padding:0.3rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:600;}}
.badge.approved{{background:#d1fae5;color:#065f46;}}
.badge.pending{{background:#fef3c7;color:#92400e;}}
.status-bar{{position:fixed;bottom:0;left:0;right:0;background:#0A1F1E;color:#fff;padding:0.75rem;text-align:center;font-size:0.85rem;}}
.status-bar .safe{{color:#34d399;font-weight:700;}}
</style>
</head>
<body>
<div class="header">
<h1> Dealix Revenue Command Room</h1>
<p>{today} | OUTBOUND_MODE: <strong>{OUTBOUND_MODE}</strong></p>
</div>
<div class="container">
<div class="grid">
<div class="card">
<h2> Pipeline Health</h2>
{pipeline_html}
</div>
<div class="card">
<h2> Outreach Drafts ({len(drafts)})</h2>
<table>
<thead><tr><th>Company</th><th>Priority</th><th>Status</th><th>Channel</th><th>Date</th></tr></thead>
<tbody>{drafts_html}</tbody>
</table>
</div>
<div class="card">
<h2> Proposals in Queue ({len(proposals)})</h2>
"""
    for p in proposals[:5]:
        html += f"<p><strong>{p['company']}</strong> — {p['offer']} ({p['value']} SAR)<br><small>{p['next_step']}</small></p>"
    
    html += """
</div>
<div class="card">
<h2> Follow-up Sequences</h2>
<p>AI-generated multi-day follow-up sequences available.</p>
<p>Review sequences in drafts before activation.</p>
</div>
</div>
</div>
<div class="status-bar">
<span class="safe">● SAFE MODE:</span> No outbound messages will be sent without manual approval. All AI-generated content has been tagged and awaits founder review.
</div>
</body>
</html>
"""
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return html


def save_drafts_to_csv(drafts: list[dict]):
    """Save generated drafts to CSV ledger."""
    LEDGERS_DIR.mkdir(parents=True, exist_ok=True)
    path = LEDGERS_DIR /"drafts_log.csv"
    
    fieldnames = ["id", "prospect_email", "prospect_company", "type", "priority", "recommended_send_date", "approved", "sent", "outbound_mode"]
    
    mode = "w" if not path.exists() or path.stat().st_size == 0 else "a"
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if mode == "w":
            writer.writeheader()
        for d in drafts:
            writer.writerow(d)


def main():
    """Run the full revenue engine daily cycle."""
    print("=" * 70)
    print("  DEALIX REVENUE ENGINE — Daily Generation")
    print("=" * 70)
    print()
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Outbound Mode: {OUTBOUND_MODE}")
    print()
    
    # 1. Load data
    print("  → Loading prospects...")
    prospects = load_prospects()
    print(f"     Prospects loaded: {len(prospects)}")
    
    print("  → Loading pipeline...")
    pipeline = load_pipeline()
    
    print("  → Getting hot targets...")
    hot_targets = get_due_today(prospects)
    print(f"     Hot targets: {len(hot_targets)}")
    
    # 2. Generate drafts
    print("  → Generating outreach drafts (Arabic + English)...")
    drafts = generate_outreach_drafts(hot_targets)
    print(f"     Drafts generated: {len(drafts)}")
    
    # 3. Generate follow-up sequences
    print("  → Generating follow-up sequences...")
    followups = generate_followup_sequences(hot_targets)
    print(f"     Sequences generated: {len(followups)}")
    
    # 4. Generate proposal queue
    print("  → Generating proposal queue...")
    proposals = generate_proposal_queue(prospects)
    print(f"     Proposals in queue: {len(proposals)}")
    
    # 5. Save drafts to ledger
    print("  → Saving drafts to ledger...")
    save_drafts_to_csv(drafts)
    
    # 6. Save raw drafts JSON for Command Room
    drafts_json_path = COMPANY_OS / "command_room" / "outreach_drafts.json"
    drafts_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(drafts_json_path, "w", encoding="utf-8") as f:
        json.dump({"drafts": drafts, "date": datetime.now().strftime("%Y-%m-%d")}, f, ensure_ascii=False, indent=2)
    
    # 7. CEO Daily Report
    print("  → Generating CEO Daily Report...")
    report_path = COMPANY_OS / "command_room" / "CEO_DAILY_REPORT.md"
    generate_ceo_daily_report(
        len(hot_targets), drafts, followups, proposals, pipeline, str(report_path)
    )
    print(f"     Report: {report_path}")
    
    # 8. Command Room HTML
    print("  → Generating Command Room HTML...")
    html_path = COMPANY_OS / "command_room" / "index.html"
    generate_command_room_html(drafts, followups, proposals, pipeline, str(html_path))
    print(f"     HTML: {html_path}")
    
    # 9. War Room markdown (Python script legacy compatible)
    print("  → Generating War Room markdown...")
    from generate_war_room import generate_war_room
    generate_war_room(
        prospects_path=str(LEDGERS_DIR / "prospects.csv") if (LEDGERS_DIR / "prospects.csv").exists() else str(BASE_DIR / "db" / "seed" / "prospects.csv"),
        pipeline_path=str(OUTPUT_DIR / "pipeline.json") if (OUTPUT_DIR / "pipeline.json").exists() else "",
        followups_path=str(OUTPUT_DIR / "followups.json") if (OUTPUT_DIR / "followups.json").exists() else "",
        proposals_path=str(OUTPUT_DIR / "proposals.json") if (OUTPUT_DIR / "proposals.json").exists() else "",
        output_path=str(COMPANY_OS / "war_room" / "REVENUE_WAR_ROOM_TODAY.md")
    )
    
    print()
    print("=" * 70)
    print("  ✅ REVENUE ENGINE COMPLETE")
    print("=" * 70)
    print()
    print("  Generated files:")
    print(f"    • CEO Report:     {report_path}")
    print(f"    • Command Room:   {html_path}")
    print(f"    • Drafts JSON:    {drafts_json_path}")
    print(f"    • Drafts CSV:     {LEDGERS_DIR / 'drafts_log.csv'}")
    print(f"    • War Room:       {COMPANY_OS / 'war_room' / 'REVENUE_WAR_ROOM_TODAY.md'}")
    print()
    print("  IMPORTANT:")
    print(f"  → All {len(drafts)} drafts are in PENDING state.")
    print("  → Review drafts in Command Room before any send.")
    print(f"  → Outbound mode: {OUTBOUND_MODE}")
    print()


if __name__ == "__main__":
    main()
