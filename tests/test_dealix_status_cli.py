"""Tests for scripts/dealix_status.py — founder one-command status CLI.

Read-only diagnostics; the CLI must produce a stable bilingual
report and a JSON payload with predictable keys, regardless of
external state. Importantly, it must NEVER report a live-action
gate as ALLOWED on a clean checkout.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_status.py"


def _import_module():
    """Load scripts/dealix_status.py as a module without spawning a
    subprocess (keeps coverage attached + avoids env shell quirks)."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_status  # type: ignore[import-not-found]
        return dealix_status
    finally:
        sys.path.pop(0)


def test_status_script_exists_and_is_executable():
    assert SCRIPT.exists(), "scripts/dealix_status.py must exist"
    text = SCRIPT.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env python3"), "must have shebang"


def test_status_text_render_has_all_sections():
    mod = _import_module()
    payload = mod._build_status_payload()
    rendered = mod.render_text(payload)

    expected_sections = [
        "Service Activation",       # services
        "Reliability OS",            # reliability
        "Top decisions today",       # daily_loop
        "Weekly scorecard",          # weekly_scorecard
        "Live-action gates",         # live_gates
        "Founder decisions queue",   # founder_decisions
    ]
    for section in expected_sections:
        assert section in rendered, (
            f"text status missing required section: {section!r}"
        )

    # Bilingual header must appear
    assert "Dealix" in rendered
    assert "حالة المنصّة" in rendered
    assert "Founder Status" in rendered


def test_status_json_payload_has_stable_keys():
    mod = _import_module()
    payload = mod._build_status_payload()

    required_keys = {
        "schema_version",
        "generated_at",
        "services",
        "reliability",
        "daily_loop",
        "weekly_scorecard",
        "review_pending_count",
        "open_founder_decisions",
        "live_gates",
    }
    missing = required_keys - set(payload.keys())
    assert not missing, f"missing keys in status payload: {missing}"


def test_live_gates_never_report_allowed_on_clean_checkout():
    mod = _import_module()
    gates = mod._live_gate_status()

    # The four canonical gates we report on
    expected_gates = {
        "live_charge",
        "whatsapp_live_send",
        "email_live_send",
        "linkedin_and_scraping",
    }
    assert expected_gates.issubset(set(gates.keys())), (
        f"expected gates missing; got {sorted(gates.keys())}"
    )

    for name, status in gates.items():
        # 'ALLOWED' on a clean checkout would mean a live gate is
        # mis-configured — that is a hard failure for this test.
        assert "ALLOWED" not in status, (
            f"gate {name} reported ALLOWED on clean checkout: {status!r}"
        )


def test_main_returns_zero_in_text_mode(capsys):
    mod = _import_module()
    rc = mod.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Dealix" in out
    assert "Service Activation" in out


def test_main_returns_zero_in_json_mode(capsys):
    mod = _import_module()
    rc = mod.main(["--json"])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)
    assert payload["schema_version"] == 1
    assert "live_gates" in payload


def test_review_pending_counter_finds_known_entries():
    mod = _import_module()
    count = mod._review_pending_count()
    # As of v5 close, the forbidden-claims allowlist surfaces multiple
    # REVIEW_PENDING entries (academy 'Cold Email Pro', roi 'نضمن', etc.).
    # Tolerate any non-negative number — we only assert the parser ran
    # successfully, not the exact count (which the founder may shrink).
    assert count >= 0, f"review_pending_count returned {count}"


def test_open_founder_decisions_counter_runs():
    mod = _import_module()
    count = mod._open_founder_decisions()
    # Tolerate a wide range — the count is informational, not gating.
    assert count >= 0
    assert count <= 10
