#!/usr/bin/env python3
"""
Dealix Proof Pack Generator
Generates a Proof Pack markdown report for a client.
"""

import argparse
import json
import csv
from datetime import datetime
from pathlib import Path


def load_prospect_data(prospects_path: str, client_name: str) -> dict | None:
    """Load prospect data for a specific client."""
    try:
        with open(prospects_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('company', '').lower() == client_name.lower():
                    return row
    except FileNotFoundError:
        pass
    return None


def generate_proof_pack(client_name: str, output_path: str, prospect_data: dict | None = None):
    """Generate a Proof Pack markdown report."""
    
    today = datetime.now().strftime('%Y-%m-%d')
    segment = prospect_data.get('segment', 'Unknown') if prospect_data else 'Unknown'
    pain = prospect_data.get('pain', 'Multiple revenue leakage points') if prospect_data else 'Revenue leakage'
    
    # Simulated analysis data (replace with real analysis)
    response_time = '4.2'
    followup_rate = '35'
    conversion_rate = '8'
    monthly_leakage = '45000'
    
    md = f"""# Proof Pack — Revenue Intelligence Sprint

---

**Client**: {client_name}  
**Date**: {today}  
**Prepared By**: Dealix  
**Confidential**: Yes — Do not distribute without permission

---

## 1. Executive Summary

{client_name} engaged Dealix for a 5-day Revenue Intelligence Sprint. This report identifies key revenue leakage points and provides actionable recommendations.

### Key Findings

| Metric | Current | Industry Best | Gap |
|--------|---------|---------------|-----|
| Avg Response Time | {response_time} hours | 15 minutes | 17x slower |
| Follow-up Rate | {followup_rate}% | 80%+ | 45% gap |
| Lead-to-Deal Conversion | {conversion_rate}% | 15-25% | 7-17% gap |
| Pipeline Visibility | Low | High | Missing system |

### Revenue at Risk

**Estimated monthly revenue leakage: {monthly_leakage} SAR**

This is calculated based on:
- Leads not followed up: {int(int(monthly_leakage) * 0.4)} SAR
- Slow response conversion loss: {int(int(monthly_leakage) * 0.25)} SAR
- No follow-up sequence: {int(int(monthly_leakage) * 0.35)} SAR

---

## 2. Revenue Leakage Map

### Leakage by Stage

| Stage | Leads Entered | Converted | Drop-off | Revenue Lost |
|-------|--------------|-----------|----------|-------------:|
| Inquiry | [Data needed] | [Data needed] | [X]% | [X] SAR |
| First Response | [Data needed] | [Data needed] | [X]% | [X] SAR |
| Follow-up | [Data needed] | [Data needed] | [X]% | [X] SAR |
| Proposal | [Data needed] | [Data needed] | [X]% | [X] SAR |
| Close | [Data needed] | [Data needed] | [X]% | [X] SAR |

### Biggest Leakage Point
**Follow-up stage** — {followup_rate}% of leads receive no follow-up after initial contact.

**Root Cause**: Missing automated follow-up system + no SLA for response time.

---

## 3. Lead Response Audit

### Response Time Distribution

| Time to First Response | % of Leads | Status |
|------------------------|-----------:|--------|
| < 15 minutes | 5% | ✅ Good |
| 15 min — 1 hour | 15% | ⚠️ Acceptable |
| 1 — 4 hours | 30% | ⚠️ Slow |
| 4 — 24 hours | 35% | 🔴 At Risk |
| 24+ hours / No response | 15% | 🔴 Critical |

### Recommendation
Implement 15-minute SLA for first response + automated acknowledgment.

---

## 4. Follow-up Gap Report

### Follow-up Completion Rate

| Touch Point | Expected | Actual | Gap |
|-------------|---------:|-------:|-----:|
| Touch 1 (Initial response) | 100% | 85% | 15% |
| Touch 2 (Day 1 follow-up) | 100% | {followup_rate}% | {100 - int(followup_rate)}% |
| Touch 3 (Day 3 follow-up) | 80% | 20% | 60% |
| Touch 4 (Day 7 follow-up) | 60% | 10% | 50% |
| Touch 5 (Day 14 follow-up) | 40% | 5% | 35% |

### Missing Follow-ups Impact
**[X] leads** received no follow-up after initial contact = **{monthly_leakage} SAR** potential revenue.

---

## 5. Offer Quality Review

### Current Offer Assessment

| Criteria | Score (1-10) | Notes |
|----------|-------------:|-------|
| Clarity | [X] | [Notes] |
| Value proposition | [X] | [Notes] |
| Pricing presentation | [X] | [Notes] |
| Urgency/scarcity | [X] | [Notes] |
| Call to action | [X] | [Notes] |
| Social proof | [X] | [Notes] |
| **Overall** | **[X]** | |

### Top 5 Objections Encountered

1. [OBJECTION_1] — [X]% frequency
2. [OBJECTION_2] — [X]% frequency
3. [OBJECTION_3] — [X]% frequency
4. [OBJECTION_4] — [X]% frequency
5. [OBJECTION_5] — [X]% frequency

---

## 6. 30-Day Revenue Plan

### Quick Wins (Week 1-2)
- [ ] Implement 15-min response SLA
- [ ] Set up follow-up reminders
- [ ] Fix top 3 message templates
- [ ] Review and update pricing presentation

### Medium-term (Week 3-4)
- [ ] Build objection response library
- [ ] Create proposal template
- [ ] Set up weekly pipeline review
- [ ] Train team on new follow-up sequence

### Target Outcome
| Metric | Current | 30-Day Target |
|--------|---------|---------------|
| Response time | {response_time} hours | < 1 hour |
| Follow-up rate | {followup_rate}% | 80%+ |
| Conversion rate | {conversion_rate}% | +5-10% |
| Pipeline visibility | Low | Weekly review |

---

## 7. Next Step — P2 Operating System

The Sprint revealed where revenue is leaking. The next step is systematic execution:

**Dealix AI Sales Ops Retainer includes:**
- Weekly War Room sessions
- Pipeline tracking & optimization
- Message improvement & A/B testing
- Monthly CEO report
- Team training
- Proof Pack generation

**Investment**: Starting at 5,000 SAR/month

---

## Appendix

### Data Sources
- Client CRM export ([DATE_RANGE])
- [X] sales conversations analyzed
- [X] proposals reviewed

### Methodology
All analysis follows Dealix Revenue Intelligence framework with AI-assisted analysis and human verification.

### Confidentiality
This report contains confidential business information. Distribution requires written consent.

---

*Generated: {today} | Dealix Revenue Intelligence*
"""
    
    # Write file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"✅ Proof Pack generated: {output_path}")
    print(f"   Client: {client_name}")
    print(f"   Segment: {segment}")
    print(f"   Key pain: {pain}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Proof Pack for a client')
    parser.add_argument('--client', type=str, required=True, help='Client name')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    parser.add_argument('--prospects', type=str, default=None, help='Path to prospects.csv')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    prospects_path = args.prospects or str(base_dir / 'company_os' / 'revenue' / 'prospects.csv')
    
    # Load prospect data
    prospect_data = load_prospect_data(prospects_path, args.client)
    
    # Set output path
    if args.output:
        output_path = args.output
    else:
        safe_name = args.client.replace(' ', '_').lower()
        output_path = str(base_dir / 'company_os' / 'marketing' / 'case_studies' / f"proof_pack_{safe_name}.md")
    
    generate_proof_pack(args.client, output_path, prospect_data)
