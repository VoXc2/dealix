"""Wave 8 — Customer Signal Synthesis tests."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "dealix_customer_signal_synthesis.py"

import importlib.util
import sys


def _load_module():
    spec = importlib.util.spec_from_file_location("signal_synthesis", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_exists():
    assert SCRIPT_PATH.exists()


def test_no_customers_returns_insufficient_data(monkeypatch, tmp_path):
    mod = _load_module()
    monkeypatch.setattr(mod, "CUSTOMERS_DIR", tmp_path / "nonexistent_customers")
    result = mod.synthesize_signals()
    assert result["status"] == "insufficient_data"


def test_empty_customer_dir_returns_ok(monkeypatch, tmp_path):
    mod = _load_module()
    customers_dir = tmp_path / "customers"
    customers_dir.mkdir()
    (customers_dir / "test-co").mkdir()
    monkeypatch.setattr(mod, "CUSTOMERS_DIR", customers_dir)
    result = mod.synthesize_signals()
    assert result["status"] == "ok"
    assert result["total_signals"] == 0


def test_signals_loaded_from_jsonl(monkeypatch, tmp_path):
    mod = _load_module()
    customers_dir = tmp_path / "customers"
    customers_dir.mkdir()
    handle_dir = customers_dir / "test-co"
    handle_dir.mkdir()
    fr_path = handle_dir / "feature_requests.jsonl"
    fr_path.write_text(
        json.dumps({"customer_handle": "test-co", "request_text": "Need HubSpot integration", "logged_at": "2026-05-07T00:00:00Z", "wave_logged": "wave_8"}) + "\n" +
        json.dumps({"customer_handle": "test-co", "request_text": "WhatsApp automation", "logged_at": "2026-05-07T00:00:00Z", "wave_logged": "wave_8"}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "CUSTOMERS_DIR", customers_dir)
    result = mod.synthesize_signals()
    assert result["status"] == "ok"
    assert result["total_signals"] == 2


def test_classify_crm_request():
    mod = _load_module()
    assert mod.classify_request("I need HubSpot integration") == "crm_integration"


def test_classify_whatsapp_request():
    mod = _load_module()
    assert mod.classify_request("واتساب automation please") == "whatsapp_automation"


def test_classify_unknown_returns_other():
    mod = _load_module()
    assert mod.classify_request("something totally unrelated xyz123") == "other"


def test_report_has_no_pii(monkeypatch, tmp_path):
    mod = _load_module()
    customers_dir = tmp_path / "customers"
    customers_dir.mkdir()
    handle_dir = customers_dir / "test-co"
    handle_dir.mkdir()
    fr_path = handle_dir / "feature_requests.jsonl"
    fr_path.write_text(
        json.dumps({
            "customer_handle": "test-co",
            "request_text": "Need more reports",
            "logged_at": "2026-05-07T00:00:00Z",
        }) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "CUSTOMERS_DIR", customers_dir)
    result = mod.synthesize_signals()
    result_str = json.dumps(result)
    # No phone patterns, no email patterns in report
    import re
    assert not re.search(r"\+966[5][0-9]{8}", result_str)
    assert not re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", result_str)
