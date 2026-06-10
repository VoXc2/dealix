"""Phase 2 — integration_upgrade adapter shim tests.

Asserts:
- safe_import returns None for unknown modules (never raises)
- safe_call catches BaseException and returns degraded
- hide_internal_terms strips v11/v12/v13/v14/router/verifier/growth_beast
- customer_safe_label returns Arabic + English
- no secrets in any output
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.integration_upgrade import (
    contract_status,
    customer_safe_label,
    degraded_section,
    hide_internal_terms,
    safe_call,
    safe_import,
)


def test_safe_import_unknown_returns_none() -> None:
    assert safe_import("module.that.does.not.exist") is None
    assert safe_import("auto_client_acquisition.nonexistent_module") is None


def test_safe_import_existing_returns_module() -> None:
    mod = safe_import("auto_client_acquisition.full_ops_contracts")
    assert mod is not None
    assert hasattr(mod, "schemas")


def test_safe_call_returns_value_on_success() -> None:
    result = safe_call(name="test_section", fn=lambda: {"ok": True})
    assert result == {"ok": True}


def test_safe_call_returns_degraded_on_exception() -> None:
    def boom():
        raise ValueError("simulated failure with secret_key=abc123")
    result = safe_call(name="boom_section", fn=boom)
    assert result["degraded"] is True
    assert result["section"] == "boom_section"
    assert "secret_key" not in str(result)
    assert "abc123" not in str(result)
    # Type name OK to leak (just exception class), no message
    assert "ValueError" in str(result)


def test_safe_call_returns_fallback_when_provided() -> None:
    def boom():
        raise RuntimeError("nope")
    result = safe_call(name="x", fn=boom, fallback={"safe": "fallback"})
    assert result == {"safe": "fallback"}


def test_safe_call_catches_keyboard_interrupt() -> None:
    """BaseException-level catch — even KeyboardInterrupt gets caught."""
    def boom():
        raise KeyboardInterrupt()
    result = safe_call(name="kb", fn=boom)
    assert result["degraded"] is True


def test_hide_internal_terms_strips_all_internal_names() -> None:
    text = "We use v12 router with verifier and growth_beast plus v14 stacktrace"
    cleaned = hide_internal_terms(text)
    assert "v12" not in cleaned
    assert "router" not in cleaned
    assert "verifier" not in cleaned
    assert "growth_beast" not in cleaned
    assert "v14" not in cleaned
    assert "stacktrace" not in cleaned
    assert "[—]" in cleaned


def test_hide_internal_terms_case_insensitive() -> None:
    cleaned = hide_internal_terms("V12 ROUTER and Verifier")
    assert "[—]" in cleaned
    # All variants should be scrubbed
    assert "V12" not in cleaned
    assert "ROUTER" not in cleaned
    assert "Verifier" not in cleaned


def test_hide_internal_terms_handles_empty() -> None:
    assert hide_internal_terms("") == ""
    assert hide_internal_terms("safe text") == "safe text"


def test_customer_safe_label_known_module() -> None:
    label = customer_safe_label("leadops_spine")
    assert label["label_ar"] == "تأهيل الفرص"
    assert label["label_en"] == "Opportunity qualification"
    assert label["source_internal"] == "leadops_spine"


def test_customer_safe_label_unknown_returns_generic() -> None:
    label = customer_safe_label("some_random_internal_module_xyz")
    assert "label_ar" in label
    assert "label_en" in label
    # Must not echo the internal name to customer
    assert "some_random_internal_module_xyz" not in label["label_ar"]
    assert "some_random_internal_module_xyz" not in label["label_en"]


def test_degraded_section_shape() -> None:
    d = degraded_section(
        section="x", reason_ar="غير متاح", reason_en="not available",
        next_fix_ar="افعّل الوحدة", next_fix_en="enable module",
    )
    assert d["degraded"] is True
    assert d["severity"] == "medium"
    assert d["safety_summary"] == "no_500_no_internal_leak"


def test_contract_status_shape() -> None:
    c = contract_status(name="leadops", available=True)
    assert c["available"] is True
    assert c["degraded"] is False
    assert c["blockers"] == []


def test_no_secrets_in_safe_call_output() -> None:
    """Any leaked secret patterns from raised exceptions are scrubbed."""
    secret = "sk_live_AbCdEf1234567890"
    def leaky():
        raise ValueError(f"failure with {secret}")
    result = safe_call(name="leaky", fn=leaky)
    assert secret not in str(result)
