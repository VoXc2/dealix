#!/usr/bin/env python3
"""
Dealix Outreach Queue Generator
Generates personalized outreach messages and adds them to the approval queue.
"""

import argparse
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path


# Outreach message templates by segment
TEMPLATES = {
    'Marketing Agency': {
        'subject': 'وين تضيع فرص عملائك؟',
        'body_template': """السلام عليكم {name}،
لاحظت أن كثير من وكالات التسويق تخسر فرصاً ليس بسبب قلة الطلب، بل بسبب بطء المتابعة وعدم وضوح pipeline.
نحن في Dealix نسوي Revenue Intelligence Sprint خلال 5 أيام:
نكشف أين تضيع الفرص، نحلل المتابعة والعروض، ونطلع لكم Proof Pack وخطة 30 يوم لتحسين التحويل.
هل يناسبك أرسل لك مثال مختصر على التقرير؟"""
    },
    'Training Company': {
        'subject': 'فرص التسجيل اللي تروح واتساب',
        'body_template': """السلام عليكم {name}،
شركات التدريب اللي نشتغل معاها تكتشف أن 40-60% من استفسارات واتساب ما تتحول لتسجيلات بسبب بطء الرد أو غياب المتابعة.
نسوي Sprint 5 أيام نحلل فيه استفساراتك ونكشف أين التسريب ونبني نظام متابعة.
تهمني تجربة وكالة تدريب؟"""
    },
    'B2B Services': {
        'subject': 'صفقات B2B تاخذ وقت أطول من اللازم؟',
        'body_template': """السلام عليكم {name}،
شركات الاستشارات B2B في السعودية تواجه تحدي إغلاق الصفقات بسرعة.
Dealix يسوي Sprint يكشف أين تتعطل صفقاتك:
- سرعة الرد على العملاء
- جودة المتابعات
- قوة العروض
- أكثر الاعتراضات تكراراً
نقدم خطة تشغيل واضحة.
نقدر نتواصل؟"""
    }
}


def load_prospects(filepath: str) -> list[dict]:
    """Load prospects from CSV."""
    prospects = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prospects.append(row)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found.")
    return prospects


def generate_outreach(prospect: dict, seq_id: int) -> dict:
    """Generate personalized outreach for a prospect."""
    segment = prospect.get('segment', 'B2B Services')
    template = TEMPLATES.get(segment, TEMPLATES['B2B Services'])
    
    decision_maker = prospect.get('decision_maker', 'مدير')
    company = prospect.get('company', '')
    pain = prospect.get('pain', '')
    
    # Personalize body
    body = template['body_template'].format(name=decision_maker.split('/')[0].strip())
    
    # Add pain-specific hook if available
    if pain and 'lost' in pain.lower():
        body = body.replace('السلام عليكم', f"السلام عليكم {decision_maker.split('/')[0].strip()}،\n\nوصلني أن {company} تستقبل استفسارات كثيرة لكن {pain}.")
    
    return {
        "id": f"OUT-{seq_id:03d}",
        "company": company,
        "decision_maker": decision_maker,
        "pain": pain,
        "draft_subject": template['subject'],
        "draft_body": body,
        "status": "pending_approval",
        "priority": min(int(prospect.get('score', 5)), 3),
        "created_at": datetime.now().strftime('%Y-%m-%d'),
        "scheduled_for": (datetime.now() + timedelta(days=0)).strftime('%Y-%m-%d')
    }


def load_approval_queue(filepath: str) -> list[dict]:
    """Load existing approval queue."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_approval_queue(queue: list[dict], filepath: str):
    """Save approval queue to JSON."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def generate_outreach_queue(prospects_path: str, approval_queue_path: str, limit: int = 10):
    """Generate outreach queue for top prospects."""
    
    prospects = load_prospects(prospects_path)
    queue = load_approval_queue(approval_queue_path)
    
    # Sort by score and take top N
    scored = []
    for p in prospects:
        try:
            score = int(p.get('score', 0))
        except ValueError:
            score = 0
        scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Filter prospects not yet in queue
    queued_companies = {item.get('company') for item in queue}
    new_items = []
    seq_start = len(queue) + 1
    
    for i, (_, prospect) in enumerate(scored[:limit]):
        if prospect.get('company') not in queued_companies:
            outreach = generate_outreach(prospect, seq_start + len(new_items))
            new_items.append(outreach)
    
    # Add to queue
    queue.extend(new_items)
    save_approval_queue(queue, approval_queue_path)
    
    print(f"✅ Generated {len(new_items)} outreach messages")
    print(f"   Total in approval queue: {len(queue)}")
    for item in new_items:
        print(f"   - {item['company']}: {item['draft_subject']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate outreach queue for Dealix')
    parser.add_argument('--limit', type=int, default=10, help='Number of prospects to process')
    parser.add_argument('--prospects', type=str, default=None, help='Path to prospects.csv')
    parser.add_argument('--output', type=str, default=None, help='Path to approval_queue.json')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    prospects_path = args.prospects or str(base_dir / 'company_os' / 'revenue' / 'prospects.csv')
    approval_queue_path = args.output or str(base_dir / 'company_os' / 'governance' / 'approval_queue.json')
    
    generate_outreach_queue(prospects_path, approval_queue_path, args.limit)
