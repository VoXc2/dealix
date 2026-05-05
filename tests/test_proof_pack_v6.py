"""Proof Pack v6 standard — pack rendering + HMAC metadata signing.

These tests pin the v6 contract:
  - render_pack always returns ``approval_required`` (even with consent)
  - mixed-consent → ``audience = internal_only``
  - all-consented → ``audience = public_with_consent`` + still
    ``approval_required``
  - any forbidden token in any event → whole pack BLOCKED
  - ``hmac_signing.sign_pack_metadata`` returns 64-char hex when a
    secret is given, ``"UNSIGNED"`` when None
  - same payload + secret → stable digest across calls
"""
from __future__ import annotations

from auto_client_acquisition.proof_ledger import hmac_signing
from auto_client_acquisition.self_growth_os import proof_snippet_engine


_GOOD_EVENT_INTERNAL = {
    "event_type": "pilot_delivered",
    "service_id": "growth_starter",
    "outcome_metric": "qualified_opportunities",
    "outcome_value": 14,
    "sla_period_days": 7,
    "consent_for_publication": False,
    "customer_anonymized": "Slot-A",
}

_GOOD_EVENT_PUBLIC = {
    "event_type": "pilot_delivered",
    "service_id": "growth_starter",
    "outcome_metric": "drafts_approved",
    "outcome_value": 22,
    "sla_period_days": 7,
    "consent_for_publication": True,
    "customer_display_name": "Slot-A",
}


# ─── render_pack contract ───────────────────────────────────────────


def test_render_pack_returns_approval_required_even_with_consent() -> None:
    """A pack with every event consented still requires founder approval."""
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_PUBLIC, _GOOD_EVENT_PUBLIC],
        customer_handle="Slot-A",
    )
    assert pack["approval_status"] == "approval_required"
    assert pack["decision"] == "allowed_draft"


def test_internal_only_pack_when_any_consent_false() -> None:
    """Mixed-consent pack falls back to ``internal_only`` audience."""
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL, _GOOD_EVENT_PUBLIC],
        customer_handle="Slot-A",
    )
    assert pack["audience"] == "internal_only"
    assert pack["decision"] == "allowed_draft"
    # Approval still required.
    assert pack["approval_status"] == "approval_required"


def test_all_consented_pack_is_public_with_consent_and_approval_required() -> None:
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_PUBLIC, _GOOD_EVENT_PUBLIC],
        customer_handle="Slot-A",
    )
    assert pack["audience"] == "public_with_consent"
    assert pack["approval_status"] == "approval_required"


def test_forbidden_token_blocks_whole_pack() -> None:
    """One poisoned event pollutes the entire pack — even with other
    well-formed events alongside it."""
    poisoned = dict(_GOOD_EVENT_INTERNAL)
    poisoned["outcome_metric"] = "guaranteed sales"
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_PUBLIC, poisoned, _GOOD_EVENT_PUBLIC],
        customer_handle="Slot-A",
    )
    assert pack["decision"] == "blocked"
    assert pack["audience"] == "invalid"
    assert "guaranteed" in pack.get("forbidden_tokens_found", [])


# ─── hmac_signing contract ──────────────────────────────────────────


def test_hmac_returns_unsigned_when_secret_is_none() -> None:
    sig = hmac_signing.sign_pack_metadata(
        {"customer_handle": "Slot-A", "events_count": 3},
        secret=None,
    )
    assert sig == "UNSIGNED"

    # Empty string is treated as "no secret" too — never digest the empty key.
    sig_empty = hmac_signing.sign_pack_metadata(
        {"customer_handle": "Slot-A"},
        secret="",
    )
    assert sig_empty == "UNSIGNED"


def test_hmac_returns_64_char_hex_when_secret_given() -> None:
    sig = hmac_signing.sign_pack_metadata(
        {"customer_handle": "Slot-A", "events_count": 3},
        secret="rotate-me",
    )
    assert isinstance(sig, str)
    assert len(sig) == 64
    # Lowercase hex digits only.
    assert all(c in "0123456789abcdef" for c in sig)


def test_hmac_is_stable_for_same_payload_and_secret() -> None:
    payload = {
        "customer_handle": "Slot-A",
        "events_count": 3,
        "audience": "internal_only",
        "arabic": "حزمة الأدلة",
    }
    secret = "rotate-me"
    a = hmac_signing.sign_pack_metadata(payload, secret=secret)
    b = hmac_signing.sign_pack_metadata(payload, secret=secret)
    assert a == b

    # Key reordering must not change the digest (canonical sort_keys).
    payload_reordered = {
        "arabic": "حزمة الأدلة",
        "audience": "internal_only",
        "events_count": 3,
        "customer_handle": "Slot-A",
    }
    c = hmac_signing.sign_pack_metadata(payload_reordered, secret=secret)
    assert a == c

    # A different secret yields a different digest.
    d = hmac_signing.sign_pack_metadata(payload, secret="different")
    assert a != d
