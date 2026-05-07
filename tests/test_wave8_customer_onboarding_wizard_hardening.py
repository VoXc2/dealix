"""Wave 8 §7 — Onboarding Wizard Hardening tests."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIZARD_PATH = REPO_ROOT / "scripts" / "dealix_customer_onboarding_wizard.py"


def _load_wizard():
    spec = importlib.util.spec_from_file_location("wizard", WIZARD_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_wizard_exists():
    assert WIZARD_PATH.exists(), "dealix_customer_onboarding_wizard.py must exist"


def test_wizard_has_dry_run_flag():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "--dry-run" in content, "Wizard must have --dry-run flag"
    assert "dry_run" in content, "Wizard must handle dry_run attribute"


def test_wizard_has_no_token_print_flag():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "--no-token-print" in content, "Wizard must have --no-token-print flag"


def test_wizard_has_redact_flag():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "--redact" in content, "Wizard must have --redact flag"


def test_wizard_has_language_flag():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "--language" in content, "Wizard must have --language flag"


def test_wizard_has_output_dir_flag():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "--output-dir" in content, "Wizard must have --output-dir flag"


def test_wizard_has_sector_validation():
    content = WIZARD_PATH.read_text(encoding="utf-8")
    assert "VALID_SECTORS" in content, "Wizard must have VALID_SECTORS list"
    mod = _load_wizard()
    assert hasattr(mod, "VALID_SECTORS"), "VALID_SECTORS must be accessible"
    assert "real_estate" in mod.VALID_SECTORS
    assert len(mod.VALID_SECTORS) >= 8


def test_wizard_dry_run_does_not_write_files(tmp_path):
    """--dry-run must not create any files."""
    mod = _load_wizard()

    # Simulate sys.argv for dry-run
    test_argv = [
        "wizard",
        "--customer-handle", "test-handle",
        "--company", "Test Co",
        "--sector", "real_estate",
        "--dry-run",
        "--output-dir", str(tmp_path / "output"),
    ]
    orig_argv = sys.argv
    try:
        sys.argv = test_argv
        result = mod.main()
        assert result == 0
        # No files should have been created
        output_dir = tmp_path / "output"
        assert not output_dir.exists(), "dry-run must not create output directory"
    finally:
        sys.argv = orig_argv


def test_wizard_language_en_accepted(tmp_path, monkeypatch):
    """--language en should be accepted without error."""
    mod = _load_wizard()
    inputs_file = tmp_path / "inputs.json"
    inputs_file.write_text(json.dumps({
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
        },
        "feature_requests": [],
    }), encoding="utf-8")

    test_argv = [
        "wizard",
        "--customer-handle", "test-en",
        "--company", "Test EN",
        "--sector", "services",
        "--inputs-json", str(inputs_file),
        "--language", "en",
        "--output-dir", str(tmp_path / "out"),
    ]
    orig_argv = sys.argv
    try:
        sys.argv = test_argv
        result = mod.main()
        assert result == 0
    finally:
        sys.argv = orig_argv


def test_wizard_dpa_gate_blocks_without_consent(tmp_path, monkeypatch):
    """Wizard must refuse (exit 2) if dpa_signed=False."""
    mod = _load_wizard()
    inputs_file = tmp_path / "inputs.json"
    inputs_file.write_text(json.dumps({
        "dpa_signed": False,
    }), encoding="utf-8")

    test_argv = [
        "wizard",
        "--customer-handle", "blocked-handle",
        "--company", "Blocked Co",
        "--sector", "real_estate",
        "--inputs-json", str(inputs_file),
        "--output-dir", str(tmp_path / "out"),
    ]
    orig_argv = sys.argv
    try:
        sys.argv = test_argv
        result = mod.main()
        assert result == 2, "Must return exit code 2 when DPA not signed"
    finally:
        sys.argv = orig_argv


def test_wizard_no_token_print_flag_suppresses_token(tmp_path, capsys, monkeypatch):
    """--no-token-print must not print the actual token to stdout."""
    mod = _load_wizard()
    inputs_file = tmp_path / "inputs.json"
    inputs_file.write_text(json.dumps({
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
        },
        "feature_requests": [],
    }), encoding="utf-8")

    test_argv = [
        "wizard",
        "--customer-handle", "notoken-co",
        "--company", "NoToken Co",
        "--sector", "agencies",
        "--inputs-json", str(inputs_file),
        "--no-token-print",
        "--output-dir", str(tmp_path / "out"),
    ]
    orig_argv = sys.argv
    try:
        sys.argv = test_argv
        mod.main()
        captured = capsys.readouterr()
        # Token should be hidden in output
        assert "dealix-cust-" not in captured.out, \
            "Token must not appear in stdout when --no-token-print is used"
    finally:
        sys.argv = orig_argv


def test_wizard_output_files_generated(tmp_path, monkeypatch):
    """Wizard must generate 4 output files in the output directory."""
    mod = _load_wizard()
    inputs_file = tmp_path / "inputs.json"
    inputs_file.write_text(json.dumps({
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": True, "phone": "+966512345678", "meta_verified": False},
            "email": {"enabled": True},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
        },
        "feature_requests": ["Better reporting"],
    }), encoding="utf-8")

    out_dir = tmp_path / "customer_output"
    test_argv = [
        "wizard",
        "--customer-handle", "output-test-co",
        "--company", "Output Test Co",
        "--sector", "real_estate",
        "--inputs-json", str(inputs_file),
        "--output-dir", str(out_dir),
    ]
    orig_argv = sys.argv
    try:
        sys.argv = test_argv
        result = mod.main()
        assert result == 0
        assert (out_dir / "integration_plan.md").exists()
        assert (out_dir / "env_vars_railway.txt").exists()
        assert (out_dir / "customer_portal_token.txt").exists()
        assert (out_dir / "feature_requests.jsonl").exists()
    finally:
        sys.argv = orig_argv
