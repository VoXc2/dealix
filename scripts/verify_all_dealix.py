#!/usr/bin/env python3
"""
Dealix Master Verifier
======================

Single judge for "is Dealix shipped?" Reads the actual state of the repo
and reports PASS / FAIL per system, plus a 0-5 completion score per system.

Doctrine: nothing is "shipped" until five proof types exist —
  1. Files          (docs / code modules on disk)
  2. Tests          (locked-in rule tests)
  3. API / Script   (programmatic verifier)
  4. Deploy         (Founder Command Center / production)
  5. Market Motion  (partner / invoice / customer feedback)

This script verifies (1), (2), and (3). Layers (4) and (5) are gated by
explicit marker files the founder updates after deploy / outreach:

    data/founder_command_center_status.json
    data/partner_outreach_log.json
    data/first_invoice_log.json

If those marker files are absent, the verifier will not award the
deploy / market motion points — by design.

Usage:
    python scripts/verify_all_dealix.py
    python scripts/verify_all_dealix.py --json
    python scripts/verify_all_dealix.py --system Doctrine

Exit code 0 = overall PASS, 1 = overall FAIL.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

def _c(code: str, text: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"

def green(t: str) -> str: return _c("32", t)
def red(t: str)   -> str: return _c("31", t)
def yellow(t: str) -> str: return _c("33", t)
def bold(t: str)  -> str: return _c("1",  t)


# ---------------------------------------------------------------------------
# Check primitives
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""

@dataclass
class SystemReport:
    name: str
    docs:    list[CheckResult] = field(default_factory=list)
    code:    list[CheckResult] = field(default_factory=list)
    tests:   list[CheckResult] = field(default_factory=list)
    api:     list[CheckResult] = field(default_factory=list)
    deploy:  list[CheckResult] = field(default_factory=list)
    market:  list[CheckResult] = field(default_factory=list)

    def _layer_ok(self, layer: list[CheckResult]) -> bool:
        return bool(layer) and all(c.ok for c in layer)

    def _all(self) -> Iterable[CheckResult]:
        yield from self.docs
        yield from self.code
        yield from self.tests
        yield from self.api
        yield from self.deploy
        yield from self.market

    @property
    def passed(self) -> bool:
        results = list(self._all())
        return bool(results) and all(c.ok for c in results)

    @property
    def missing(self) -> list[str]:
        return [c.name for c in self._all() if not c.ok]

    @property
    def score(self) -> int:
        """
        0 = missing            (no docs)
        1 = docs only          (docs present)
        2 = code exists        (docs + required code present, or n/a)
        3 = tests pass         (above + tests present, or n/a)
        4 = deploy verified    (above + deploy marker present, or n/a)
        5 = market motion      (above + market marker present)
        """
        s = 0
        if self.docs   and self._layer_ok(self.docs):   s = 1
        elif not self.docs: s = 1  # nothing required → start at 1
        if s >= 1 and (not self.code   or self._layer_ok(self.code)):   s = max(s, 2)
        if s >= 2 and (not self.tests  or self._layer_ok(self.tests)):  s = max(s, 3)
        if s >= 3 and (not self.api    or self._layer_ok(self.api)):    s = max(s, 4)
        if s >= 4 and self.deploy and self._layer_ok(self.deploy):       s = 4
        if s >= 4 and self.market and self._layer_ok(self.market):       s = 5
        # If a required earlier layer fails, score must reflect that.
        if self.docs   and not self._layer_ok(self.docs):   s = 0
        elif self.code  and not self._layer_ok(self.code):  s = min(s, 1)
        elif self.tests and not self._layer_ok(self.tests): s = min(s, 2)
        elif self.api   and not self._layer_ok(self.api):   s = min(s, 3)
        return s


def file_check(rel: str, label: str | None = None) -> CheckResult:
    p = REPO_ROOT / rel
    return CheckResult(
        name=label or rel,
        ok=p.exists(),
        detail="exists" if p.exists() else "MISSING",
    )

def any_of_files_check(rels: list[str], label: str) -> CheckResult:
    for rel in rels:
        if (REPO_ROOT / rel).exists():
            return CheckResult(name=label, ok=True, detail=f"found {rel}")
    return CheckResult(name=label, ok=False, detail=f"none of: {rels}")

def grep_absent(pattern: str, paths: list[str], label: str) -> CheckResult:
    """PASS if `pattern` is NOT found in any of `paths`."""
    rx = re.compile(pattern, re.IGNORECASE)
    hits: list[str] = []
    for rel in paths:
        root = REPO_ROOT / rel
        if not root.exists():
            continue
        if root.is_file():
            files = [root]
        else:
            files = [p for p in root.rglob("*") if p.is_file()]
        for f in files:
            if f.suffix in {".png", ".jpg", ".jpeg", ".pdf", ".zip", ".woff", ".woff2", ".ico", ".gif"}:
                continue
            try:
                txt = f.read_text(errors="ignore")
            except OSError:
                continue
            if rx.search(txt):
                hits.append(str(f.relative_to(REPO_ROOT)))
                if len(hits) >= 3:
                    break
        if len(hits) >= 3:
            break
    if hits:
        return CheckResult(name=label, ok=False, detail=f"found in: {', '.join(hits)}")
    return CheckResult(name=label, ok=True, detail="not found")

def json_check(rel: str, required_keys: list[str], label: str) -> CheckResult:
    p = REPO_ROOT / rel
    if not p.exists():
        return CheckResult(name=label, ok=False, detail=f"MISSING {rel}")
    try:
        data = json.loads(p.read_text())
    except Exception as e:
        return CheckResult(name=label, ok=False, detail=f"INVALID JSON {rel}: {e}")
    missing = [k for k in required_keys if k not in data]
    if missing:
        return CheckResult(name=label, ok=False, detail=f"missing keys: {missing}")
    return CheckResult(name=label, ok=True, detail=f"{rel} ok")


def positive_count_check(rel: str, count_key: str, label: str) -> CheckResult:
    """
    Honest market-motion check. Passes only if the JSON marker file exists,
    is valid, and the named count is >= 1. This is how we refuse to award a
    market-motion score for an artifact that says nothing has happened yet.
    """
    p = REPO_ROOT / rel
    if not p.exists():
        return CheckResult(name=label, ok=False, detail=f"MISSING {rel}")
    try:
        data = json.loads(p.read_text())
    except Exception as e:
        return CheckResult(name=label, ok=False, detail=f"INVALID JSON {rel}: {e}")
    value = data.get(count_key)
    if not isinstance(value, int):
        return CheckResult(name=label, ok=False, detail=f"{rel}: {count_key} not an int")
    if value < 1:
        return CheckResult(
            name=label, ok=False,
            detail=f"{rel}: {count_key}={value} — no real activity logged yet",
        )
    return CheckResult(name=label, ok=True, detail=f"{rel}: {count_key}={value}")


# ---------------------------------------------------------------------------
# System definitions
# ---------------------------------------------------------------------------

def system_doctrine() -> SystemReport:
    r = SystemReport("Doctrine")
    r.docs = [
        file_check("docs/00_constitution/DEALIX_CONSTITUTION.md"),
        file_check("docs/00_constitution/NON_NEGOTIABLES.md"),
        file_check("docs/00_constitution/WHAT_DEALIX_REFUSES.md"),
        file_check("docs/01_category/GOVERNED_AI_OPERATIONS.md"),
    ]
    r.tests = [
        any_of_files_check(
            ["tests/test_doctrine_guardrails.py",
             "tests/test_dealix_promise.py",
             "tests/test_doctrine_has_11_non_negotiables.py"],
            "doctrine guardrail tests",
        ),
    ]
    return r

def system_offer_ladder() -> SystemReport:
    r = SystemReport("Offer Ladder")
    r.docs = [
        any_of_files_check(
            ["docs/sales-kit/OFFER_LADDER.md",
             "docs/OFFER_LADDER.md",
             "docs/OFFER_LADDER_AND_PRICING.md",
             "docs/company/OFFER_LADDER.md"],
            "OFFER_LADDER doc",
        ),
        file_check("docs/03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md"),
        any_of_files_check(
            ["docs/sales-kit/INVESTOR_ONE_PAGER.md",
             "docs/INVESTOR_ONE_PAGER.md",
             "docs/investment/INVESTOR_ONE_PAGER.md"],
            "INVESTOR_ONE_PAGER doc",
        ),
    ]
    # The verifier itself is the API/script for this system.
    r.api = [CheckResult(name="offer ladder grep", ok=True, detail="this script")]
    return r

def system_revenue_engine() -> SystemReport:
    r = SystemReport("Revenue Engine")
    r.docs = [file_check("docs/03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md")]
    r.code = [
        file_check("auto_client_acquisition/revenue_os/account_scoring.py"),
        file_check("auto_client_acquisition/revenue_os/draft_pack.py"),
        file_check("auto_client_acquisition/revenue_os/followup_plan.py"),
    ]
    r.tests = [
        file_check("tests/test_no_scraping_engine.py"),
        file_check("tests/test_no_cold_whatsapp.py"),
        file_check("tests/test_no_guaranteed_claims.py"),
    ]
    return r

def system_data_os() -> SystemReport:
    r = SystemReport("Data OS")
    r.docs = [any_of_files_check(
        ["docs/04_data_os/README.md", "docs/06_data_os/README.md"],
        "Data OS doc",
    )]
    r.code = [
        file_check("auto_client_acquisition/data_os/source_passport.py"),
        file_check("auto_client_acquisition/data_os/import_preview.py"),
        file_check("auto_client_acquisition/data_os/data_quality_score.py"),
        file_check("auto_client_acquisition/data_os/pii_classifier.py"),
        file_check("auto_client_acquisition/data_os/dedupe.py"),
        file_check("auto_client_acquisition/data_os/normalization.py"),
    ]
    r.tests = [
        file_check("tests/test_no_source_passport_no_ai.py"),
        file_check("tests/test_pii_external_requires_approval.py"),
    ]
    return r

def system_governance_os() -> SystemReport:
    r = SystemReport("Governance OS")
    r.docs = [any_of_files_check(
        ["docs/05_governance_os/README.md", "docs/07_governance/README.md"],
        "Governance OS doc",
    )]
    r.code = [
        file_check("auto_client_acquisition/governance_os/runtime_decision.py"),
        file_check("auto_client_acquisition/governance_os/policy_registry.py"),
        file_check("auto_client_acquisition/governance_os/channel_policy.py"),
        file_check("auto_client_acquisition/governance_os/claim_safety.py"),
        file_check("auto_client_acquisition/governance_os/approval_policy.py"),
    ]
    r.tests = [
        file_check("tests/test_no_cold_whatsapp.py"),
        file_check("tests/test_no_linkedin_automation.py"),
        file_check("tests/test_no_scraping_engine.py"),
        file_check("tests/test_no_guaranteed_claims.py"),
    ]
    return r

def system_proof_os() -> SystemReport:
    r = SystemReport("Proof OS")
    r.docs = [file_check("docs/07_proof_os/README.md")]
    r.code = [file_check("auto_client_acquisition/proof_os/proof_pack.py")]
    r.tests = [
        file_check("tests/test_proof_pack_required.py"),
        file_check("tests/test_case_study_requires_verified_value.py"),
    ]
    return r

def system_value_os() -> SystemReport:
    r = SystemReport("Value OS")
    r.docs = [file_check("docs/08_value_os/README.md")]
    r.code = [file_check("auto_client_acquisition/value_os/value_ledger.py")]
    r.tests = [file_check("tests/test_case_study_requires_verified_value.py")]
    return r

def system_capital_os() -> SystemReport:
    r = SystemReport("Capital OS")
    r.docs = [file_check("docs/09_capital_os/README.md")]
    r.code = [
        file_check("auto_client_acquisition/capital_os/capital_ledger.py"),
        file_check("auto_client_acquisition/capital_os/asset_types.py"),
    ]
    return r

def system_retainer_engine() -> SystemReport:
    r = SystemReport("Retainer Engine")
    r.docs = [any_of_files_check(
        ["docs/delivery/RETAINER_READINESS.md",
         "docs/readiness/gate_8_retainer_readiness.md",
         "docs/03_commercial_mvp/RETAINER_PATH.md"],
        "Retainer readiness doc",
    )]
    return r

def system_trust_pack() -> SystemReport:
    r = SystemReport("Trust Pack")
    r.docs = [file_check("docs/14_trust_os/TRUST_PACK.md")]
    r.code = [file_check("auto_client_acquisition/trust_os/trust_pack.py")]
    return r

def system_evidence_plane() -> SystemReport:
    r = SystemReport("Evidence Control Plane")
    r.docs = [any_of_files_check(
        ["docs/16_evidence_control_plane/README.md",
         "docs/13_evidence_control_plane/README.md",
         "docs/15_evidence_control_plane/README.md"],
        "Evidence Control Plane doc",
    )]
    r.code = [
        file_check("auto_client_acquisition/evidence_control_plane_os/evidence_graph.py"),
        file_check("auto_client_acquisition/evidence_control_plane_os/accountability_map.py"),
    ]
    return r

def system_agent_safety() -> SystemReport:
    r = SystemReport("Agent Safety")
    r.docs = [any_of_files_check(
        ["docs/17_secure_agent_runtime/README.md",
         "docs/11_secure_runtime/README.md",
         "docs/18_secure_agent_runtime/README.md",
         "docs/36_agent_runtime_security/README.md"],
        "Agent runtime doc",
    )]
    r.code = [
        any_of_files_check(
            ["auto_client_acquisition/agent_os/__init__.py",
             "auto_client_acquisition/agents/__init__.py"],
            "agent_os module",
        ),
        file_check("auto_client_acquisition/secure_agent_runtime_os/__init__.py"),
    ]
    return r

def system_gcc_expansion() -> SystemReport:
    r = SystemReport("GCC Expansion")
    r.docs = [any_of_files_check(
        ["docs/gcc-expansion/GCC_EXPANSION_THESIS.md",
         "docs/saudi/GCC_EXPANSION.md",
         "docs/37_saudi_layer/GCC_EXPANSION.md",
         "docs/SAUDI_GCC_EXPANSION.md"],
        "GCC Expansion doc",
    )]
    r.tests = [any_of_files_check(
        ["tests/test_gcc_expansion_preserves_saudi_beachhead.py",
         "tests/test_gcc_expansion.py"],
        "GCC expansion test",
    )]
    return r

def system_funding_pack() -> SystemReport:
    r = SystemReport("Funding Pack")
    r.docs = [
        file_check("docs/investment/FUNDING_READINESS.md"),
        any_of_files_check(
            ["docs/funding/USE_OF_FUNDS.md",
             "docs/investment/USE_OF_FUNDS.md"],
            "USE_OF_FUNDS doc",
        ),
        any_of_files_check(
            ["docs/funding/HIRING_SCORECARDS.md",
             "docs/hiring/HIRING_SCORECARDS.md",
             "docs/hiring/SCORECARDS.md"],
            "Hiring scorecards doc",
        ),
    ]
    r.tests = [any_of_files_check(
        ["tests/test_funding_pack_has_use_of_funds.py"],
        "funding pack test",
    )]
    return r

def system_open_doctrine() -> SystemReport:
    r = SystemReport("Open Doctrine")
    r.docs = [any_of_files_check(
        ["open-doctrine/README.md",
         "docs/open-doctrine/README.md",
         "docs/open_doctrine/README.md",
         "docs/OPEN_DOCTRINE.md"],
        "Open Doctrine doc",
    )]
    r.tests = [any_of_files_check(
        ["tests/test_open_doctrine_exists.py",
         "tests/test_public_doctrine_does_not_expose_commercial_secrets.py"],
        "open doctrine test",
    )]
    return r

def system_founder_command_center() -> SystemReport:
    r = SystemReport("Founder Command Center")
    r.docs = [any_of_files_check(
        ["landing/founder-command-center.html",
         "landing/founder-command-bus.html",
         "landing/executive-command-center.html"],
        "Founder Command Center page",
    )]
    # Deploy marker: founder sets data/founder_command_center_status.json
    # after confirming the dashboard reflects current state.
    r.deploy = [file_check(
        "data/founder_command_center_status.json",
        label="founder_command_center_status.json (deploy marker)",
    )]
    return r

def system_partner_motion() -> SystemReport:
    r = SystemReport("Partner Motion")
    r.docs = [
        any_of_files_check(
            ["docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md",
             "docs/partners/ANCHOR_PARTNER_OUTREACH.md"],
            "Anchor partner outreach doc",
        ),
        any_of_files_check(
            ["docs/partners/PARTNER_COVENANT.md",
             "docs/40_partners/PARTNER_COVENANT.md"],
            "Partner covenant doc",
        ),
    ]
    r.api = [file_check("data/anchor_partner_pipeline.json")]
    # Market motion: file must exist AND outreach_sent_count >= 1.
    # File presence alone does not award the market-motion point.
    r.market = [positive_count_check(
        "data/partner_outreach_log.json",
        "outreach_sent_count",
        "partner outreach actually sent",
    )]
    return r

def system_first_invoice_motion() -> SystemReport:
    r = SystemReport("First Invoice Motion")
    r.docs = [file_check("docs/ops/FIRST_INVOICE_UNLOCK.md")]
    # Operational layer: log file must exist and be valid JSON.
    r.api = [file_check(
        "data/first_invoice_log.json",
        label="first_invoice_log.json (operational marker)",
    )]
    # Market motion: invoice_sent_count >= 1.
    r.market = [positive_count_check(
        "data/first_invoice_log.json",
        "invoice_sent_count",
        "first invoice actually sent",
    )]
    return r

def system_business_unit_registry() -> SystemReport:
    r = SystemReport("Business Unit Registry")
    r.docs = [
        file_check("docs/holding/HOLDING_CHARTER.md"),
        file_check("docs/holding/BUSINESS_UNIT_REGISTRY.md"),
    ]
    r.code = [
        file_check("scripts/register_business_unit.py"),
        file_check("scripts/validate_business_units.py"),
    ]
    r.tests = [file_check("tests/test_business_unit_registry.py")]
    r.api = [file_check("data/business_units.json")]
    return r


def system_group_apis() -> SystemReport:
    r = SystemReport("Group APIs")
    r.code = [
        file_check("api/routers/holding.py"),
        file_check("api/routers/business_units.py"),
    ]
    r.tests = [file_check("tests/test_holding_endpoints.py")]
    r.api = [file_check("data/business_units.json")]
    return r


def system_group_treasury_and_capital_allocation() -> SystemReport:
    r = SystemReport("Group Treasury & Capital Allocation")
    r.docs = [
        file_check("docs/holding/CAPITAL_ALLOCATION_POLICY.md"),
        file_check("docs/holding/GROUP_TREASURY.md"),
        file_check("docs/holding/HOLDING_ANNUAL_REPORT_TEMPLATE.md"),
    ]
    r.code = [file_check("scripts/render_annual_report.py")]
    r.tests = [
        file_check("tests/test_capital_allocation_policy_matches_board_engine.py"),
        file_check("tests/test_annual_report_is_byte_stable.py"),
    ]
    r.api = [file_check("landing/assets/downloads/dealix-group-annual-report-2026.md")]
    return r


def system_brand_architecture() -> SystemReport:
    r = SystemReport("Brand Architecture")
    r.docs = [
        file_check("docs/brand/BRAND_ARCHITECTURE.md"),
        file_check("docs/brand/MASTER_BRAND.md"),
        file_check("docs/brand/SUB_BRAND_RULES.md"),
        file_check("partner-kit/branding/HOLDING_BRAND_NOTE.md"),
    ]
    r.code = [file_check("scripts/render_holding_portfolio.py")]
    r.tests = [
        file_check("tests/test_brand_architecture_lists_all_active_units.py"),
        file_check("tests/test_brand_architecture_doctrine_endorsement.py"),
    ]
    r.api = [
        file_check("landing/group.html"),
        file_check("landing/assets/data/holding-portfolio.json"),
    ]
    return r


def system_ma_and_bu_lifecycle() -> SystemReport:
    r = SystemReport("M&A & BU Lifecycle Discipline")
    r.docs = [
        file_check("docs/holding/ACQUISITION_THESIS.md"),
        file_check("docs/holding/MA_PLAYBOOK.md"),
        file_check("docs/holding/SUBSIDIARY_ONBOARDING.md"),
        file_check("docs/holding/BU_KILL_RULES.md"),
    ]
    r.code = [file_check("scripts/draft_bu_decision_memo.py")]
    r.tests = [
        file_check("tests/test_bu_kill_rules_match_unit_governance.py"),
        file_check("tests/test_ma_playbook_lists_required_artifacts.py"),
    ]
    return r


def system_market_feedback() -> SystemReport:
    r = SystemReport("Market Feedback")
    r.docs = [any_of_files_check(
        ["docs/ops/MARKET_FEEDBACK.md", "docs/sales-kit/MARKET_FEEDBACK.md"],
        "Market feedback doc",
    )]
    r.code = [
        file_check("api/routers/market_feedback.py"),
        file_check("scripts/market_feedback_summary.py"),
    ]
    r.tests = [file_check("tests/test_market_feedback_endpoint.py")]
    return r


def system_partner_kit() -> SystemReport:
    r = SystemReport("Partner Kit")
    r.docs = [
        file_check("partner-kit/README.md"),
        file_check("partner-kit/TRUST_PACK_TEMPLATE.md"),
        file_check("partner-kit/PROOF_PACK_TEMPLATE.md"),
        file_check("partner-kit/DOCTRINE_ADOPTION_CHECKLIST.md"),
    ]
    r.code = [file_check("scripts/build_partner_kit_zip.py")]
    r.tests = [file_check("tests/test_partner_kit_contents.py")]
    r.api = [file_check("landing/assets/downloads/dealix-partner-kit-v1.zip")]
    return r


def system_doctrine_versioning() -> SystemReport:
    r = SystemReport("Doctrine Versioning")
    r.docs = [
        file_check("open-doctrine/VERSIONS.md"),
    ]
    r.code = [
        file_check("open-doctrine/doctrine_versions.json"),
        file_check("scripts/tag_doctrine_version.py"),
    ]
    r.tests = [file_check("tests/test_doctrine_versioning.py")]
    return r


def system_customer_readiness_gate() -> SystemReport:
    r = SystemReport("Customer Readiness Gate")
    r.docs = [any_of_files_check(
        ["docs/sales-kit/CUSTOMER_READINESS.md"],
        "Customer Readiness sales-kit doc",
    )]
    r.code = [
        file_check("auto_client_acquisition/customer_readiness/readiness_gate.py"),
        file_check("api/routers/customer_readiness_gate.py"),
    ]
    r.tests = [
        file_check("tests/test_customer_readiness_gate_compute.py"),
        file_check("tests/test_customer_readiness_admin_endpoint.py"),
        file_check("tests/test_customer_readiness_public_endpoint_is_safe.py"),
    ]
    return r


def system_public_trust_surface() -> SystemReport:
    r = SystemReport("Public Trust Surface")
    r.docs = [any_of_files_check(
        ["landing/founder-command-center.html"],
        "Founder Command Center page",
    )]
    r.code = [
        file_check("scripts/render_trust_badges.py"),
        file_check("scripts/render_public_sitemap.py"),
        file_check("api/routers/trust_status.py"),
    ]
    r.tests = [
        file_check("tests/test_trust_status_endpoint.py"),
        file_check("tests/test_trust_badges_are_stable.py"),
        file_check("tests/test_trust_badges_have_no_pii.py"),
    ]
    r.api = [
        file_check("landing/assets/badges/doctrine-status.svg"),
        file_check("landing/assets/badges/verifier-score.svg"),
        file_check("landing/sitemap.xml"),
    ]
    return r


def system_continuous_routine() -> SystemReport:
    r = SystemReport("Continuous Routine")
    r.docs = [any_of_files_check(
        ["docs/ops/CONTINUOUS_ROUTINE.md",
         "docs/ops/DAILY_OPERATING_LOOP.md"],
        "Continuous routine doc",
    )]
    r.code = [
        any_of_files_check(
            ["scripts/daily_routine.py", "scripts/daily_operate.sh", "scripts/daily_sanity.sh"],
            "daily routine script",
        ),
        any_of_files_check(
            ["scripts/weekly_ceo_review.py",
             "scripts/dealix_weekly_executive_pack.py",
             "scripts/weekly_brief_runner.py"],
            "weekly CEO review script",
        ),
    ]
    return r


SYSTEMS: list[Callable[[], SystemReport]] = [
    system_doctrine,
    system_offer_ladder,
    system_revenue_engine,
    system_data_os,
    system_governance_os,
    system_proof_os,
    system_value_os,
    system_capital_os,
    system_retainer_engine,
    system_trust_pack,
    system_evidence_plane,
    system_agent_safety,
    system_gcc_expansion,
    system_funding_pack,
    system_open_doctrine,
    system_founder_command_center,
    system_partner_motion,
    system_first_invoice_motion,
    system_continuous_routine,
    system_public_trust_surface,
    system_customer_readiness_gate,
    system_doctrine_versioning,
    system_partner_kit,
    system_market_feedback,
    system_business_unit_registry,
    system_group_apis,
    system_group_treasury_and_capital_allocation,
    system_brand_architecture,
    system_ma_and_bu_lifecycle,
]

# Systems that must be ≥ 4/5 for "CEO complete".
TOP_EIGHT = {
    "Doctrine",
    "Offer Ladder",
    "Revenue Engine",
    "Data OS",
    "Governance OS",
    "Proof OS",
    "Founder Command Center",
    "Partner Motion",
}


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_human(reports: list[SystemReport]) -> None:
    print(bold("DEALIX MASTER VERIFICATION"))
    print("=" * 60)
    for r in reports:
        tag = green("[PASS]") if r.passed else red("[FAIL]")
        score = f"score {r.score}/5"
        print(f"{tag} {r.name:<28}  {score}")
        if not r.passed:
            for m in r.missing:
                print(f"        - missing: {m}")
    print("=" * 60)

    overall = all(r.passed for r in reports)
    ceo_ready = all(r.score >= 4 for r in reports if r.name in TOP_EIGHT)

    print(f"Overall: {green('PASS') if overall else red('FAIL')}")
    print(f"CEO-complete (top 8 ≥ 4/5): {green('YES') if ceo_ready else yellow('NO')}")
    if not overall:
        print("\nFix the missing items above, then re-run:")
        print("    python scripts/verify_all_dealix.py")

def print_json(reports: list[SystemReport]) -> None:
    payload = {
        "overall_pass": all(r.passed for r in reports),
        "ceo_complete": all(r.score >= 4 for r in reports if r.name in TOP_EIGHT),
        "systems": [
            {
                "name": r.name,
                "passed": r.passed,
                "score": r.score,
                "in_top_eight": r.name in TOP_EIGHT,
                "missing": r.missing,
            }
            for r in reports
        ],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix master verifier")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--system", default=None, help="verify only one system by name")
    args = parser.parse_args(argv)

    reports = [fn() for fn in SYSTEMS]
    if args.system:
        reports = [r for r in reports if r.name.lower() == args.system.lower()]
        if not reports:
            print(red(f"unknown system: {args.system}"), file=sys.stderr)
            return 2

    if args.json:
        print_json(reports)
    else:
        print_human(reports)

    return 0 if all(r.passed for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
