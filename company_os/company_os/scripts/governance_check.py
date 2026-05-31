#!/usr/bin/env python3
"""
Governance Check for Dealix
Checks: secrets, claims, unauthorized sends, sensitive data, AI action logging
"""

import csv
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

COMPANY_OS_DIR = Path(__file__).parent.parent
LEDGER_FILE = COMPANY_OS_DIR / "governance" / "ai_action_ledger.jsonl"
APPROVAL_FILE = COMPANY_OS_DIR / "governance" / "approval_queue.json"
DATA_CHECKLIST_FILE = COMPANY_OS_DIR / "governance" / "data_handling_checklist.md"
SECRETS_PATTERN = re.compile(r'(ghp_|ghu_|RAILWAY_TOKEN|sk-|OPENAI_API_KEY|OPENROUTER|DEEPSEEK)', re.IGNORECASE)
SENSITIVE_PATTERN = re.compile(r'(\b\d{10}\b|\b\d{2}/\d{2}/\d{4}\b|\b[A-Z]{2}-\d{4}\b)', re.IGNORECASE)
CLAIM_PATTERN = re.compile(r'(ضعف|ضعيف|أفضل|أسوأ|ممتاز|سيء)', re.IGNORECASE)

SA_TZ = timezone(timedelta(hours=3))

def check_secrets():
    """Check for exposed secrets in repository"""
    issues = []
    repo_dir = COMPANY_OS_DIR.parent
    
    for file_path in repo_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.json', '.env', '.md', '.csv']:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                matches = SECRETS_PATTERN.findall(content)
                if matches:
                    issues.append({
                        'file': str(file_path.relative_to(repo_dir)),
                        'type': 'secret_exposed',
                        'details': f'Found potential secrets: {matches}',
                        'severity': 'critical'
                    })
            except:
                pass
    
    return issues

def check_approval_queue():
    """Check for unapproved actions"""
    issues = []
    
    if APPROVAL_FILE.exists():
        with open(APPROVAL_FILE, 'r', encoding='utf-8') as f:
            approvals = json.load(f)
        
        unapproved = [a for a in approvals if not a.get('approved', False)]
        
        for item in unapproved:
            if item.get('type') == 'outreach_message':
                issues.append({
                    'file': 'approval_queue.json',
                    'type': 'unapproved_outreach',
                    'details': f"Unapproved outreach to {item.get('company', 'unknown')}: {item.get('id', '')}",
                    'severity': 'medium'
                })
            elif item.get('type') == 'proposal_pricing':
                issues.append({
                    'file': 'approval_queue.json',
                    'type': 'unapproved_proposal',
                    'details': f"Unapproved proposal for {item.get('company', 'unknown')}: {item.get('id', '')}",
                    'severity': 'medium'
                })
    
    return issues

def check_sensitive_data():
    """Check for sensitive data in prompts/outputs"""
    issues = []
    
    # Check outreach messages for sensitive data
    outreach_file = COMPANY_OS_DIR / "revenue" / "outreach_queue.json"
    if outreach_file.exists():
        with open(outreach_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for msg in data.get("messages", []):
            draft = msg.get("draft", "")
            # Check for phone numbers, IDs, etc.
            if re.search(r'\b05\d{8}\b', draft):
                issues.append({
                    'file': 'outreach_queue.json',
                    'type': 'sensitive_data_in_prompt',
                    'details': f"Message {msg.get('id', '')} contains potential phone number",
                    'severity': 'high'
                })
            
            # Check for real names
            if re.search(r'[أ-ي]{3,}\s+[أ-ي]{3,}', draft) and '[الاسم]' not in draft:
                issues.append({
                    'file': 'outreach_queue.json',
                    'type': 'real_name_in_prompt',
                    'details': f"Message {msg.get('id', '')} may contain real name instead of placeholder",
                    'severity': 'medium'
                })
    
    return issues

def check_ai_ledger():
    """Check if all AI actions are logged"""
    issues = []
    
    if not LEDGER_FILE.exists():
        issues.append({
            'file': 'ai_action_ledger.jsonl',
            'type': 'missing_ledger',
            'details': 'AI action ledger file not found',
            'severity': 'critical'
        })
        return issues
    
    # Check ledger has entries
    entry_count = 0
    with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entry_count += 1
                try:
                    entry = json.loads(line)
                    required_fields = ['time', 'agent', 'action', 'risk', 'requires_approval', 'approved']
                    for field in required_fields:
                        if field not in entry:
                            issues.append({
                                'file': 'ai_action_ledger.jsonl',
                                'type': 'incomplete_log_entry',
                                'details': f"Entry missing required field: {field}",
                                'severity': 'medium'
                            })
                except json.JSONDecodeError:
                    issues.append({
                        'file': 'ai_action_ledger.jsonl',
                        'type': 'malformed_log_entry',
                        'details': f"Invalid JSON at line {entry_count}",
                        'severity': 'medium'
                    })
    
    if entry_count == 0:
        issues.append({
            'file': 'ai_action_ledger.jsonl',
            'type': 'empty_ledger',
            'details': 'AI action ledger is empty',
            'severity': 'high'
        })
    
    return issues

def check_claims():
    """Check for unsubstantiated claims"""
    issues = []
    
    # Check proposals for exaggerated claims
    proposals_file = COMPANY_OS_DIR / "revenue" / "proposals.json"
    if proposals_file.exists():
        with open(proposals_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for prop in data.get("proposals", []):
            # Check for claims without backing
            notes = prop.get("notes", "")
            if "guarantee" in notes.lower() or "مضمون" in notes or "مضمونة" in notes:
                issues.append({
                    'file': 'proposals.json',
                    'type': 'unsubstantiated_claim',
                    'details': f"Proposal {prop.get('id', '')} contains guarantee language",
                    'severity': 'high'
                })
    
    return issues

def run_governance_check():
    """Run full governance check"""
    now = datetime.now(SA_TZ)
    
    print("=" * 70)
    print("DEALIX GOVERNANCE CHECK")
    print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')} AST")
    print("=" * 70)
    
    all_issues = []
    
    # Check 1: Secrets
    print("\n[1/5] Checking for exposed secrets...")
    secret_issues = check_secrets()
    all_issues.extend(secret_issues)
    if secret_issues:
        print(f"  ✗ Found {len(secret_issues)} potential secret exposures!")
        for issue in secret_issues:
            print(f"    - {issue['file']}: {issue['details'][:80]}")
    else:
        print("  ✓ No secrets detected")
    
    # Check 2: Approval Queue
    print("\n[2/5] Checking approval queue...")
    approval_issues = check_approval_queue()
    all_issues.extend(approval_issues)
    if approval_issues:
        print(f"  ! Found {len(approval_issues)} unapproved items (expected)")
        for issue in approval_issues:
            print(f"    - {issue['details'][:80]}")
    else:
        print("  ✓ All items approved")
    
    # Check 3: Sensitive Data
    print("\n[3/5] Checking for sensitive data in prompts...")
    sensitive_issues = check_sensitive_data()
    all_issues.extend(sensitive_issues)
    if sensitive_issues:
        print(f"  ✗ Found {len(sensitive_issues)} sensitive data issues!")
        for issue in sensitive_issues:
            print(f"    - {issue['file']}: {issue['details'][:80]}")
    else:
        print("  ✓ No sensitive data detected")
    
    # Check 4: AI Ledger
    print("\n[4/5] Checking AI action ledger...")
    ledger_issues = check_ai_ledger()
    all_issues.extend(ledger_issues)
    if ledger_issues:
        print(f"  ✗ Found {len(ledger_issues)} ledger issues!")
        for issue in ledger_issues:
            print(f"    - {issue['type']}: {issue['details'][:80]}")
    else:
        print("  ✓ AI action ledger is complete")
    
    # Check 5: Claims
    print("\n[5/5] Checking for unsubstantiated claims...")
    claim_issues = check_claims()
    all_issues.extend(claim_issues)
    if claim_issues:
        print(f"  ✗ Found {len(claim_issues)} claim issues!")
        for issue in claim_issues:
            print(f"    - {issue['file']}: {issue['details'][:80]}")
    else:
        print("  ✓ No unsubstantiated claims detected")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    critical = sum(1 for i in all_issues if i['severity'] == 'critical')
    high = sum(1 for i in all_issues if i['severity'] == 'high')
    medium = sum(1 for i in all_issues if i['severity'] == 'medium')
    low = sum(1 for i in all_issues if i['severity'] == 'low')
    
    print(f"Total Issues: {len(all_issues)}")
    print(f"  Critical: {critical}")
    print(f"  High: {high}")
    print(f"  Medium: {medium}")
    print(f"  Low: {low}")
    
    if critical > 0:
        print("\n⚠️  CRITICAL ISSUES FOUND - STOP ALL AI OPERATIONS")
        print("   Notify founder immediately!")
    elif high > 0:
        print("\n⚠️  HIGH SEVERITY ISSUES - REVIEW REQUIRED")
    elif medium > 0:
        print("\nℹ️  Medium issues found - review recommended")
    else:
        print("\n✓ Governance check passed")
    
    print("=" * 70)
    
    # Recommendations
    print("\nRECOMMENDATIONS:")
    if critical == 0 and high == 0:
        print("1. Continue daily War Room reviews")
        print("2. Maintain approval queue discipline")
        print("3. Run this check weekly")
        print("4. Update data handling checklist monthly")
    else:
        print("1. Address all critical/high issues immediately")
        print("2. Review approval queue items")
        print("3. Verify no sensitive data in outputs")
    
    return len(all_issues) == 0

if __name__ == "__main__":
    passed = run_governance_check()
    exit(0 if passed else 1)
