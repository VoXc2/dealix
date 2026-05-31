#!/usr/bin/env python3
"""
Dealix Governance Check
Validates compliance with governance rules and PDPL requirements.
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path


# Critical governance rules
RULES = [
    {
        "id": "G001",
        "name": "No AI sends external messages without approval",
        "check": "approval_queue",
        "severity": "CRITICAL"
    },
    {
        "id": "G002", 
        "name": "No PII in public AI tools",
        "check": "data_handling",
        "severity": "CRITICAL"
    },
    {
        "id": "G003",
        "name": "No AI makes pricing decisions",
        "check": "approval_queue",
        "severity": "CRITICAL"
    },
    {
        "id": "G004",
        "name": "All AI actions logged",
        "check": "ledger",
        "severity": "HIGH"
    },
    {
        "id": "G005",
        "name": "Client data anonymized before AI analysis",
        "check": "data_handling",
        "severity": "HIGH"
    },
    {
        "id": "G006",
        "name": "No unauthorized data deletion",
        "check": "permissions",
        "severity": "CRITICAL"
    },
    {
        "id": "G007",
        "name": "No production secrets modification",
        "check": "permissions",
        "severity": "CRITICAL"
    }
]


def load_approval_queue(filepath: str) -> list[dict]:
    """Load approval queue."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_ledger(filepath: str) -> list[str]:
    """Load JSONL ledger."""
    entries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except FileNotFoundError:
        pass
    return entries


def check_approval_queue(queue: list[dict]) -> list[dict]:
    """Check approval queue for compliance issues."""
    findings = []
    
    for item in queue:
        # Check if unapproved items have sensitive types
        if not item.get('approved', False) and item.get('requires_approval', False):
            item_type = item.get('type', '')
            
            if item_type == 'outreach_message':
                # Check for PII in draft
                draft = item.get('draft_body', '')
                if any(pii in draft for pii in ['@', 'phone', 'موبايل', 'جوال']):
                    findings.append({
                        "rule": "G002",
                        "severity": "CRITICAL",
                        "detail": f"Potential PII in outreach draft for {item.get('company')}",
                        "item_id": item.get('id')
                    })
            
            if item_type == 'pricing_offer':
                findings.append({
                    "rule": "G003",
                    "severity": "CRITICAL",
                    "detail": f"Pricing decision pending approval for {item.get('company')}",
                    "item_id": item.get('id')
                })
    
    return findings


def check_ledger(ledger: list[dict]) -> list[dict]:
    """Check ledger for compliance issues."""
    findings = []
    
    # Check for actions without approval that require it
    for entry in ledger:
        if entry.get('requires_approval') and not entry.get('approved'):
            findings.append({
                "rule": "G001",
                "severity": "CRITICAL",
                "detail": f"Unapproved action: {entry.get('action')} by {entry.get('agent')}",
                "timestamp": entry.get('time')
            })
    
    return findings


def check_data_handling(prospects_path: str) -> list[dict]:
    """Check data handling practices."""
    findings = []
    
    try:
        with open(prospects_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Check for potential PII
                for col in ['decision_maker', 'contact']:
                    if col in row and row[col]:
                        value = row[col]
                        # Simple check for personal names
                        if any(name in value for name in ['أحمد', 'محمد', 'خالد', 'فهد', 'سامي']):
                            findings.append({
                                "rule": "G002",
                                "severity": "HIGH",
                                "detail": f"Potential personal name in prospects row {i+1}: {col}",
                                "item_id": None
                            })
    except FileNotFoundError:
        pass
    
    return findings


def run_governance_check(
    approval_queue_path: str,
    ledger_path: str,
    prospects_path: str
):
    """Run full governance check."""
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 80)
    print(f"  DEALIX GOVERNANCE CHECK — {today}")
    print("=" * 80)
    print()
    
    # Load data
    queue = load_approval_queue(approval_queue_path)
    ledger = load_ledger(ledger_path)
    
    print(f"  Loaded: {len(queue)} approval items, {len(ledger)} ledger entries")
    print()
    
    # Run checks
    all_findings = []
    all_findings.extend(check_approval_queue(queue))
    all_findings.extend(check_ledger(ledger))
    all_findings.extend(check_data_handling(prospects_path))
    
    # Categorize
    critical = [f for f in all_findings if f['severity'] == 'CRITICAL']
    high = [f for f in all_findings if f['severity'] == 'HIGH']
    medium = [f for f in all_findings if f['severity'] == 'MEDIUM']
    
    # Summary
    print(f"  FINDINGS SUMMARY:")
    print(f"  🔴 Critical: {len(critical)}")
    print(f"  🟠 High: {len(high)}")
    print(f"  🟡 Medium: {len(medium)}")
    print()
    
    if critical:
        print("  CRITICAL ISSUES (Must fix immediately):")
        print("  " + "-" * 50)
        for finding in critical:
            print(f"  [{finding['rule']}] {finding['detail']}")
        print()
    
    if high:
        print("  HIGH ISSUES (Fix within 24 hours):")
        print("  " + "-" * 50)
        for finding in high:
            print(f"  [{finding['rule']}] {finding['detail']}")
        print()
    
    # Rules status
    print("  GOVERNANCE RULES STATUS:")
    print("  " + "-" * 50)
    for rule in RULES:
        related_findings = [f for f in all_findings if f['rule'] == rule['id']]
        status = "🔴 VIOLATIONS" if related_findings else "✅ COMPLIANT"
        print(f"  {rule['id']}: {rule['name'][:45]:<45} {status}")
    print()
    
    # Overall status
    if critical:
        print("  OVERALL STATUS: 🔴 NON-COMPLIANT (Critical issues found)")
    elif high:
        print("  OVERALL STATUS: 🟠 AT RISK (High issues found)")
    else:
        print("  OVERALL STATUS: ✅ COMPLIANT")
    print()
    
    print("  " + "=" * 80)
    
    return len(critical) == 0 and len(high) == 0


if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    
    compliant = run_governance_check(
        approval_queue_path=str(base_dir / 'company_os' / 'governance' / 'approval_queue.json'),
        ledger_path=str(base_dir / 'company_os' / 'governance' / 'ai_action_ledger.jsonl'),
        prospects_path=str(base_dir / 'company_os' / 'revenue' / 'prospects.csv')
    )
    
    exit(0 if compliant else 1)
