"""Tests for the partner kit — content + zip stability + doctrine adoption."""
from __future__ import annotations

import importlib.util
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
KIT_DIR = REPO_ROOT / "partner-kit"
ZIP_PATH = REPO_ROOT / "landing" / "assets" / "downloads" / "dealix-partner-kit-v1.zip"


def test_partner_kit_directory_has_required_files():
    required = [
        "README.md",
        "TRUST_PACK_TEMPLATE.md",
        "PROOF_PACK_TEMPLATE.md",
        "DOCTRINE_ADOPTION_CHECKLIST.md",
        "branding/COLORS.md",
        "branding/LOGO_USAGE.md",
        "landing-template/index.html",
    ]
    for rel in required:
        p = KIT_DIR / rel
        assert p.exists(), f"missing partner-kit file: {rel}"


def test_doctrine_adoption_checklist_contains_eleven_non_negotiables():
    text = (KIT_DIR / "DOCTRINE_ADOPTION_CHECKLIST.md").read_text(encoding="utf-8")
    # 11 checkboxes for the eleven commitments.
    boxes = text.count("- [ ]")
    assert boxes >= 11, f"expected >= 11 checkboxes, found {boxes}"

    must_contain = [
        "Source Passport before AI use",
        "Human approval before external action",
        "Governance Runtime before client-facing output",
        "Proof Pack before any claim",
        "No scraping",
        "No cold WhatsApp",
        "No LinkedIn automation",
        "No guaranteed sales claims",
        "No agent without identity",
        "Capital Asset registration before invoice",
        "Verifiable, not merely trusted",
    ]
    for s in must_contain:
        assert s in text, f"adoption checklist missing: {s!r}"


def test_partner_kit_zip_exists_and_is_nonempty():
    assert ZIP_PATH.exists(), "partner kit zip missing; run scripts/build_partner_kit_zip.py"
    assert ZIP_PATH.stat().st_size > 1000


def test_partner_kit_zip_is_byte_stable(tmp_path):
    """Re-building from the same source produces identical bytes."""
    _SCRIPT = REPO_ROOT / "scripts" / "build_partner_kit_zip.py"
    spec = importlib.util.spec_from_file_location("build_partner_kit_zip_mod", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    out1 = tmp_path / "kit1.zip"
    out2 = tmp_path / "kit2.zip"
    mod.build(out1)
    mod.build(out2)
    assert out1.read_bytes() == out2.read_bytes()


def test_partner_kit_zip_contains_all_required_files():
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = set(zf.namelist())
    required = [
        "partner-kit/README.md",
        "partner-kit/TRUST_PACK_TEMPLATE.md",
        "partner-kit/PROOF_PACK_TEMPLATE.md",
        "partner-kit/DOCTRINE_ADOPTION_CHECKLIST.md",
        "partner-kit/branding/COLORS.md",
        "partner-kit/branding/LOGO_USAGE.md",
        "partner-kit/landing-template/index.html",
    ]
    for r in required:
        assert r in names, f"zip missing: {r}"


def test_partner_kit_landing_template_uses_doctrine_link():
    text = (KIT_DIR / "landing-template" / "index.html").read_text(encoding="utf-8")
    assert "/api/v1/doctrine" in text
    assert "v1.0.0" in text
