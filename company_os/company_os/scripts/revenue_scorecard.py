#!/usr/bin/env python3
"""
Revenue Scorecard for Dealix
Tracks KPIs: outreach, replies, meetings, proposals, payments, delivery, proof events
"""

import csv
import json
from datetime import datetime, timezone, timedelta, date
from pathlib import Path
from collections import defaultdict

COMPANY_OS_DIR = Path(__file__).parent.parent
SCORECARD_FILE = COMPANY_OS_DIR / "finance" / "revenue_scorecard.csv"
OUTREACH_FILE = COMPANY_OS_DIR / "revenue" / "outreach_queue.json"
PROPOSALS_FILE = COMPANY_OS_DIR / "revenue" / "proposals.json"
FOLLOWUPS_FILE = COMPANY_OS_DIR / "revenue" / "followups.json"
PAYMENTS_FILE = COMPANY_OS_DIR / "revenue" / "payments.csv"
PROSPECTS_FILE = COMPANY_OS_DIR / "revenue" / "prospects.csv"
LEDGER_FILE = COMPANY_OS_DIR / "governance" / "ai_action_ledger.jsonl"

SA_TZ = timezone(timedelta(hours=3))

def read_scorecard():
    """Read existing scorecard data"""
    entries = []
    if SCORECARD_FILE.exists():
        with open(SCORECARD_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
    return entries

def count_outreach():
    """Count outreach messages sent"""
    if OUTREACH_FILE.exists():
        with open(OUTREACH_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len([m for m in data.get("messages", []) if m.get("approved")])
    return 0

def count_replies():
    """Count replies received"""
    # Placeholder - would integrate with email/WhatsApp API
    return 0

def count_meetings():
    """Count discovery meetings booked"""
    if PROPOSALS_FILE.exists():
        with open(PROPOSALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len([p for p in data.get("proposals", []) if p.get("status") == "sent"])
    return 0

def count_proposals_sent():
    """Count proposals sent"""
    if PROPOSALS_FILE.exists():
        with open(PROPOSALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len([p for p in data.get("proposals", []) if p.get("status") in ["sent", "pending_approval"]])
    return 0

def count_proposals_won():
    """Count proposals won"""
    if PROPOSALS_FILE.exists():
        with open(PROPOSALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len([p for p in data.get("proposals", []) if p.get("status") == "won"])
    return 0

def sum_revenue():
    """Sum revenue collected"""
    total = 0
    if PAYMENTS_FILE.exists():
        with open(PAYMENTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if row.get('status') == 'Received':
                        total += int(row.get('amount_sar', 0) or 0)
                except:
                    pass
    return total

def count_delivery_hours():
    """Count delivery hours this month"""
    # Placeholder - would track from time logs
    return 0

def calculate_mrr():
    """Calculate Monthly Recurring Revenue"""
    mrr = 0
    if PAYMENTS_FILE.exists():
        with open(PAYMENTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Retainer payments count toward MRR
                    if 'Retainer' in (row.get('notes', '') or ''):
                        mrr += int(row.get('amount_sar', 0) or 0)
                except:
                    pass
    return mrr

def count_proof_events():
    """Count proof events this week"""
    if LEDGER_FILE.exists():
        count = 0
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("action") == "generated_case_insight":
                        count += 1
                except:
                    pass
        return count
    return 0

def count_governance_checks():
    """Count governance checks"""
    if LEDGER_FILE.exists():
        count = 0
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("agent") == "governance_monitor":
                        count += 1
                except:
                    pass
        return count
    return 0

def generate_scorecard():
    """Generate today's scorecard entry"""
    today = date.today().isoformat()
    
    metrics = {
        'date': today,
        'prospects_added': 0,  # Would track daily additions
        'outreach_sent': count_outreach(),
        'replies_received': count_replies(),
        'calls_booked': count_meetings(),
        'proposals_sent': count_proposals_sent(),
        'proposals_won': count_proposals_won(),
        'revenue_collected': sum_revenue(),
        'delivery_hours': count_delivery_hours(),
        'mrr': calculate_mrr(),
        'proof_events': count_proof_events(),
        'governance_checks': count_governance_checks(),
        'notes': 'Auto-generated'
    }
    
    # Read existing entries
    entries = read_scorecard()
    
    # Check if entry for today exists
    today_exists = False
    for entry in entries:
        if entry.get('date') == today:
            today_exists = True
            entry.update(metrics)
            break
    
    if not today_exists:
        entries.append(metrics)
    
    # Write updated scorecard
    fieldnames = ['date', 'prospects_added', 'outreach_sent', 'replies_received', 
                  'calls_booked', 'proposals_sent', 'proposals_won', 
                  'revenue_collected', 'delivery_hours', 'mrr', 
                  'proof_events', 'governance_checks', 'notes']
    
    SCORECARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCORECARD_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    
    # Print summary
    print("=" * 60)
    print("DEALIX REVENUE SCORECARD")
    print(f"Date: {today}")
    print("=" * 60)
    print(f"Outreach Sent:      {metrics['outreach_sent']}")
    print(f"Replies Received:   {metrics['replies_received']}")
    print(f"Meetings Booked:    {metrics['calls_booked']}")
    print(f"Proposals Sent:     {metrics['proposals_sent']}")
    print(f"Proposals Won:      {metrics['proposals_won']}")
    print(f"Revenue Collected:  {metrics['revenue_collected']:,} SAR")
    print(f"Delivery Hours:     {metrics['delivery_hours']}")
    print(f"MRR:                {metrics['mrr']:,} SAR")
    print(f"Proof Events:       {metrics['proof_events']}")
    print(f"Governance Checks:  {metrics['governance_checks']}")
    print("=" * 60)
    
    # Calculate conversion rates
    if metrics['outreach_sent'] > 0:
        reply_rate = (metrics['replies_received'] / metrics['outreach_sent']) * 100
        print(f"Reply Rate:         {reply_rate:.1f}%")
    
    if metrics['replies_received'] > 0:
        meeting_rate = (metrics['calls_booked'] / metrics['replies_received']) * 100
        print(f"Meeting Rate:       {meeting_rate:.1f}%")
    
    if metrics['proposals_sent'] > 0:
        win_rate = (metrics['proposals_won'] / metrics['proposals_sent']) * 100
        print(f"Win Rate:           {win_rate:.1f}%")
    
    print(f"\nScorecard saved to: {SCORECARD_FILE}")

if __name__ == "__main__":
    generate_scorecard()
