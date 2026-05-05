"""Hard rule: PII redaction must catch Saudi/Gulf phones, emails,
and Saudi national IDs. False positives ok; false negatives are
PDPL-fineable.

Tests `auto_client_acquisition.customer_data_plane.pii_redactor` —
the same redactor wired into `proof_ledger` exports."""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_dict,
    redact_email,
    redact_phone,
    redact_saudi_id,
    redact_text,
)


def test_redact_email_basic():
    assert "ali@example.sa" not in redact_text("contact ali@example.sa today")
    out = redact_text("contact ali@example.sa")
    assert "@example.sa" in out  # domain preserved
    assert "ali@" not in out


def test_redact_email_preserves_domain_only():
    assert redact_email("user@dealix.me") == "u***@dealix.me"


def test_redact_saudi_phone_966_form():
    text = "contact me at +966501234567 anytime"
    out = redact_text(text)
    assert "501234567" not in out
    assert "REDACTED_PHONE" in out


def test_redact_saudi_phone_local_05_form():
    text = "or via 0501234567"
    out = redact_text(text)
    assert "0501234567" not in out
    assert "REDACTED_PHONE" in out


def test_redact_saudi_national_id():
    text = "ID 1012345678 verified"
    out = redact_text(text)
    assert "1012345678" not in out
    assert "REDACTED_ID" in out


def test_redact_dict_recurses():
    payload = {
        "customer": {
            "email": "ali@example.sa",
            "phone": "+966501234567",
            "notes": "ID 2012345678 confirmed",
        },
        "tags": ["contact ali@example.sa", "phone +966501234567"],
    }
    out = redact_dict(payload)
    flat = repr(out)
    assert "ali@example.sa" not in flat
    assert "+966501234567" not in flat
    assert "2012345678" not in flat


def test_redact_does_not_mutate_input():
    text = "ali@example.sa +966501234567 ID 2012345678"
    redact_text(text)
    # Original string unchanged
    assert "ali@example.sa" in text
    assert "501234567" in text


def test_redact_text_handles_non_string():
    """Non-string input passes through (e.g. None, dict from upstream)."""
    assert redact_text(None) is None
    assert redact_text(42) == 42
