#!/usr/bin/env python3
"""
Generate Outreach Queue for Dealix
Selects top prospects, generates messages, adds to approval queue
Usage: python generate_outreach_queue.py --limit 10
"""

import argparse
import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuration
COMPANY_OS_DIR = Path(__file__).parent.parent
PROSPECTS_FILE = COMPANY_OS_DIR / "revenue" / "prospects.csv"
OUTREACH_FILE = COMPANY_OS_DIR / "revenue" / "outreach_queue.json"
APPROVAL_FILE = COMPANY_OS_DIR / "governance" / "approval_queue.json"
LEDGER_FILE = COMPANY_OS_DIR / "governance" / "ai_action_ledger.jsonl"

SA_TZ = timezone(timedelta(hours=3))

# Message templates by segment
TEMPLATES = {
    "Marketing Agency": {
        "subject": "كيف تثبتون قيمة التسويق لعملائكم؟",
        "body": """السلام عليكم [الاسم]،

لاحظت أن كثير من وكالات التسويق تواجه تحدي إثبات النتائج للعملاء. عملاء يدفعون ويسألون: "وش استفدنا؟"

في Dealix نبني لكم نظام يثبت أين تضيع فرص عملائكم:
• خريطة تسرب الإيرادات
• Proof Pack أسبوعي/شهري
• تحليل المتابعة والردود

نبدأ بـ Sprint 5 أيام يكشف الوضع الحقيقي.

هل يناسبك نشرح أكثر؟

مع التحية،
[اسمك]"""
    },
    "Training": {
        "subject": "تحويل الاستفسارات إلى تسجيلات مدفوعة",
        "body": """السلام عليكم [الاسم]،

كثير من مراكز التدريب تستقبل استفسارات كثيرة لكن نسبة التحويل إلى تسجيلات تبقى أقل من المتوقع.

في Dealix نسوي Revenue Intelligence Sprint خلال 5 أيام:
• نكشف أين تضيع فرص التسجيل
• نحلل جودة المتابعة والردود
• نطلع Proof Pack واضح + خطة 30 يوم لتحسين التحويل

هل يناسبك أرسل لك مثال مختصر على شكل التقرير؟

مع التحية،
[اسمك]"""
    },
    "B2B Services": {
        "subject": "أين تضيع صفقاتكم؟",
        "body": """السلام عليكم [الاسم]،

في شركات [القطاع]، كثير من العروض تُرسل لكن لا تُتابع. الصفقات تموت بصمت.

Dealix يكشف الصفقات المتعثرة ويبني نظام متابعة وإغلاق واضح:
• Revenue Leakage Map
• Follow-up Gap Analysis
• Executive War Room

نبدأ بـ Sprint 5 أيام.

هل لديكم 15 دقيقة هذا الأسبوع؟

مع التحية،
[اسمك]"""
    }
}

def read_prospects():
    """Read prospects from CSV"""
    prospects = []
    if PROSPECTS_FILE.exists():
        with open(PROSPECTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['score'] = int(row.get('score', 0) or 0)
                except:
                    row['score'] = 0
                prospects.append(row)
    return prospects

def read_existing_queue():
    """Read existing outreach queue"""
    if OUTREACH_FILE.exists():
        with open(OUTREACH_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"messages": []}

def read_approval_queue():
    """Read approval queue"""
    if APPROVAL_FILE.exists():
        with open(APPROVAL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def log_action(company, action_type, risk="low"):
    """Log action to AI action ledger"""
    now = datetime.now(SA_TZ)
    entry = {
        "time": now.isoformat(),
        "agent": "outreach_draft_agent",
        "action": action_type,
        "company": company,
        "risk": risk,
        "requires_approval": True,
        "approved": False
    }
    with open(LEDGER_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def generate_outreach(limit=10):
    """Generate outreach messages for top prospects"""
    prospects = read_prospects()
    existing_queue = read_existing_queue()
    approval_queue = read_approval_queue()
    
    # Sort by score descending
    top_prospects = sorted(prospects, key=lambda x: x.get('score', 0), reverse=True)[:limit]
    
    messages = []
    new_approvals = []
    
    now = datetime.now(SA_TZ)
    
    for i, prospect in enumerate(top_prospects, 1):
        segment = prospect.get('segment', 'B2B Services')
        company = prospect.get('company', '')
        pain = prospect.get('pain', '')
        
        # Get template for segment
        template = TEMPLATES.get(segment, TEMPLATES['B2B Services'])
        
        # Customize message
        body = template['body']
        body = body.replace('[الاسم]', 'المسؤول')  # Placeholder
        body = body.replace('[القطاع]', segment)
        
        # Add pain point context if available
        if pain:
            body = body.replace('[المشكلة]', pain)
        
        msg_id = f"OUT-{i:03d}"
        
        message = {
            "id": msg_id,
            "prospect": company,
            "segment": segment,
            "channel": "email",
            "priority": prospect.get('score', 5),
            "draft": body,
            "requires_approval": True,
            "approved": False,
            "risk": "low"
        }
        messages.append(message)
        
        # Add to approval queue
        approval = {
            "id": f"APP-{len(approval_queue) + i:03d}",
            "type": "outreach_message",
            "company": company,
            "risk": "low",
            "draft": body[:100] + "...",
            "requires_approval": True,
            "approved": False,
            "created_at": now.strftime('%Y-%m-%d')
        }
        new_approvals.append(approval)
        
        # Log to ledger
        log_action(company, "created_outreach_draft", "low")
    
    # Update outreach queue
    queue_data = {
        "queue_id": f"OUT-{now.strftime('%Y-%m-%d')}-001",
        "generated_at": now.isoformat(),
        "total_messages": len(messages),
        "status": "pending_approval",
        "messages": messages
    }
    
    OUTREACH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTREACH_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue_data, f, ensure_ascii=False, indent=2)
    
    # Update approval queue
    approval_queue.extend(new_approvals)
    with open(APPROVAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(approval_queue, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(messages)} outreach messages")
    print(f"Added {len(new_approvals)} items to approval queue")
    print(f"Queue saved to: {OUTREACH_FILE}")
    print(f"\nTop {limit} prospects targeted:")
    for m in messages:
        print(f"  - {m['prospect']} ({m['segment']}) - Priority: {m['priority']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate outreach queue for Dealix')
    parser.add_argument('--limit', type=int, default=10, help='Number of prospects to target')
    args = parser.parse_args()
    
    generate_outreach(args.limit)
