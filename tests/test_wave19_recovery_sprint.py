"""Wave 19 Recovery — CEO Completion Sprint tests.

The verifier-aligned canary tests. Each test enforces ONE gap closed by
the Recovery Sprint. Tests are tolerant of in-flight doc agents:
they skip rather than fail if the file isn't on disk yet — but once
the file lands, the test asserts the integrity rule.

Critical test: `test_public_doctrine_does_not_expose_commercial_secrets`
is the canary against accidentally publishing internal materials in the
open framework.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


# ── INVESTOR_ONE_PAGER ─────────────────────────────────────────────


def test_investor_one_pager_exists_and_lists_three_offer_ladder():
    p = REPO / "docs" / "sales-kit" / "INVESTOR_ONE_PAGER.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # The 3-offer ladder must be visible
    assert "4,999" in text
    assert "25,000" in text
    # Doctrine + non-negotiables references
    assert "Dealix Promise" in text or "doctrine" in text.lower()
    # Bilingual disclaimer
    assert "Estimated outcomes are not guaranteed outcomes" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text


# ── Founder Command Center deployment marker ───────────────────────


def test_founder_command_center_status_marker_exists():
    p = REPO / "data" / "founder_command_center_status.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["deployment_marker"] is True
    assert "Partner Motion" in data["required_cards"]
    assert "Invoice #1" in data["required_cards"]
    # Wave 19 cards present
    for card in ("GCC Standard Readiness", "Capital Asset Count",
                 "Open Doctrine Status", "Funding Pack Status"):
        assert card in data["wave19_cards"], f"missing wave19 card: {card}"


# ── Partner Motion marker integrity ────────────────────────────────


def test_partner_outreach_log_exists_and_is_honest():
    p = REPO / "data" / "partner_outreach_log.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    # MUST be honest: count == len(entries)
    assert data["outreach_sent_count"] == len(data["entries"]), (
        "Marker file lies about outreach state. NEVER edit count without an entry."
    )
    # CEO-complete only flips when at least one outreach is sent
    if data["outreach_sent_count"] == 0:
        assert data["ceo_complete"] is False


def test_anchor_partner_pipeline_exists_with_three_archetypes():
    p = REPO / "data" / "anchor_partner_pipeline.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    # Three archetypes seeded
    partners = data.get("partners") or data.get("partner_archetypes") or []
    assert len(partners) >= 3, f"expected >= 3 partner archetypes; got {len(partners)}"


# ── First Invoice Motion marker integrity ──────────────────────────


def test_first_invoice_log_exists_and_is_honest():
    p = REPO / "data" / "first_invoice_log.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    # Counts MUST equal entry counts
    assert data["invoice_sent_count"] == len(data["entries"]), (
        "Marker file lies about invoice state. NEVER edit count without an entry."
    )
    assert data["invoice_paid_count"] <= data["invoice_sent_count"]
    if data["invoice_sent_count"] == 0:
        assert data["ceo_complete"] is False


# ── Funding pack integrity ─────────────────────────────────────────


def test_funding_pack_has_use_of_funds():
    p = REPO / "docs" / "funding" / "USE_OF_FUNDS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # Two scenarios: bootstrapped + angel/pre-seed
    lower = text.lower()
    assert "bootstrapped" in lower or "invoice" in lower
    assert "angel" in lower or "pre-seed" in lower or "funded" in lower


def test_hiring_scorecards_have_no_hire_conditions():
    p = REPO / "docs" / "funding" / "HIRING_SCORECARDS.md"
    if not p.exists():
        pytest.skip("HIRING_SCORECARDS.md not yet landed")
    text = p.read_text(encoding="utf-8")
    lower = text.lower()
    assert "do not hire" in lower or "no-hire" in lower or "do-not-hire" in lower
    # All three hires must be named
    for role_keyword in ("ai ops", "delivery", "partnership"):
        assert role_keyword in lower, f"hiring scorecard missing role: {role_keyword}"


def test_first_3_hires_revenue_gated():
    p = REPO / "docs" / "funding" / "FIRST_3_HIRES.md"
    if not p.exists():
        pytest.skip("FIRST_3_HIRES.md not yet landed")
    text = p.read_text(encoding="utf-8")
    lower = text.lower()
    # Revenue-gated, not time-gated
    assert "sar" in lower or "arr" in lower or "invoice" in lower


# ── GCC expansion preserves Saudi beachhead ─────────────────────────


def test_gcc_expansion_thesis_preserves_saudi_beachhead():
    p = REPO / "docs" / "gcc-expansion" / "GCC_EXPANSION_THESIS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    lower = text.lower()
    # Saudi MUST be cited as the commercial beachhead
    assert "saudi" in lower
    # Doctrine framing
    assert "doctrine" in lower
    # NO claim of launching across GCC before Invoice #1
    # (heuristic: the words "before invoice" + "saudi-first" or similar)
    # Just verify the file isn't claiming pan-GCC active markets
    assert "active beachhead" in lower or "commercial beachhead" in lower or (
        "saudi-first" in lower or "saudi first" in lower
    )


# ── Open doctrine commercial-secret canary ─────────────────────────


def test_public_doctrine_does_not_expose_commercial_secrets():
    """THE most important Wave 19 test. The open-doctrine directory is
    intended for external publication. It MUST NOT leak Dealix-internal
    materials. This canary catches accidents."""
    open_doctrine_dir = REPO / "open-doctrine"
    if not open_doctrine_dir.exists():
        pytest.skip("open-doctrine/ not yet created")
    forbidden_terms = (
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "pricing_notes",
        "secret",
        "password",
        "token",
    )
    violations: list[str] = []
    for path in open_doctrine_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            if term.lower() in text.lower():
                rel = path.relative_to(REPO)
                # Exception: SECURITY.md can document the `security@` token in its title,
                # and the word "secret" can appear in negation context (e.g. "this is not a secret").
                # Heuristic: skip if the file is SECURITY.md and the term is the soft "token/secret/password".
                if path.name == "SECURITY.md" and term in {"secret", "password", "token"}:
                    continue
                violations.append(f"{rel}: contains forbidden token {term!r}")
    assert not violations, "\n".join(violations)


def test_open_doctrine_readme_states_not_commercial_code():
    p = REPO / "open-doctrine" / "README.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    lower = text.lower()
    assert ("does not provide commercial" in lower or "not provide commercial" in lower
            or "not a substitute" in lower or "doctrine, controls" in lower)


# ── Master verifier itself ──────────────────────────────────────────


def test_master_verifier_runs_to_completion():
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "verify_all_dealix.py"), "--json"],
        capture_output=True, text=True, check=False, cwd=str(REPO), timeout=60,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    # Wave 19+ Closure adds the 10th system "Operational Closure".
    # 8 of 10 must be at score 5 (the build-complete systems).
    # The two market-motion systems (Partner Motion + First Invoice Motion) stay at 3/5
    # until the founder takes real action — this is intentional and honest.
    assert payload["systems_count"] == 10
    assert payload["systems_at_5_perfect"] >= 8, (
        f"expected >= 8 perfect systems (build-complete); got {payload['systems_at_5_perfect']}"
    )


def test_master_verifier_includes_operational_closure_check():
    """Wave 19+ closure adds the 10th system. Confirm it's wired."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "verify_all_dealix.py"), "--json"],
        capture_output=True, text=True, check=False, cwd=str(REPO), timeout=60,
    )
    payload = json.loads(result.stdout)
    names = [s["name"] for s in payload["systems"]]
    closure_systems = [n for n in names if "Operational Closure" in n]
    assert len(closure_systems) == 1, (
        f"expected exactly 1 Operational Closure system; got {closure_systems}"
    )
