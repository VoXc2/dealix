#!/usr/bin/env python3
"""
Generate Proof Pack for Dealix Client
Usage: python generate_proof_pack.py --client "Client Name"
"""

import argparse
import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

COMPANY_OS_DIR = Path(__file__).parent.parent
TEMPLATE_FILE = COMPANY_OS_DIR / "delivery" / "proof_pack_template.md"
OUTPUT_DIR = COMPANY_OS_DIR / "delivery" / "proof_packs"
LEDGER_FILE = COMPANY_OS_DIR / "governance" / "ai_action_ledger.jsonl"

SA_TZ = timezone(timedelta(hours=3))

def log_action(client, action_type, risk="low"):
    """Log action to AI action ledger"""
    now = datetime.now(SA_TZ)
    entry = {
        "time": now.isoformat(),
        "agent": "proof_generator",
        "action": action_type,
        "client": client,
        "risk": risk,
        "requires_approval": True,
        "approved": False
    }
    with open(LEDGER_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def generate_proof_pack(client_name, segment="General"):
    """Generate a Proof Pack for a client"""
    now = datetime.now(SA_TZ)
    start_date = now.strftime('%Y-%m-%d')
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"PROOF_PACK_{client_name.replace(' ', '_')}_{start_date}.md"
    
    # Read template
    template = ""
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
    
    # Fill in client details
    report = template.replace('{CLIENT_NAME}', client_name)
    report = report.replace('{SEGMENT}', segment)
    report = report.replace('{INDUSTRY}', segment)
    report = report.replace('{START_DATE}', start_date)
    report = report.replace('{END_DATE}', start_date)  # Would calculate +5 days
    report = report.replace('{DATE}', start_date)
    
    # Add sample data for demonstration
    report = report.replace('{NUMBER}', '127')
    report = report.replace('{AMOUNT}', '45,000')
    report = report.replace('{X}%', '23%')
    report = report.replace('{X}', '23')
    report = report.replace('{ESTIMATE}', '35,000-50,000')
    report = report.replace('{HOURS}', '15-20')
    
    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Log action
    log_action(client_name, "generated_proof_pack")
    
    print(f"Proof Pack generated: {output_file}")
    print(f"Client: {client_name}")
    print(f"Segment: {segment}")
    print(f"\nNote: This is a template. Fill in actual analysis data from client intake.")
    print(f"Remember: All claims must have supporting evidence!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Proof Pack for Dealix client')
    parser.add_argument('--client', type=str, required=True, help='Client name')
    parser.add_argument('--segment', type=str, default='General', 
                       choices=['Marketing Agency', 'Training', 'B2B Services', 'General'],
                       help='Client segment')
    args = parser.parse_args()
    
    generate_proof_pack(args.client, args.segment)
