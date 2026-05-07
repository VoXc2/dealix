#!/usr/bin/env python3
"""Wave 8 §11 — Customer Signal Synthesis.

Reads feature_requests.jsonl files from all active customers
(gitignored data/customers/**) and synthesizes a prioritized signal
report for the founder.

Output: JSON summary of top feature requests + customer signal patterns.
Never reads or logs PII — only feature request text and metadata.

Usage:
    py scripts/dealix_customer_signal_synthesis.py
    py scripts/dealix_customer_signal_synthesis.py --output-json signals.json
    py scripts/dealix_customer_signal_synthesis.py --customer-handle acme-co
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CUSTOMERS_DIR = REPO_ROOT / "data" / "customers"

# Category keywords for signal classification (Arabic + English)
SIGNAL_CATEGORIES = {
    "crm_integration":    ["crm", "hubspot", "salesforce", "zoho", "pipeline", "CRM"],
    "reporting":          ["report", "analytics", "dashboard", "تقرير", "إحصاء", "لوحة"],
    "whatsapp_automation":["whatsapp", "واتساب", "automation", "auto", "تلقائي"],
    "calendar_booking":   ["calendly", "calendar", "booking", "موعد", "حجز"],
    "payment":            ["moyasar", "payment", "invoice", "فاتورة", "دفع"],
    "email":              ["email", "gmail", "إيميل", "بريد"],
    "lead_management":    ["lead", "leads", "prospect", "عميل", "عملاء"],
    "other":              [],
}


def classify_request(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in SIGNAL_CATEGORIES.items():
        if any(kw.lower() in text_lower for kw in keywords):
            return category
    return "other"


def load_customer_signals(customer_dir: Path) -> list[dict]:
    """Load feature requests from a customer's JSONL file."""
    fr_path = customer_dir / "feature_requests.jsonl"
    if not fr_path.exists():
        return []
    signals = []
    for line in fr_path.read_text(encoding="utf-8").strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            signals.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return signals


def synthesize_signals(customer_handle: str | None = None) -> dict:
    """Synthesize all customer signals into a report."""
    all_signals = []

    if not CUSTOMERS_DIR.exists():
        return {
            "status": "insufficient_data",
            "message": "No customer data directory found (data/customers/). No customers onboarded yet.",
            "signals": [],
            "category_counts": {},
            "top_requests": [],
            "customer_count": 0,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    # Collect signals from all customers or specific customer
    dirs_to_scan = []
    if customer_handle:
        handle_dir = CUSTOMERS_DIR / customer_handle
        if handle_dir.exists():
            dirs_to_scan = [handle_dir]
        else:
            return {
                "status": "insufficient_data",
                "message": f"Customer '{customer_handle}' not found in data/customers/",
                "signals": [],
                "category_counts": {},
                "top_requests": [],
                "customer_count": 0,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
    else:
        dirs_to_scan = [d for d in CUSTOMERS_DIR.iterdir() if d.is_dir()]

    for customer_dir in dirs_to_scan:
        signals = load_customer_signals(customer_dir)
        for s in signals:
            s["_customer_dir"] = customer_dir.name
            s["_category"] = classify_request(s.get("request_text", ""))
        all_signals.extend(signals)

    # Count by category
    category_counts = Counter(s["_category"] for s in all_signals)

    # Top request texts (de-duplicated by similarity — simple exact match here)
    seen_texts: set[str] = set()
    top_requests = []
    for sig in sorted(all_signals, key=lambda s: s.get("logged_at", ""), reverse=True):
        text = sig.get("request_text", "").strip()
        if text and text not in seen_texts:
            seen_texts.add(text)
            top_requests.append({
                "text": text,
                "category": sig.get("_category", "other"),
                "wave_logged": sig.get("wave_logged", ""),
                "logged_at": sig.get("logged_at", ""),
            })
        if len(top_requests) >= 20:
            break

    return {
        "status": "ok",
        "customer_count": len(dirs_to_scan),
        "total_signals": len(all_signals),
        "category_counts": dict(category_counts),
        "top_requests": top_requests,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Customer PII not included. Feature request text only.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Customer Signal Synthesis")
    parser.add_argument("--customer-handle", default=None, help="Filter to specific customer")
    parser.add_argument("--output-json", default=None, help="Write JSON output to file")
    args = parser.parse_args()

    report = synthesize_signals(customer_handle=args.customer_handle)

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Signal synthesis written to {out_path}")
        return 0

    print("\n=== Customer Signal Synthesis ===\n")
    print(f"Status:         {report['status']}")
    print(f"Customers:      {report.get('customer_count', 0)}")
    print(f"Total signals:  {report.get('total_signals', 0)}")
    print(f"Generated at:   {report.get('generated_at', '')}")

    if report["status"] == "insufficient_data":
        print(f"\nℹ️  {report['message']}")
        return 0

    print(f"\nCategory breakdown:")
    for cat, count in sorted(report.get("category_counts", {}).items(), key=lambda x: -x[1]):
        print(f"  {cat:<25} {count}")

    print(f"\nTop feature requests:")
    for req in report.get("top_requests", [])[:10]:
        print(f"  [{req['category']}] {req['text'][:80]}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
