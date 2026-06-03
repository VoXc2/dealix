#!/usr/bin/env python3
"""
Dealix Operating Factory Check
Validates the integrity of the Maximum Revenue Factory operating loop:
files present, scorecard sections, loop coverage, quality-gate coverage,
clean customer-facing copy (no guaranteed claims / no internal module names),
and presence of security/privacy policies.

Exit 0 if all REQUIRED checks pass, else 1. Does not check whether the website
is fully built or the pipeline is automated — that is tracked in the scorecard.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Required files
# ---------------------------------------------------------------------------
REQUIRED_FILES = [
    "docs/operating_factory/DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md",
    "docs/operating_factory/DAILY_LOOP_AR.md",
    "docs/operating_factory/WEEKLY_LOOP_AR.md",
    "docs/operating_factory/MONTHLY_REVIEW_AR.md",
    "docs/operating_factory/ROLE_OWNERSHIP_AR.md",
    "docs/operating_factory/QUALITY_GATES_AR.md",
    "docs/operating_factory/READY_TO_LAUNCH_CHECKLIST_AR.md",
    "docs/operating_factory/README.md",
    "docs/privacy/PROSPECT_DATA_MINIMIZATION_AR.md",
    "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
    "docs/privacy/CLIENT_DATA_HANDLING_AR.md",
    "docs/privacy/SECRET_HANDLING_POLICY_AR.md",
    "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY_AR.md",
    "reports/operating_factory/DAILY_LOOP_STATUS.md",
    "reports/operating_factory/WEEKLY_LOOP_STATUS.md",
    "reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md",
    "reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md",
    "company_os/governance/do_not_contact.csv",
]

# Required section labels inside the scorecard (the 11 launch capabilities)
SCORECARD_SECTIONS = [
    "Website", "Account Intelligence", "Contacts", "Emails", "Calls",
    "Mini Proposals", "Delivery", "Finance", "Founder Command",
    "Security", "Privacy",
]

# Daily loop must cover the full flow
DAILY_LOOP_STAGES = [
    "Account Discovery", "Contact Discovery", "Email", "Call Brief",
    "Quality Gate", "Founder", "Send", "Mini Proposal", "Delivery",
]

# Quality gates must cover these surfaces
GATE_SURFACES = ["Contact", "Email", "Call", "Proposal", "Delivery", "Finance"]

# Customer-facing claim phrases that are forbidden
FORBIDDEN_CLAIMS = ["نضمن", "نضاعف مبيعاتكم", "مضمون", "guaranteed", "guarantee "]

# Internal-only tokens that must never appear in customer-facing copy
INTERNAL_TOKENS = [
    "Account Pack", "Cash Priority Score", "operating_factory",
    "ai_action_ledger", "contact_confidence", "suppression_list",
]


def read(path):
    p = REPO / path
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="ignore")


def customer_facing_files():
    """The live customer surface = the React web app (excluding vendored UI)."""
    out = []
    src = REPO / "src"
    if src.exists():
        for f in src.rglob("*"):
            if f.suffix in (".tsx", ".ts", ".jsx", ".js") and "components/ui" not in str(f):
                out.append(f)
    return out


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def check_files():
    missing = [f for f in REQUIRED_FILES if not (REPO / f).exists()]
    return (not missing), [f"missing file: {m}" for m in missing]


def check_scorecard_sections():
    content = read("reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md") or ""
    missing = [s for s in SCORECARD_SECTIONS if s not in content]
    return (not missing), [f"scorecard missing section: {m}" for m in missing]


def check_daily_loop():
    content = read("docs/operating_factory/DAILY_LOOP_AR.md") or ""
    missing = [s for s in DAILY_LOOP_STAGES if s not in content]
    return (not missing), [f"daily loop missing stage: {m}" for m in missing]


def check_weekly_learning():
    content = read("docs/operating_factory/WEEKLY_LOOP_AR.md") or ""
    issues = []
    if "Learning Loop" not in content and "حلقة التعلّم" not in content:
        issues.append("weekly loop missing Learning Loop section")
    if "Experiments" not in content and "تجارب" not in content:
        issues.append("weekly loop missing experiments / تجارب")
    return (not issues), issues


def check_quality_gates():
    content = read("docs/operating_factory/QUALITY_GATES_AR.md") or ""
    missing = [s for s in GATE_SURFACES if s not in content]
    return (not missing), [f"quality gates missing surface: {m}" for m in missing]


def check_no_invented_contacts():
    qg = read("docs/operating_factory/QUALITY_GATES_AR.md") or ""
    pm = read("docs/privacy/PROSPECT_DATA_MINIMIZATION_AR.md") or ""
    if "اختلاق" in qg or "مُختلق" in pm or "invented" in (qg + pm).lower():
        return True, []
    return False, ["no-invented-contacts rule not found in gates/privacy docs"]


def check_security_privacy_present():
    needed = [
        "docs/security/EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY_AR.md",
        "docs/privacy/PROSPECT_DATA_MINIMIZATION_AR.md",
        "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
        "docs/privacy/CLIENT_DATA_HANDLING_AR.md",
        "docs/privacy/SECRET_HANDLING_POLICY_AR.md",
    ]
    missing = [f for f in needed if not (REPO / f).exists()]
    return (not missing), [f"missing security/privacy policy: {m}" for m in missing]


def check_no_guaranteed_claims():
    issues = []
    for f in customer_facing_files():
        text = f.read_text(encoding="utf-8", errors="ignore")
        for phrase in FORBIDDEN_CLAIMS:
            if phrase in text:
                issues.append(f"{f.relative_to(REPO)}: forbidden claim '{phrase}'")
    return (not issues), issues


def check_no_internal_names_in_copy():
    issues = []
    for f in customer_facing_files():
        text = f.read_text(encoding="utf-8", errors="ignore")
        for token in INTERNAL_TOKENS:
            if token in text:
                issues.append(f"{f.relative_to(REPO)}: internal token '{token}'")
    return (not issues), issues


CHECKS = [
    ("Required files present", check_files),
    ("Scorecard has all 11 sections", check_scorecard_sections),
    ("Daily loop covers full flow", check_daily_loop),
    ("Weekly loop includes learning loop", check_weekly_learning),
    ("Quality gates cover all surfaces", check_quality_gates),
    ("No-invented-contacts rule present", check_no_invented_contacts),
    ("Security/privacy policies present", check_security_privacy_present),
    ("No guaranteed claims in customer copy", check_no_guaranteed_claims),
    ("No internal module names in customer copy", check_no_internal_names_in_copy),
]


def main():
    print("=" * 70)
    print("DEALIX OPERATING FACTORY CHECK")
    print("=" * 70)

    failures = 0
    for i, (name, fn) in enumerate(CHECKS, 1):
        passed, issues = fn()
        mark = "PASS" if passed else "FAIL"
        print(f"\n[{i}/{len(CHECKS)}] {name} ... {mark}")
        if not passed:
            failures += 1
            for issue in issues[:10]:
                print(f"      - {issue}")

    print("\n" + "=" * 70)
    if failures == 0:
        print("RESULT: ALL CHECKS PASSED")
        print("Operating factory integrity verified.")
    else:
        print(f"RESULT: {failures} CHECK(S) FAILED")
    print("=" * 70)
    return failures == 0


if __name__ == "__main__":
    ok = main()
    raise SystemExit(0 if ok else 1)
