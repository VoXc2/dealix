#!/usr/bin/env python3
"""
Generate War Room Report for Dealix
Reads prospects, followups, proposals and generates REVENUE_WAR_ROOM_TODAY.md
"""

import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuration
COMPANY_OS_DIR = Path(__file__).parent.parent
OUTPUT_FILE = COMPANY_OS_DIR / "war_room" / "REVENUE_WAR_ROOM_TODAY.md"

# Saudi timezone
SA_TZ = timezone(timedelta(hours=3))

def read_prospects():
    """Read prospects from CSV"""
    prospects_file = COMPANY_OS_DIR / "revenue" / "prospects.csv"
    prospects = []
    if prospects_file.exists():
        with open(prospects_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prospects.append(row)
    return prospects

def read_followups():
    """Read followups from JSON"""
    followups_file = COMPANY_OS_DIR / "revenue" / "followups.json"
    if followups_file.exists():
        with open(followups_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("followups", [])
    return []

def read_proposals():
    """Read proposals from JSON"""
    proposals_file = COMPANY_OS_DIR / "revenue" / "proposals.json"
    if proposals_file.exists():
        with open(proposals_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("proposals", [])
    return []

def read_approval_queue():
    """Read pending approvals"""
    approval_file = COMPANY_OS_DIR / "governance" / "approval_queue.json"
    if approval_file.exists():
        with open(approval_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def generate_war_room():
    """Generate the War Room markdown report"""
    now = datetime.now(SA_TZ)
    prospects = read_prospects()
    followups = read_followups()
    proposals = read_proposals()
    approvals = read_approval_queue()
    
    # Calculate metrics
    total_prospects = len(prospects)
    researched = sum(1 for p in prospects if p.get('status') == 'Researched')
    top_prospects = sorted(
        [p for p in prospects if int(p.get('score', 0) or 0) >= 6],
        key=lambda x: int(x.get('score', 0) or 0),
        reverse=True
    )[:10]
    
    pending_approvals = [a for a in approvals if not a.get('approved', False)]
    pending_followups = [f for f in followups if f.get('status') == 'pending']
    active_proposals = [p for p in proposals if p.get('status') in ['pending_approval', 'sent']]
    
    # Generate report
    report = f"""# Dealix Revenue War Room — Today
Generated: {now.strftime('%Y-%m-%d %H:%M')} AST

## Today's Revenue Target
- Cash target: 5,000 SAR
- Meetings target: 3
- Proposals target: 1

## Pipeline Summary
| Metric | Count |
|---|---|
| Total Prospects | {total_prospects} |
| Researched | {researched} |
| Pending Approvals | {len(pending_approvals)} |
| Pending Follow-ups | {len(pending_followups)} |
| Active Proposals | {len(active_proposals)} |

## Top 10 Prospects
| Company | Segment | Pain | Status | Next Action | Score |
|---|---|---|---|---|---|
"""
    
    for p in top_prospects:
        report += f"| {p.get('company', '')} | {p.get('segment', '')} | {p.get('pain', '')} | {p.get('status', '')} | {p.get('next_action', '')} | {p.get('score', '')} |\n"
    
    report += f"""
## Follow-ups Due
| Company | Last Touch | Draft Message | Deadline |
|---|---|---|---|
"""
    
    for f in pending_followups[:5]:
        report += f"| {f.get('company', '')} | {f.get('last_contact', '')} | {f.get('draft_message', '')[:50]}... | {f.get('next_due', '')} |\n"
    
    report += f"""
## Proposals
| Company | Offer | Value | Status |
|---|---|---:|---|
"""
    
    for p in active_proposals:
        report += f"| {p.get('client', '')} | {p.get('service', '')} | {p.get('value_sar', 0):,} SAR | {p.get('status', '')} |\n"
    
    report += f"""
## Pending Approvals
| ID | Type | Company | Risk | Status |
|---|---|---|---|---|
"""
    
    for a in pending_approvals[:5]:
        report += f"| {a.get('id', '')} | {a.get('type', '')} | {a.get('company', '')} | {a.get('risk', '')} | {'Approved' if a.get('approved') else 'Pending'} |\n"
    
    report += f"""
## Delivery
| Client | Deliverable | Due | Risk |
|---|---|---|---|
| N/A | Awaiting first client | — | Low |

## Proof Events
| Proof | Source | Can Publish? |
|---|---|---|
| Pipeline analysis methodology | Internal research | Yes (anonymized) |

## Founder Decision Queue
| Decision | Risk | Recommendation |
|---|---|---|
| Approve outreach batch (OUT-001 to OUT-010) | Low | Approve and send today |
| Review proposal for مؤسسة استشارات مالية (PROP-001) | Medium | Approve with standard pricing |
| Set weekly War Room review schedule | Low | Every Sunday 9 AM |

## Actions for Today
1. Review and approve pending outreach messages
2. Send follow-ups to top 5 prospects
3. Review proposal APP-002
4. Add 5 new prospects to pipeline
5. Prepare first Proof Pack on sample data
6. Run governance check

---
*Auto-generated by Dealix War Room System*
*Next update: Tomorrow 09:00 AST*
"""
    
    # Write report
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"War Room report generated: {OUTPUT_FILE}")
    print(f"Pipeline: {total_prospects} prospects, {len(pending_followups)} follow-ups due, {len(pending_approvals)} approvals pending")

if __name__ == "__main__":
    generate_war_room()
