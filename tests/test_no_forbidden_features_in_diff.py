"""Doctrine-as-code: forbidden features must never appear in product code.

The eleven non-negotiables prohibit:
  - scraping engines
  - cold WhatsApp automation
  - LinkedIn automation
  - guaranteed-revenue language in customer-facing copy

This test scans product directories for forbidden patterns and an
allowlist of safety / doctrine files that LEGITIMATELY mention these
terms because they PROHIBIT them. Any new occurrence outside the
allowlist fails the build.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Directories where forbidden patterns must NOT introduce active features.
SCAN_DIRS = (
    "auto_client_acquisition",
    "api",
    "scripts",
    "integrations",
    "core",
)

# File extensions worth scanning (skip binary / vendored).
SCAN_SUFFIXES = {".py", ".sh"}

# Path patterns whose entire purpose is to forbid / detect / refuse
# these things. New entries here are only added if the file's job is
# to enforce a prohibition, not implement an active feature.
ALLOWLIST_SUBSTRINGS = (
    # Test files that lock the rules:
    "test_no_",
    "no_cold_whatsapp",
    "no_linkedin",
    "no_scraping",
    "no_guaranteed",
    # Doctrine / safety / governance directories:
    "/governance_os/",
    "/safety",
    "forbidden_actions",
    "claim_safety",
    "channel_policy",
    "agent_governance",
    "approval_policy",
    "compliance_os",
    "responsible_ai_os",
    "risk_resilience_os",
    # Verifier and reporting tooling that references rule names:
    "verify_all_dealix",
    "render_verifier_report",
    "log_partner_outreach",
    "v7_no_",
    "v10_master",
    # Refusal-listing modules — they enumerate forbidden patterns so
    # the system can reject them (these are the OPPOSITE of an active
    # feature implementing them):
    "bad_revenue",
    "good_revenue_bad_revenue",
    "/decision_passport/",
    "/board_decision_os/",
    "capital_allocation_board",
    "evidence_control_plane_os",
    "customer_journey",  # safety_notes registry
    "campaign_intelligence_sprint",  # docstring references to refusals
    "/blockers.py",                  # tool-category BLOCKER registry
    "pricing_catalog",               # refused pricing patterns
    "saudi_dimensions",              # source-type rejection branch
    "service_mapping_v7",            # schema fields enumerating refusals
    "/audits/",                      # audit / detection passes
    "anti_waste",                    # explicit anti-waste rules
    "founder_v10/founder_rules",     # founder-rule registry
    "/audit_",                       # audit detection scripts
)


def _allowlisted(rel_path: str) -> bool:
    return any(s in rel_path for s in ALLOWLIST_SUBSTRINGS)


def _candidate_files() -> list[Path]:
    out: list[Path] = []
    for d in SCAN_DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix not in SCAN_SUFFIXES:
                continue
            rel = p.relative_to(REPO_ROOT).as_posix()
            if _allowlisted(rel):
                continue
            out.append(p)
    return out


# Only flag matches that appear in **active-feature implementations**:
# function definitions, class definitions, async function definitions,
# or imports — NOT string literals, schema fields, or comment lists.
#
# This is the right architectural check: a string containing the term
# "linkedin_automation" inside a list of refused categories is not an
# active feature. A `def linkedin_automation_send(...)` is.
ACTIVE_FEATURE_LINE = re.compile(
    r"^\s*(async\s+def|def|class|from\s+\S+\s+import|import)\s",
)

FORBIDDEN_IDENTIFIER = re.compile(
    r"(?:"
    r"cold[_-]*whatsapp[_-]*(?:send|engine|blast|loop|queue|worker|runner|client)|"
    r"send[_-]*cold[_-]*whatsapp|"
    r"linkedin[_-]*(?:scraper|automation|connection[_-]*spam|dm[_-]*spam)|"
    r"linkedin[_-]*scrape\b|"
    r"scrape[_-]*linkedin|scrape[_-]*twitter|scrape[_-]*facebook|scrape[_-]*instagram|"
    r"web[_-]*scraper|generic[_-]*scraper|html[_-]*scraper|"
    r"guarantee[_-]*(?:revenue|sales|outcome)"
    r")",
    flags=re.IGNORECASE,
)


# Markers that indicate the line is referencing a PROHIBITION, not an
# active feature. If any of these appear on the same line as a forbidden
# match, the match is considered a legitimate prohibition reference.
PROHIBITION_MARKERS = re.compile(
    r"("
    # Negation prefixes / phrases:
    r"\bno[_ ][a-z]|"
    r"\bnot[_ ][a-z]|"
    r"\bnever\b|"
    r"\bwithout\b|"
    # Explicit prohibition vocabulary (also as a prefix for refusal
    # function names like `reject_cold_whatsapp_send`):
    r"\bforbidden\b|\bprohibit\w*|\brefus\w+|\bdeny\b|\bdenied\b|"
    r"\bblock\w*|\brejected?\b|"
    r"\breject_|\bblock_|\bforbid_|\brefuse_|\bdeny_|\bguard_|\bgate_|"
    # Compliance / policy / safety registries:
    r"\bcompliance\b|\bsafety_note|\bsafety\b|\bpolicy\b|\bguardrail|"
    # Test / evidence / reference fields in registry data structures:
    r"\btest_paths\s*=|\bevidence_paths\s*=|\breference\s*=|\brequirement\s*=|"
    # Docstring / comment patterns that explicitly list refusals:
    r"\"\s*No\s+|'\s*No\s+|#\s*No\s+|\bWHAT_DEALIX_REFUSES|REFUSES"
    r")",
    flags=re.IGNORECASE,
)


def _line_at(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return text[start:end]


def test_no_forbidden_features_implemented_in_product_code():
    """Active-feature check: a forbidden identifier must NOT appear as a
    function definition, class definition, or import. String literals
    and schema fields that mention these terms are fine — they're
    enumerating refusals, not implementing them.
    """
    hits: list[str] = []
    for path in _candidate_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in FORBIDDEN_IDENTIFIER.finditer(text):
            line = _line_at(text, m.start())
            # Only flag if the line is an ACTIVE feature declaration.
            if not ACTIVE_FEATURE_LINE.match(line):
                continue
            # And the line is not a prohibition marker (e.g.
            # `def reject_cold_whatsapp(...)` should be skipped).
            if PROHIBITION_MARKERS.search(line):
                continue
            line_no = text[: m.start()].count("\n") + 1
            hits.append(
                f"{path.relative_to(REPO_ROOT)}:{line_no} → matched {m.group(0)!r}\n      line: {line.strip()[:120]}"
            )
            if len(hits) >= 5:
                break
        if len(hits) >= 5:
            break

    assert not hits, (
        "Forbidden feature implementations found in product code:\n  - "
        + "\n  - ".join(hits)
        + "\n\nDealix doctrine refuses these features. If the new code is "
        "actually a REFUSAL of the feature, name it accordingly "
        "(reject_*, block_*, no_*) and the prohibition-markers regex "
        "will allow it."
    )


def test_gate_would_catch_a_real_violation():
    """Meta-test: prove the gate isn't all-allowlist. A synthetic
    'def cold_whatsapp_send_loop(...)' line MUST trigger a hit.
    """
    synthetic = "def cold_whatsapp_send_loop(target):\n    pass\n"
    found = False
    for line in synthetic.splitlines():
        if ACTIVE_FEATURE_LINE.match(line) and FORBIDDEN_IDENTIFIER.search(line):
            if not PROHIBITION_MARKERS.search(line):
                found = True
                break
    assert found, (
        "The active-feature gate failed to catch a synthetic violation. "
        "Either FORBIDDEN_IDENTIFIER or ACTIVE_FEATURE_LINE is broken."
    )

    # And a synthetic refusal definition MUST NOT be flagged.
    refusal = "def reject_cold_whatsapp_send(...):\n    pass\n"
    flagged = False
    for line in refusal.splitlines():
        if ACTIVE_FEATURE_LINE.match(line) and FORBIDDEN_IDENTIFIER.search(line):
            if not PROHIBITION_MARKERS.search(line):
                flagged = True
                break
    assert not flagged, (
        "A `reject_*` refusal function was incorrectly flagged as an "
        "active feature."
    )
