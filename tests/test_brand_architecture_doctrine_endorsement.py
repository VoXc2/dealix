"""Every Dealix Group public surface page must display the doctrine
endorsement line: a link to `/api/v1/doctrine?version=` somewhere in
the page (footer counts).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Pages that represent the Dealix Group public surface (added across
# Wave 22). HTML files outside this list are not required to carry the
# endorsement (they may be partner-kit templates with placeholders,
# legacy pages, etc.).
GROUP_PUBLIC_PAGES = (
    "landing/group.html",
    "landing/founder-command-center.html",  # operator-facing but still doctrine-anchored
)


def test_every_group_public_page_links_to_versioned_doctrine():
    rx = re.compile(r"/api/v1/doctrine\?version=v\d+\.\d+\.\d+")
    missing = []
    for rel in GROUP_PUBLIC_PAGES:
        p = REPO_ROOT / rel
        assert p.exists(), f"{rel} should exist"
        text = p.read_text(encoding="utf-8")
        if not rx.search(text):
            missing.append(rel)
    assert not missing, f"missing versioned doctrine endorsement on: {missing}"


def test_brand_architecture_doc_exists():
    assert (REPO_ROOT / "docs" / "brand" / "BRAND_ARCHITECTURE.md").exists()
    assert (REPO_ROOT / "docs" / "brand" / "MASTER_BRAND.md").exists()
    assert (REPO_ROOT / "docs" / "brand" / "SUB_BRAND_RULES.md").exists()


def test_brand_architecture_lists_dealix_group_naming_rule():
    text = (REPO_ROOT / "docs" / "brand" / "BRAND_ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "Dealix" in text
    assert "Dealix Group" in text
    assert "Dealix Core OS" in text


def test_sub_brand_rules_enforce_doctrine_pinning():
    text = (REPO_ROOT / "docs" / "brand" / "SUB_BRAND_RULES.md").read_text(encoding="utf-8")
    assert "doctrine version" in text.lower() or "doctrine pinning" in text.lower()
    # Must mention every visible lifecycle state.
    for state in ("BUILD", "PILOT", "SCALE", "HOLD", "KILL", "SPINOUT"):
        assert state in text, f"SUB_BRAND_RULES.md missing lifecycle state: {state}"


def test_partner_kit_has_holding_brand_note():
    p = REPO_ROOT / "partner-kit" / "branding" / "HOLDING_BRAND_NOTE.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # Partner page should NOT use the holding parent as primary mark.
    assert "primary" in text.lower()
    assert "secondary" in text.lower()
