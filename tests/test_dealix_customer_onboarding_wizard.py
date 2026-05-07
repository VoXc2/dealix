"""Wave 7.5 §24.5 — onboarding wizard tests."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path("scripts/dealix_customer_onboarding_wizard.py")


def _run_with_inputs(tmp_path, inputs: dict, *, handle="acme-real-estate", company="Acme Real Estate", sector="real_estate"):
    inputs_file = tmp_path / "inputs.json"
    inputs_file.write_text(json.dumps(inputs), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--customer-handle", handle,
            "--company", company,
            "--sector", sector,
            "--inputs-json", str(inputs_file),
            "--output-base-dir", str(tmp_path / "out"),
        ],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()
    # Must be executable
    assert SCRIPT.stat().st_mode & 0o111


def test_dpa_blocked_refuses(tmp_path) -> None:
    inputs = {"dpa_signed": False}
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 2
    # Don't generate any output if DPA missing
    assert not (tmp_path / "out" / "acme-real-estate" / "integration_plan.md").exists()


def test_happy_path_full_8_channels(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": True, "phone": "+966512345678", "meta_verified": True},
            "email": {"enabled": True},
            "crm": {"enabled": True, "provider": "hubspot"},
            "csv_bulk": {"enabled": True},
            "calendly": {"enabled": True, "link": "calendly.com/sami"},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
        "feature_requests": ["bulk SMS automation"],
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    out = tmp_path / "out" / "acme-real-estate"
    assert (out / "integration_plan.md").exists()
    assert (out / "env_vars_railway.txt").exists()
    assert (out / "customer_portal_token.txt").exists()
    assert (out / "feature_requests.jsonl").exists()
    # Token should be 24+ chars
    token = (out / "customer_portal_token.txt").read_text(encoding="utf-8").strip()
    assert token.startswith("dealix-cust-")
    assert len(token) > 20


def test_minimal_path_only_whatsapp_payment(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": True, "phone": "+966512345678", "meta_verified": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    plan = (tmp_path / "out" / "acme-real-estate" / "integration_plan.md").read_text(encoding="utf-8")
    # Must show enabled channels honestly
    assert "whatsapp" in plan
    assert "approval" in plan


def test_invalid_handle_refused(tmp_path) -> None:
    r = _run_with_inputs(tmp_path, {"dpa_signed": True}, handle="Invalid Handle!")
    assert r.returncode == 2


def test_token_uniqueness_per_run(tmp_path) -> None:
    (tmp_path / "r1").mkdir()
    (tmp_path / "r2").mkdir()
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
    }
    r1 = _run_with_inputs(tmp_path / "r1", inputs)
    r2 = _run_with_inputs(tmp_path / "r2", inputs)
    assert r1.returncode == 0 and r2.returncode == 0
    t1 = (tmp_path / "r1" / "out" / "acme-real-estate" / "customer_portal_token.txt").read_text(encoding="utf-8").strip()
    t2 = (tmp_path / "r2" / "out" / "acme-real-estate" / "customer_portal_token.txt").read_text(encoding="utf-8").strip()
    assert t1 != t2  # tokens are unique per run


def test_no_forbidden_tokens_in_output(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": True, "phone": "+966512345678", "meta_verified": True},
            "email": {"enabled": True},
            "crm": {"enabled": True, "provider": "hubspot"},
            "csv_bulk": {"enabled": True},
            "calendly": {"enabled": True, "link": "calendly.com/sami"},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    plan = (tmp_path / "out" / "acme-real-estate" / "integration_plan.md").read_text(encoding="utf-8")
    # Forbidden token scan
    for pattern in [r"\bguaranteed?\b", r"\bblast\b", "نضمن"]:
        assert not re.search(pattern, plan, re.IGNORECASE), f"forbidden token found: {pattern}"
    # Must explicitly STATE the gates (NO_LIVE_SEND etc.)
    assert "NO_LIVE_SEND" in plan
    assert "NO_LIVE_CHARGE" in plan


def test_payment_method_always_no_live_charge(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "moyasar"},  # even when moyasar selected
            "approval": {"ok": True},
        },
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    plan = (tmp_path / "out" / "acme-real-estate" / "integration_plan.md").read_text(encoding="utf-8")
    # No live charge regardless of method choice
    assert "live_charge: False" in plan or "live_charge:** False" in plan


def test_feature_request_logged_to_jsonl(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": False},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
        "feature_requests": ["bulk SMS automation", "integration with Telegram"],
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    fr_path = tmp_path / "out" / "acme-real-estate" / "feature_requests.jsonl"
    lines = fr_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    for line in lines:
        record = json.loads(line)
        assert record["customer_handle"] == "acme-real-estate"
        assert record["wave_logged"] == "wave_7_5"
        assert "logged_at" in record


def test_env_vars_no_real_secrets(tmp_path) -> None:
    inputs = {
        "dpa_signed": True,
        "channels": {
            "whatsapp": {"enabled": True, "phone": "+966512345678", "meta_verified": True},
            "email": {"enabled": False},
            "crm": {"enabled": False},
            "csv_bulk": {"enabled": False},
            "calendly": {"enabled": False},
            "payment": {"method": "bank"},
            "approval": {"ok": True},
        },
    }
    r = _run_with_inputs(tmp_path, inputs)
    assert r.returncode == 0
    env_text = (tmp_path / "out" / "acme-real-estate" / "env_vars_railway.txt").read_text(encoding="utf-8")
    # placeholder, never real keys
    assert "<paste-from-meta>" in env_text
    # No leaked patterns
    for pat in [r"sk_live_[A-Za-z0-9]{8,}", r"AIza[A-Za-z0-9]{30,}", r"ghp_[A-Za-z0-9]{30,}"]:
        assert not re.search(pat, env_text), f"leaked: {pat}"
