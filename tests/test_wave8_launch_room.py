"""Wave 8 — First Customer Launch Room tests."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAUNCH_ROOM = REPO_ROOT / "docs" / "FIRST_CUSTOMER_LAUNCH_ROOM.md"
LAUNCH_ROOM_TEMPLATE = REPO_ROOT / "docs" / "wave8" / "FIRST_CUSTOMER_LAUNCH_ROOM.template.md"

REQUIRED_SECTIONS = [
    "System Status",
    "DPA",
    "Warm Intro",
    "Onboarding Wizard",
    "Integration Plan",
    "Credentials",
    "Payment",
    "Delivery",
    "Proof Pack",
    "Case Study Consent",
    "Customer Signal",
    "GO",
]


def test_launch_room_exists():
    assert LAUNCH_ROOM.exists(), "FIRST_CUSTOMER_LAUNCH_ROOM.md must exist"


def test_launch_room_template_exists():
    assert LAUNCH_ROOM_TEMPLATE.exists(), "FIRST_CUSTOMER_LAUNCH_ROOM.template.md must exist"


def test_launch_room_has_15_sections():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    section_count = content.count("## §")
    assert section_count >= 15, f"Launch room must have 15 sections (§1-§15), found {section_count}"


def test_launch_room_has_required_sections():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"Missing section: {section}"


def test_launch_room_mentions_dpa_gate():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "DPA" in content
    assert "DO NOT proceed" in content or "لا تكمل" in content or "NOT proceed" in content


def test_launch_room_mentions_no_live_charge():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "NO_LIVE_CHARGE" in content or "BLOCKED" in content


def test_launch_room_mentions_no_fake_proof():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "fake" in content.lower() or "مصطنع" in content


def test_launch_room_has_go_no_go():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "GO" in content and "NO-GO" in content


def test_launch_room_has_wizard_command():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "dealix_customer_onboarding_wizard.py" in content


def test_launch_room_has_wave8_verifier_reference():
    content = LAUNCH_ROOM.read_text(encoding="utf-8")
    assert "wave8_customer_ready_verify" in content


def test_template_has_15_sections():
    content = LAUNCH_ROOM_TEMPLATE.read_text(encoding="utf-8")
    # Template uses ## §N or shorter ## §N format
    import re
    sections = re.findall(r"## §\d+", content)
    assert len(sections) >= 15, f"Template must have 15 sections, found {len(sections)}"
