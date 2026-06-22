#!/usr/bin/env python3
"""
Dealix Outreach Engine
Generates WhatsApp/Email follow-up sequences, handles approval queue, and sequences.
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "company_os" / "revenue"
LEDGERS_DIR = BASE_DIR / "company_os" / "ledgers"

OUTBOUND_MODE = os.environ.get("OUTBOUND_MODE", "draft_only").strip().lower()

# ─── Sequence Templates (Arabic) ────────────────────────────────
WHATSAPP_AR_SEQUENCES = {
    "initial": """السلام عليكم {name}،

أهلاً بك. أنا من Dealix ونقدم خدمات آمنة للمتبوعين.

هل حاب تسوي Diagnostic مجاني لإيرادات شركتك؟ 🎯

— {sender_name}""",
    "followup": """{name}،

كيف الحال؟ نفس العرض باقي موجود — Diagnostic مجاني + خطة عمل.

هل مناسب الأسبوع الجاي؟ 📅

— {sender_name}""",
    "value_add": """{name}،

أبي أشاركك قصة عميلنا في {similar_company}:

• قبل Dealix: متابعات بدون نظام → 30% ردود
• بعد Dealix: drafts جاهزة + approval queue → 75% ردود

هل تحب新版本 تتشابه؟

— {sender_name}""",
    "final": """{name}،

آخر فرصة لهذا الشهر للـ Diagnostic المجاني.

نكتمها مو؟ أو نتقدم على الجائزة. 🙏

— {sender_name}""",
}

WHATSAPP_EN_SEQUENCES = {
    "initial": """Hi {name},

I'm from Dealix and I'm offering a free AI Revenue Diagnostic.

Care to get a quick analysis of where your biggest revenue leak is? 🎯

— {sender_name}""",
    "followup": """{name},

The offer is still live — free Diagnostic + action plan.

Would next week work? 📅

— {sender_name}""",
    "value_add": """{name},

Quick win story from {similar_company}:

• Before Dealix: scattered follow-ups → 30%
• After Dealix: approval queue + AI drafts → 75% reply rate

Want a similar version? 🚀

— {sender_name}""",
    "final": """{name},

Final call on the free Diagnostic this month.

Shall we? 🙏

— {sender_name}""",
}

EMAIL_AR_SEQUENCES = {
    "initial": WHATSAPP_AR_SEQUENCES["initial"],
    "followup": WHATSAPP_AR_SEQUENCES["followup"],
    "value_add": WHATSAPP_AR_SEQUENCES["value_add"],
    "final": WHATSAPP_AR_SEQUENCES["final"],
}

EMAIL_EN_SEQUENCES = {
    "initial": WHATSAPP_EN_SEQUENCES["initial"],
    "followup": WHATSAPP_EN_SEQUENCES["followup"],
    "value_add": WHATSAPP_EN_SEQUENCES["value_add"],
    "final": WHATSAPP_EN_SEQUENCES["final"],
}


def load_prospects() -> list[dict]:
    """Load prospects CSV or return sample."""
    import csv
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


def generate_followup_sequences(prospect: dict) -> list[dict]:
    """Generate multi-day follow-up sequence from a prospect."""
    company = prospect.get("company", "")
    name = prospect.get("decision_maker", prospect.get("contact_person", ""))
    segment = prospect.get("segment", "b2b_services")
    sender_name = os.environ.get("DEALIX_SENDER_NAME", "Sami")
    prospect_email = prospect.get("email", "")

    seq = [
        { "day": 0, "type": "initial", "subject_ar": f"عرض Diagnostic مجاني — {company}", "subject_en": f"Free AI Revenue Diagnostic — {company}", "content_ar": EMAIL_AR_SEQUENCES["initial"].format(name=name, sender_name=sender_name), "content_en": EMAIL_EN_SEQUENCES["initial"].format(name=name, sender_name=sender_name), "channel": "email", "status": "draft" },
        { "day": 3, "type": "followup", "subject_ar": f"متابعة: Diagnostic لـ {company}", "subject_en": f"Follow-up: Diagnostic for {company}", "content_ar": EMAIL_AR_SEQUENCES["followup"].format(name=name, sender_name=sender_name), "content_en": EMAIL_EN_SEQUENCES["followup"].format(name=name, sender_name=sender_name), "channel": "email", "status": "draft" },
        { "day": 7, "type": "value_add", "subject_ar": f"قصة نجاح: زيادة 3X في الردود", "subject_en": f"Case study: 3X reply rate improvement", "content_ar": EMAIL_AR_SEQUENCES["value_add"].format(name=name, sender_name=sender_name, similar_company="شركة مشابهة"), "content_en": EMAIL_EN_SEQUENCES["value_add"].format(name=name, sender_name=sender_name, similar_company="Similar Company"), "channel": "email", "status": "draft" },
        { "day": 14, "type": "final", "subject_ar": f"آخر فرصة — Diagnostic مجاني", "subject_en": f"Last chance — Free Diagnostic", "content_ar": EMAIL_AR_SEQUENCES["final"].format(name=name, sender_name=sender_name), "content_en": EMAIL_EN_SEQUENCES["final"].format(name=name, sender_name=sender_name), "channel": "email", "status": "draft" },
    ]

    # Mark all as draft
    for s in seq:
        s["approved"] = False
        s["sent"] = False
        s["prospect_email"] = prospect_email
        s["prospect_company"] = company
        s["outbound_mode"] = OUTBOUND_MODE
        s["id"] = f"seq_{datetime.now().strftime('%Y%m%d')}_{company[:10]}_d{s['day']}"

    return seq


def save_sequences(seqs: list[dict]):
    """Save sequences to ledger."""
    LEDGERS_DIR.mkdir(parents=True, exist_ok=True)
    path = LEDGERS_DIR / "outreach_sequences.csv"

    fieldnames = ["id", "day", "type", "channel", "prospect_email", "prospect_company", "subject_ar", "subject_en", "content_ar", "content_en", "status", "approved", "sent", "outbound_mode"]

    import csv
    mode = "a" if path.exists() and path.stat().st_size > 0 else "w"
    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if mode == "w":
            writer.writeheader()
        for s in seqs:
            writer.writerow(s)


def generate_outreach_for_all():
    """Main engine: generate all sequences for all prospects."""
    print("=" * 70)
    print("  DEALIX OUTREACH ENGINE — Multi-Channel Sequence Generator")
    print("=" * 70)
    print()
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Outbound Mode: {OUTBOUND_MODE}")
    print()

    prospects = load_prospects()
    print(f"  → Prospects loaded: {len(prospects)}")

    total_seqs = 0
    for p in prospects:
        seqs = generate_followup_sequences(p)
        save_sequences(seqs)
        total_seqs += len(seqs)

    print(f"  → Sequences generated: {total_seqs}")

    print()
    print("=" * 70)
    print("  ✅ OUTREACH ENGINE COMPLETE")
    print("=" * 70)
    print()
    print(f"  IMPORTANT:")
    print(f"  → All {total_seqs} sequences are in DRAFT state.")
    print("  → Review sequences before any send.")
    print(f"  → Outbound mode: {OUTBOUND_MODE}")
    print(f"  → Ledger saved: {LEDGERS_DIR / 'outreach_sequences.csv'}")
    print()


if __name__ == "__main__":
    generate_outreach_for_all()
