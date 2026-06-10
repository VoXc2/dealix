"""Wave 12.6 §33.2.6 — BOPLA field redaction tests.

Validates the OWASP API3:2023 BOPLA defense:
- Sensitive field categories: PII_email, PII_phone, PII_id, financial,
  secret, internal_audit
- Per-role visibility matrix (8 roles)
- redact_dict_for_role: filters nested payloads, preserves non-sensitive
- assert_no_sensitive_field_in_response: defensive double-check

Pure-function tests. Loaded via importlib to bypass api/security init.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# Bypass api/middleware/__init__.py to avoid future import surprises.
_REPO_ROOT = Path(__file__).resolve().parents[1]
_BOPLA_PATH = _REPO_ROOT / "api" / "middleware" / "bopla_redaction.py"
_spec = importlib.util.spec_from_file_location("bopla_redaction", _BOPLA_PATH)
_bopla = importlib.util.module_from_spec(_spec)
sys.modules["bopla_redaction"] = _bopla
_spec.loader.exec_module(_bopla)

RedactionResult = _bopla.RedactionResult
SENSITIVE_FIELD_CATEGORIES = _bopla.SENSITIVE_FIELD_CATEGORIES
assert_no_sensitive_field_in_response = _bopla.assert_no_sensitive_field_in_response
fields_blocked_for_role = _bopla.fields_blocked_for_role
redact_dict_for_role = _bopla.redact_dict_for_role


# ─────────────────────────────────────────────────────────────────────
# Field categories + visibility matrix (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_sensitive_categories_complete() -> None:
    """6 canonical categories present with non-empty field sets."""
    expected_cats = {"PII_email", "PII_phone", "PII_id", "financial",
                     "secret", "internal_audit"}
    assert expected_cats <= set(SENSITIVE_FIELD_CATEGORIES.keys())
    for cat, fields in SENSITIVE_FIELD_CATEGORIES.items():
        assert fields, f"category {cat} has no fields"


def test_anonymous_blocks_everything_sensitive() -> None:
    """Anonymous role sees nothing sensitive."""
    blocked = fields_blocked_for_role("anonymous")
    # Should include at least one field from each sensitive category
    assert "personal_email" in blocked
    assert "phone" in blocked
    assert "bank_account" in blocked
    assert "password" in blocked


def test_super_admin_sees_pii_but_not_secrets() -> None:
    """Super admin can see PII (debug) but never raw secrets."""
    blocked = fields_blocked_for_role("super_admin")
    assert "password" in blocked  # secrets blocked
    assert "personal_email" not in blocked  # PII allowed for super admin
    assert "bank_account" not in blocked  # financial allowed for super admin


def test_unknown_role_default_denies_all() -> None:
    """Unknown role → block every sensitive field (Article 4 fail-closed)."""
    blocked = fields_blocked_for_role("totally_made_up_role")  # type: ignore[arg-type]
    # Should block from every category
    assert "personal_email" in blocked
    assert "bank_account" in blocked
    assert "password" in blocked
    assert "internal_notes" in blocked


# ─────────────────────────────────────────────────────────────────────
# redact_dict_for_role (5 tests)
# ─────────────────────────────────────────────────────────────────────


def test_redact_replaces_blocked_fields_with_marker() -> None:
    """Blocked field gets replaced with [REDACTED] marker."""
    payload = {"name": "Acme", "email": "x@y.com", "personal_email": "secret@y.com"}
    result = redact_dict_for_role(payload, role="viewer")
    assert result.redacted_payload["name"] == "Acme"
    assert result.redacted_payload["email"] == "x@y.com"  # not in blocklist
    assert result.redacted_payload["personal_email"] == "[REDACTED]"
    assert "personal_email" in result.fields_redacted
    assert result.redacted_count >= 1


def test_redact_recurses_into_nested_dicts() -> None:
    """Sensitive fields in nested dicts also get redacted."""
    payload = {
        "name": "Acme",
        "billing": {
            "iban": "SA12345",
            "bank_account": "9999",
            "currency": "SAR",
        },
    }
    result = redact_dict_for_role(payload, role="viewer")
    assert result.redacted_payload["billing"]["iban"] == "[REDACTED]"
    assert result.redacted_payload["billing"]["bank_account"] == "[REDACTED]"
    assert result.redacted_payload["billing"]["currency"] == "SAR"


def test_redact_recurses_into_lists() -> None:
    """Sensitive fields in lists of dicts get redacted."""
    payload = {
        "contacts": [
            {"name": "Sami", "phone": "+966555"},
            {"name": "Ahmed", "phone": "+966666"},
        ],
    }
    result = redact_dict_for_role(payload, role="viewer")
    for contact in result.redacted_payload["contacts"]:
        assert contact["phone"] == "[REDACTED]"
        assert contact["name"] in ("Sami", "Ahmed")  # name preserved


def test_redact_finance_role_can_see_bank_account() -> None:
    """Finance role can see financial fields (their job)."""
    payload = {"customer": "acme", "bank_account": "SA12345", "iban": "SA98765"}
    result = redact_dict_for_role(payload, role="finance")
    # Finance can see bank_account + iban
    assert result.redacted_payload["bank_account"] == "SA12345"
    assert result.redacted_payload["iban"] == "SA98765"


def test_redact_extra_blocked_fields_per_endpoint() -> None:
    """Caller can pass extra_blocked_fields for endpoint-specific extras."""
    payload = {"name": "Acme", "internal_score": 0.85, "public_metric": 100}
    result = redact_dict_for_role(
        payload, role="tenant_admin",
        extra_blocked_fields=("internal_score",),
    )
    # internal_score not in canonical list; extra_blocked applies
    assert result.redacted_payload["internal_score"] == "[REDACTED]"
    assert result.redacted_payload["public_metric"] == 100


# ─────────────────────────────────────────────────────────────────────
# assert_no_sensitive_field_in_response defensive guard (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_assert_passes_on_redacted_payload() -> None:
    """After redaction, defensive guard passes."""
    payload = {"name": "Acme", "email": "x@y.com"}
    result = redact_dict_for_role(payload, role="viewer")
    # Should not raise — no sensitive fields present (only "email" which
    # isn't in the canonical PII_email set)
    assert_no_sensitive_field_in_response(result.redacted_payload, role="viewer")


def test_assert_raises_on_leaked_field() -> None:
    """If caller forgot to redact and a sensitive field leaked → raise."""
    payload = {"name": "Acme", "personal_email": "leaked@example.com"}
    # Notice: NO redaction applied
    with pytest.raises(AssertionError, match="BOPLA leak"):
        assert_no_sensitive_field_in_response(payload, role="viewer")


def test_assert_recurses_into_nested() -> None:
    """Defensive guard catches leaks in nested dicts."""
    payload = {
        "name": "Acme",
        "contacts": [{"name": "X", "personal_email": "leaked@example.com"}],
    }
    with pytest.raises(AssertionError, match="BOPLA leak"):
        assert_no_sensitive_field_in_response(payload, role="viewer")


# ─────────────────────────────────────────────────────────────────────
# Total: 12 tests (4 categories + 5 redact + 3 defensive)
# ─────────────────────────────────────────────────────────────────────
