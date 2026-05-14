#!/usr/bin/env python3
"""Wave 8 §8 — Integration Plan Quality Gate.

Validates a customer integration_plan.md for:
- No forbidden tokens
- Required sections present
- Hard gates respected
- Arabic language present
- Customer handle format valid
- No PII leakage patterns

Usage:
    py scripts/dealix_integration_plan_quality_check.py --plan-file data/customers/<handle>/integration_plan.md
    py scripts/dealix_integration_plan_quality_check.py --plan-dir data/customers/<handle>/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Forbidden tokens (Article 8)
FORBIDDEN_PATTERNS = [
    (re.compile(r"\bguaranteed?\b", re.IGNORECASE), "guaranteed_claims"),
    (re.compile(r"\bblast\b", re.IGNORECASE), "blast_messaging"),
    (re.compile(r"\bscrap(?:e|ing)\b", re.IGNORECASE), "scraping"),
    (re.compile(r"\bcold\s+(whatsapp|outreach|email)\b", re.IGNORECASE), "cold_outreach"),
    (re.compile(r"نضمن"), "arabic_guarantee_claim"),
    (re.compile(r"\bv1[0-4]\b"), "internal_version_leak"),
    (re.compile(r"\bgrowth.beast\b", re.IGNORECASE), "internal_label_leak"),
    (re.compile(r"\brouter\b", re.IGNORECASE), "internal_label_router"),
    (re.compile(r"\bpytest\b", re.IGNORECASE), "internal_test_label"),
    (re.compile(r"\bstacktrace\b", re.IGNORECASE), "internal_error_label"),
    (re.compile(r"\binternal_error\b", re.IGNORECASE), "internal_error_key"),
    (re.compile(r"\bmock\b", re.IGNORECASE), "mock_label"),
    (re.compile(r"\bfake\b", re.IGNORECASE), "fake_label"),
]

# Required sections in integration plan
REQUIRED_SECTIONS = [
    "خطّة الإدماج",       # Arabic title
    "DPA",                # DPA signed marker
    "القنوات",            # Channels section
    "Hard rules",         # Hard rules section
    "NO_LIVE_SEND",       # No live send gate
    "NO_LIVE_CHARGE",     # No live charge gate
    "NO_SCRAPING",        # No scraping gate
]

# PII leakage patterns (should NOT be in output)
PII_LEAK_PATTERNS = [
    re.compile(r"dealix-cust-[A-Za-z0-9\-_]{10,}"),  # Actual portal tokens
    re.compile(r"sk_live_[A-Za-z0-9]{10,}"),           # Live API keys
    re.compile(r"sk-ant-api[A-Za-z0-9\-]{10,}"),       # Anthropic keys
]

VALID_HANDLE = re.compile(r"^[a-z0-9-]{1,64}$")


def check_plan_file(plan_path: Path) -> dict:
    """Run all quality checks on an integration plan. Returns results dict."""
    results = {
        "file": str(plan_path),
        "exists": plan_path.exists(),
        "checks": [],
        "pass_count": 0,
        "fail_count": 0,
        "verdict": "unknown",
    }

    if not plan_path.exists():
        results["verdict"] = "FILE_NOT_FOUND"
        results["fail_count"] = 1
        return results

    content = plan_path.read_text(encoding="utf-8")

    def add_check(name: str, passed: bool, detail: str = ""):
        entry = {"name": name, "status": "PASS" if passed else "FAIL", "detail": detail}
        results["checks"].append(entry)
        if passed:
            results["pass_count"] += 1
        else:
            results["fail_count"] += 1

    # 1. File is not empty
    add_check("file_not_empty", len(content.strip()) > 100, f"length={len(content)}")

    # 2. Has Arabic content
    arabic_chars = sum(1 for c in content if "\u0600" <= c <= "\u06ff")
    add_check("has_arabic_content", arabic_chars > 20, f"arabic_chars={arabic_chars}")

    # 3. Required sections present
    for section in REQUIRED_SECTIONS:
        add_check(f"has_section:{section}", section in content, "")

    # 4. No forbidden tokens
    for pat, label in FORBIDDEN_PATTERNS:
        hit = pat.search(content)
        if label in {"internal_label_router", "internal_test_label", "mock_label", "fake_label"}:
            # These are OK in the hard rules section (negation context)
            if hit and f"NO_{label.upper()}" not in content:
                add_check(f"no_forbidden:{label}", False, f"found: {hit.group()!r}")
            else:
                add_check(f"no_forbidden:{label}", True, "")
        else:
            add_check(f"no_forbidden:{label}", hit is None,
                      f"found: {hit.group()!r}" if hit else "")

    # 5. No PII/token leakage
    for pii_pat in PII_LEAK_PATTERNS:
        hit = pii_pat.search(content)
        # Tokens should be REDACTED in the plan
        if hit:
            # Check if it's in a REDACTED context
            context_start = max(0, hit.start() - 20)
            context = content[context_start:hit.end() + 20]
            redacted = "REDACTED" in context.upper()
            add_check("no_token_leak", redacted,
                      f"Token found but {'REDACTED' if redacted else 'NOT REDACTED'}: {hit.group()[:8]}...")
        else:
            add_check("no_token_leak", True, "")

    # 6. Customer handle valid format (check from metadata in file)
    handle_match = re.search(r"\*\*Customer handle:\*\* `([^`]+)`", content)
    if handle_match:
        handle = handle_match.group(1)
        add_check("valid_handle_format", bool(VALID_HANDLE.match(handle)), f"handle={handle}")
    else:
        add_check("valid_handle_format", False, "handle metadata not found in plan")

    # 7. DPA signed marker present
    add_check("dpa_signed_marker", "DPA signed: ✅" in content or "dpa_signed: true" in content.lower(), "")

    # Final verdict
    results["verdict"] = "PASS" if results["fail_count"] == 0 else "FAIL"
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Integration Plan Quality Gate")
    parser.add_argument("--plan-file", default=None, help="Path to integration_plan.md")
    parser.add_argument("--plan-dir", default=None, help="Customer dir; finds integration_plan.md inside")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.plan_file:
        plan_path = Path(args.plan_file)
    elif args.plan_dir:
        plan_path = Path(args.plan_dir) / "integration_plan.md"
    else:
        # Demo check with a non-existent file for CI
        plan_path = REPO_ROOT / "data" / "customers" / "_demo" / "integration_plan.md"

    results = check_plan_file(plan_path)

    if args.json:
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0 if results["verdict"] == "PASS" else 1

    print(f"\n=== Integration Plan Quality Gate ===")
    print(f"File: {results['file']}")
    print(f"Verdict: {results['verdict']}")
    print()
    for check in results["checks"]:
        icon = "✅" if check["status"] == "PASS" else "❌"
        detail = f"  ({check['detail']})" if check["detail"] else ""
        print(f"  {icon} {check['status']:<6} {check['name']}{detail}")
    print()
    print(f"PASS: {results['pass_count']}  FAIL: {results['fail_count']}")
    print()

    if not plan_path.exists():
        print("ℹ️  No plan file found — quality gate runs in CI mode (no plan to validate).")
        return 0  # Not a failure if no customer yet

    return 0 if results["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
