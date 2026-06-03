#!/usr/bin/env python3
"""
Dealix Launch Readiness Check

Verifies that the launch-readiness *governance* is in place (docs, reports,
workflow, scorecard structure, safety policies) and computes a transparent,
evidence-based Launch Score from files that actually exist in the repository.

Design principles
-----------------
* Honest: the score is derived ONLY from real file evidence. Nothing is faked.
* Reproducible: the evidence map below is the single source of truth that the
  static reports in reports/launch/ are written to match.
* Safe by default: structural + safety checks are HARD gates (exit 1 on fail).
  Capability gaps (missing systems) are reported as WARNINGS, not failures,
  because business readiness is a founder decision — not a CI failure.

Exit code: 0 if all hard gates pass, 1 otherwise.

Stdlib only. No external dependencies.
"""

import csv
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --------------------------------------------------------------------------- #
# 1. Required launch-governance artifacts (structural hard gate)
# --------------------------------------------------------------------------- #

REQUIRED_DOCS = [
    "docs/launch/DEALIX_LAUNCH_READINESS_MASTER_AR.md",
    "docs/launch/LAUNCH_MODES_AR.md",
    "docs/launch/INTERNAL_DRY_RUN_PLAN_AR.md",
    "docs/launch/SOFT_LAUNCH_PLAN_AR.md",
    "docs/launch/CONTROLLED_LAUNCH_PLAN_AR.md",
    "docs/launch/FULL_LAUNCH_PLAN_AR.md",
    "docs/launch/LAUNCH_RISK_REGISTER_AR.md",
    "docs/launch/LAUNCH_DECISION_GATE_AR.md",
]

REQUIRED_REPORTS = [
    "reports/launch/DEALIX_LAUNCH_READINESS_EXECUTIVE_SUMMARY.md",
    "reports/launch/LAUNCH_SCORECARD.md",
    "reports/launch/LAUNCH_BLOCKERS.md",
    "reports/launch/LAUNCH_RISK_REGISTER.md",
    "reports/launch/GO_NO_GO_DECISION.md",
    "reports/launch/TECHNICAL_PROOF_CHECKLIST.md",
    "reports/launch/SECURITY_GO_NO_GO.md",
]

REQUIRED_WORKFLOW = ".github/workflows/launch-readiness.yml"

# Safety / privacy policies that resolve specific No-Go blockers
REQUIRED_POLICIES = [
    "company_os/governance/agent_permissions.md",
    "company_os/governance/data_handling_checklist.md",
    "company_os/governance/suppression_policy.md",
    "company_os/governance/external_content_policy.md",
    "reports/founder/DAILY_SUPER_COMMAND.md",
]

# --------------------------------------------------------------------------- #
# 2. Launch Score — evidence-based, transparent
#    tier values: present = 1.0, partial = 0.4, missing = 0.0
# --------------------------------------------------------------------------- #

TIER_VALUE = {"present": 1.0, "partial": 0.4, "missing": 0.0}

DIMENSIONS = [
    {
        "name": "Website",
        "weight": 10,
        "tier": "present",
        "evidence": ["index.html", "src/pages/LandingPage.tsx", "src/pages/Dashboard.tsx"],
        "note": "Site builds (npm run build) and ships multiple routes.",
    },
    {
        "name": "Core 5 Systems",
        "weight": 10,
        "tier": "partial",
        "evidence": [
            "company_os/marketing/one_pagers/one_pager_arabic.md",
            "company_os/revenue/proposals.json",
            "company_os/delivery/p1_delivery_sop.md",
        ],
        "note": "Only P1 + P2 are productized with price + delivery. Target is 5.",
    },
    {
        "name": "Business OS Catalog",
        "weight": 8,
        "tier": "missing",
        "evidence": ["docs/business_os_catalog/CATALOG.md"],
        "note": "No 40-system internal catalog yet.",
    },
    {
        "name": "Business Need Intelligence",
        "weight": 12,
        "tier": "missing",
        "evidence": ["docs/business_need_intelligence/NEEDS.md"],
        "note": "No 25 Needs + 50 Sprints library yet.",
    },
    {
        "name": "Account Intelligence",
        "weight": 12,
        "tier": "partial",
        "evidence": ["company_os/revenue/prospects.csv"],
        "note": "Basic prospect list only; no Account Pack Contract / Top 100 queue.",
    },
    {
        "name": "Contact Discovery",
        "weight": 8,
        "tier": "partial",
        "evidence": [
            "company_os/governance/data_handling_checklist.md",
            "company_os/governance/suppression_policy.md",
        ],
        "note": "Policy + role-based contacts (no invented contacts). No discovery engine.",
    },
    {
        "name": "Outreach Quality",
        "weight": 8,
        "tier": "partial",
        "evidence": [
            "company_os/revenue/outreach_queue.json",
            "scripts/generate_outreach_queue.py",
            "company_os/revenue/objections.json",
        ],
        "note": "Draft queue + generator exist. Executable email quality gate not built.",
    },
    {
        "name": "Call / Proposal",
        "weight": 8,
        "tier": "partial",
        "evidence": ["company_os/revenue/proposals.json"],
        "note": "Proposal templates exist. No call brief queue / proposal approval gate code.",
    },
    {
        "name": "Delivery",
        "weight": 8,
        "tier": "partial",
        "evidence": [
            "company_os/delivery/p1_delivery_sop.md",
            "company_os/delivery/proof_pack_template.md",
            "company_os/delivery/client_success_plan.md",
        ],
        "note": "Delivery SOPs + proof pack template. No per-system delivery gate code.",
    },
    {
        "name": "Finance / Metrics",
        "weight": 5,
        "tier": "partial",
        "evidence": ["scripts/revenue_scorecard.py", "company_os/finance/unit_economics.md"],
        "note": "Scorecard script + unit economics. No live cash-priority engine.",
    },
    {
        "name": "Security / Privacy",
        "weight": 7,
        "tier": "present",
        "evidence": [
            "company_os/governance/agent_permissions.md",
            "company_os/governance/pdpl_checklist.md",
            "company_os/governance/data_handling_checklist.md",
            "company_os/governance/external_content_policy.md",
            "scripts/governance_check.py",
        ],
        "note": "PDPL + agent permissions + untrusted-content policy + governance check.",
    },
    {
        "name": "CI/CD",
        "weight": 4,
        "tier": "present",
        "evidence": [
            ".github/workflows/launch-readiness.yml",
            "scripts/checks/check_launch_readiness.py",
        ],
        "note": "Launch-readiness workflow + this checker.",
    },
]

# Score bands
BANDS = [
    (90, "Full Launch Ready"),
    (85, "Controlled Launch Ready"),
    (75, "Soft Launch Ready"),
    (60, "Internal Dry Run Only"),
    (0, "Not Ready"),
]

# --------------------------------------------------------------------------- #
# 3. Safety scans (hard gate)
# --------------------------------------------------------------------------- #

# Phrases that constitute a guaranteed-results claim (AR + EN). Conservative:
# we target explicit guarantees of outcomes, not ordinary marketing language.
GUARANTEE_PATTERNS = [
    r"نضمن\s+النتائج",
    r"نتائج\s+مضمون",
    r"أرباح\s+مضمون",
    r"عائد\s+مضمون",
    r"ضمان\s+النتائج",
    r"نضاعف\s+أرباح",
    r"\bguarantee(d)?\s+(results|revenue|roi|sales|growth)\b",
    r"\bwe\s+guarantee\b",
    r"\b100%\s+(guarantee|results|roi)\b",
    r"\brisk[-\s]?free\b",
]

# Artifacts that face prospects — must be free of guarantees + invented contacts
PROSPECT_FACING = [
    "company_os/revenue/outreach_queue.json",
    "company_os/revenue/proposals.json",
]

# Email / Saudi-phone patterns used to detect fabricated prospect contacts
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?966|00966|0)5\d{8}")


def rel(path: str) -> Path:
    return BASE_DIR / path


def exists(path: str) -> bool:
    return rel(path).exists()


def read_text(path: str) -> str:
    try:
        return rel(path).read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def check_required_files():
    """Structural hard gate: launch docs/reports/workflow/policies exist."""
    failures = []
    for group, files in (
        ("doc", REQUIRED_DOCS),
        ("report", REQUIRED_REPORTS),
        ("policy", REQUIRED_POLICIES),
    ):
        for f in files:
            if not exists(f):
                failures.append(f"missing {group}: {f}")
    if not exists(REQUIRED_WORKFLOW):
        failures.append(f"missing workflow: {REQUIRED_WORKFLOW}")
    return failures


def check_workflow_least_privilege():
    """Workflow must declare least-privilege permissions."""
    failures = []
    text = read_text(REQUIRED_WORKFLOW)
    if not text:
        return ["workflow not found or empty"]
    if "permissions:" not in text:
        failures.append("workflow has no top-level `permissions:` block (least privilege)")
    elif "contents: read" not in text:
        failures.append("workflow `permissions:` does not pin `contents: read`")
    return failures


def check_scorecard_structure():
    """Scorecard report must mention every weighted dimension."""
    text = read_text("reports/launch/LAUNCH_SCORECARD.md")
    if not text:
        return ["LAUNCH_SCORECARD.md not found or empty"]
    return [f"scorecard missing dimension: {d['name']}"
            for d in DIMENSIONS if d["name"] not in text]


def check_go_no_go_structure():
    """Go/No-Go report must contain a decision + launch-mode structure."""
    text = read_text("reports/launch/GO_NO_GO_DECISION.md").upper()
    if not text:
        return ["GO_NO_GO_DECISION.md not found or empty"]
    failures = []
    for token in ("GO", "NO-GO", "LAUNCH MODE", "FOUNDER"):
        if token not in text:
            failures.append(f"Go/No-Go report missing required token: {token}")
    return failures


def check_blockers_documented():
    text = read_text("reports/launch/LAUNCH_BLOCKERS.md")
    if not text:
        return ["LAUNCH_BLOCKERS.md not found or empty"]
    if "No-Go" not in text and "NO-GO" not in text:
        return ["LAUNCH_BLOCKERS.md does not document No-Go blockers"]
    return []


def scan_guaranteed_claims():
    """Hard gate: no guaranteed-results language in prospect-facing artifacts."""
    findings = []
    for path in PROSPECT_FACING:
        text = read_text(path)
        if not text:
            continue
        for pat in GUARANTEE_PATTERNS:
            if re.search(pat, text, flags=re.IGNORECASE):
                findings.append(f"guaranteed-claim pattern /{pat}/ in {path}")
    return findings


def scan_invented_contacts():
    """Hard gate: prospect data must not contain fabricated personal contacts.

    Policy is role-based (e.g. "Founder / CEO"). A raw personal email or phone
    number in the prospect list/outreach — with no `source`/`contact_source`
    column to back it — is treated as a potential invented contact.
    """
    findings = []

    # prospects.csv
    ppath = rel("company_os/revenue/prospects.csv")
    if ppath.exists():
        with ppath.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            has_source = bool(reader.fieldnames) and any(
                "source" in (c or "").lower() for c in reader.fieldnames
            )
            for i, row in enumerate(reader, start=2):
                blob = " ".join(v for v in row.values() if v)
                if (EMAIL_RE.search(blob) or PHONE_RE.search(blob)) and not has_source:
                    findings.append(
                        f"prospects.csv row {i}: personal email/phone without a source column"
                    )

    # outreach drafts (exclude our own dealix.sa contact handles)
    opath = rel("company_os/revenue/outreach_queue.json")
    if opath.exists():
        try:
            data = json.loads(opath.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        for item in data.get("queue", []):
            body = f"{item.get('draft_subject', '')} {item.get('draft_body', '')}"
            for em in EMAIL_RE.findall(body):
                if not em.lower().endswith("dealix.sa"):
                    findings.append(
                        f"outreach {item.get('id', '?')}: prospect email '{em}' embedded in draft"
                    )
            if PHONE_RE.search(body):
                findings.append(
                    f"outreach {item.get('id', '?')}: phone number embedded in draft"
                )
    return findings


# --------------------------------------------------------------------------- #
# Score
# --------------------------------------------------------------------------- #

def compute_score():
    rows = []
    earned = 0.0
    total = 0
    for d in DIMENSIONS:
        tier = d["tier"]
        # Downgrade if cited evidence is missing (keeps the score honest).
        missing_evidence = [e for e in d["evidence"] if not exists(e)]
        if tier in ("present", "partial") and missing_evidence:
            if len(missing_evidence) == len(d["evidence"]):
                tier = "missing"
            elif tier == "present":
                tier = "partial"
        pts = round(d["weight"] * TIER_VALUE[tier], 2)
        earned += pts
        total += d["weight"]
        rows.append((d["name"], d["weight"], tier, pts, missing_evidence))
    return rows, round(earned, 1), total


def band_for(score: float) -> str:
    for threshold, label in BANDS:
        if score >= threshold:
            return label
    return "Not Ready"


def recommended_mode(score: float, hard_pass: bool) -> str:
    """Honest recommendation.

    Internal Dry Run is a no-external-send, internal-only mode. When the safety
    gates pass it is appropriate even while capability is still maturing, so we
    recommend it as the floor rather than 'Not Ready'.
    """
    if not hard_pass:
        return "BLOCKED — fix hard-gate failures before any launch mode"
    if score >= 90:
        return "Full Launch (subject to founder Go/No-Go)"
    if score >= 85:
        return "Controlled Launch (subject to founder Go/No-Go)"
    if score >= 75:
        return "Soft Launch (subject to founder Go/No-Go)"
    return "Internal Dry Run ONLY — no external sending"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    print("=" * 78)
    print("  DEALIX LAUNCH READINESS CHECK")
    print("=" * 78)
    print()

    hard_failures = []
    hard_failures += check_required_files()
    hard_failures += check_workflow_least_privilege()
    hard_failures += check_scorecard_structure()
    hard_failures += check_go_no_go_structure()
    hard_failures += check_blockers_documented()

    safety_findings = scan_guaranteed_claims() + scan_invented_contacts()

    # ---- Structural ----
    print("  [1] Structural / governance artifacts")
    print("  " + "-" * 60)
    structural = [f for f in hard_failures]
    if structural:
        for f in structural:
            print(f"  FAIL  {f}")
    else:
        print("  PASS  all launch docs, reports, policies, and workflow present")
        print("  PASS  workflow declares least-privilege permissions")
        print("  PASS  scorecard covers all 12 weighted dimensions")
        print("  PASS  Go/No-Go decision structure present")
    print()

    # ---- Safety ----
    print("  [2] Safety gates (no guarantees, no invented contacts)")
    print("  " + "-" * 60)
    if safety_findings:
        for f in safety_findings:
            print(f"  FAIL  {f}")
    else:
        print("  PASS  no guaranteed-results claims in prospect-facing artifacts")
        print("  PASS  no invented prospect contacts detected (role-based only)")
    print()

    # ---- Score ----
    rows, score, total = compute_score()
    print("  [3] Launch Score (evidence-based)")
    print("  " + "-" * 60)
    print(f"  {'Dimension':<28}{'Wt':>4}{'Tier':>10}{'Pts':>7}")
    for name, weight, tier, pts, _missing in rows:
        print(f"  {name:<28}{weight:>4}{tier:>10}{pts:>7}")
    print("  " + "-" * 60)
    pct = round(100 * score / total, 1) if total else 0.0
    print(f"  {'TOTAL':<28}{total:>4}{'':>10}{score:>7}")
    print(f"  Launch Score: {score} / {total}  ({pct}%)  ->  {band_for(pct)}")
    print()

    hard_pass = not structural and not safety_findings
    mode = recommended_mode(pct, hard_pass)

    print("  [4] Recommendation")
    print("  " + "-" * 60)
    print(f"  Hard gates: {'PASS' if hard_pass else 'FAIL'}")
    print(f"  Recommended launch mode: {mode}")
    print()

    print("=" * 78)
    if hard_pass:
        print("  RESULT: HARD GATES PASS (launch governance in place).")
        print("  NOTE:   Capability score is informational; founder Go/No-Go required.")
    else:
        print("  RESULT: HARD GATES FAIL — see FAIL lines above.")
    print("=" * 78)

    return 0 if hard_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
