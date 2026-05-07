"""Wave 8 — Customer Credential Readiness Check tests."""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "dealix_customer_credentials_check.py"
EXAMPLE_ENV = REPO_ROOT / "docs" / "wave8" / "customer_credentials.example.env"
READINESS_MD = REPO_ROOT / "docs" / "WAVE8_CUSTOMER_CREDENTIAL_READINESS.md"

# Dynamically import the script module
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _load_module():
    spec = importlib.util.spec_from_file_location("creds_check", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_exists():
    assert SCRIPT_PATH.exists(), "dealix_customer_credentials_check.py must exist"


def test_example_env_exists():
    assert EXAMPLE_ENV.exists(), "customer_credentials.example.env must exist"


def test_readiness_md_exists():
    assert READINESS_MD.exists(), "WAVE8_CUSTOMER_CREDENTIAL_READINESS.md must exist"


def test_moyasar_always_blocked():
    mod = _load_module()
    status = mod.check_credential("MOYASAR_SECRET_KEY", "blocked_by_policy")
    assert status == "BLOCKED_BY_POLICY"


def test_missing_required_returns_missing():
    mod = _load_module()
    with patch.dict(os.environ, {}, clear=False):
        # Ensure key is absent
        env = {k: v for k, v in os.environ.items() if k != "FAKE_WAVE8_MISSING_KEY"}
        with patch.dict(os.environ, env, clear=True):
            status = mod.check_credential("FAKE_WAVE8_MISSING_KEY", "required")
    assert status == "MISSING"


def test_present_required_returns_present():
    mod = _load_module()
    with patch.dict(os.environ, {"TEST_WAVE8_KEY": "some_value"}):
        status = mod.check_credential("TEST_WAVE8_KEY", "required")
    assert status == "PRESENT"


def test_missing_optional_returns_demo_fallback():
    mod = _load_module()
    env = {k: v for k, v in os.environ.items() if k != "FAKE_WAVE8_OPTIONAL_KEY"}
    with patch.dict(os.environ, env, clear=True):
        status = mod.check_credential("FAKE_WAVE8_OPTIONAL_KEY", "optional")
    assert status == "DEMO_FALLBACK"


def test_mask_never_returns_full_value():
    mod = _load_module()
    result = mod._mask("sk_live_super_secret_key_12345")
    assert "sk_live_super_secret" not in result
    assert result.startswith("***")


def test_example_env_has_no_real_secrets():
    content = EXAMPLE_ENV.read_text(encoding="utf-8")
    # Must not contain real-looking API key patterns
    assert "sk_live_" not in content
    assert "sk-ant-api" not in content
    # Should contain REPLACE_ME or OPTIONAL markers
    assert "REPLACE_ME" in content or "OPTIONAL" in content


def test_readiness_md_mentions_hard_rules():
    content = READINESS_MD.read_text(encoding="utf-8")
    assert "BLOCKED_BY_POLICY" in content
    assert "NO_LIVE_CHARGE" in content
    assert "NEVER" in content


def test_credentials_list_has_moyasar_blocked():
    mod = _load_module()
    moyasar_entries = [c for c in mod.CREDENTIALS if "MOYASAR" in c[0]]
    for entry in moyasar_entries:
        assert entry[2] == "blocked_by_policy", f"{entry[0]} must be blocked_by_policy"
