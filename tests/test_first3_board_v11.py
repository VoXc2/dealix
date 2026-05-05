"""V11 Phase 5 — first-3 board generator tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_first3_board.py"


def test_script_exists_and_is_executable() -> None:
    assert SCRIPT.exists(), "scripts/dealix_first3_board.py is missing"


def test_dry_run_prints_markdown_and_json(capsys) -> None:
    out = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "=== Markdown ===" in out.stdout
    assert "=== JSON ===" in out.stdout
    assert "Phase E" in out.stdout
    assert "Slot-A" in out.stdout
    assert "Slot-B" in out.stdout
    assert "Slot-C" in out.stdout


def test_writes_files_to_output_dir(tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    md = tmp_path / "FIRST_3_CUSTOMER_BOARD.md"
    js = tmp_path / "FIRST_3_CUSTOMER_BOARD.json"
    assert md.exists()
    assert js.exists()


def test_json_output_has_required_fields(tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads((tmp_path / "FIRST_3_CUSTOMER_BOARD.json").read_text())
    assert data["schema_version"] == 1
    assert len(data["slots"]) == 3
    required_slot_fields = {
        "slot_id", "company_name", "contact_name", "relationship",
        "sector", "region", "source", "consent_status",
        "first_message_status", "diagnostic_status", "pilot_status",
        "proof_status", "next_action", "owner", "notes",
    }
    for slot in data["slots"]:
        missing = required_slot_fields - set(slot.keys())
        assert not missing, f"slot missing fields: {missing}"
    assert data["hard_gates"]["no_live_send"] is True
    assert data["hard_gates"]["no_live_charge"] is True
    assert data["hard_gates"]["no_scraping"] is True


def test_no_real_customer_data_in_output(tmp_path: Path) -> None:
    """Output must contain only placeholders."""
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    md = (tmp_path / "FIRST_3_CUSTOMER_BOARD.md").read_text()
    # No real-looking emails, phone numbers, or proper-noun company names
    assert "@" not in md
    assert "+966" not in md
    # Slot placeholders MUST be present
    assert "Slot-A" in md
    assert "Slot-B" in md
    assert "Slot-C" in md
