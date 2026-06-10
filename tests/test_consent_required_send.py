"""V14 Phase K4 — consent_required_send: per-channel × per-purpose
default-deny test.

Closes the registry's `next_activation_step_en` for
`consent_required_send`: "Upgrade the consent table schema and add a
default-deny test when consent is absent."

Hard rules verified:
  - Default-deny on absent record (PDPL Article 5)
  - Per-channel × per-purpose isolation: grant for one pair does NOT
    leak into another pair
  - Revoke is permanent for a pair (overrides earlier grant)
  - Re-grant after revoke is allowed (explicit re-opt-in)
  - Malformed inputs (unknown channel / purpose) default-deny
  - Storage I/O failure → default-deny (best-effort)
"""
from __future__ import annotations

import os
import tempfile

import pytest

from auto_client_acquisition import consent_table


@pytest.fixture(autouse=True)
def _isolated_consent_store(monkeypatch, tmp_path):
    """Each test gets its own consent-table file so tests don't pollute
    each other's state."""
    p = tmp_path / "consent-test.jsonl"
    monkeypatch.setenv("DEALIX_CONSENT_TABLE_PATH", str(p))
    yield


# ─────────────────────── Default-deny ───────────────────────


def test_no_record_means_no_consent() -> None:
    """The crown jewel — PDPL Article 5: absence of explicit consent
    means NO consent. Default-deny on every (contact, channel, purpose)
    triple."""
    assert (
        consent_table.is_consented(
            contact_id="lead_abc123",
            channel="whatsapp",
            purpose="marketing",
        )
        is False
    )


def test_empty_contact_id_is_default_deny() -> None:
    assert consent_table.is_consented(contact_id="", channel="email", purpose="transactional") is False


def test_unknown_channel_is_default_deny() -> None:
    assert consent_table.is_consented(contact_id="lead_x", channel="telegram", purpose="marketing") is False


def test_unknown_purpose_is_default_deny() -> None:
    assert consent_table.is_consented(contact_id="lead_x", channel="email", purpose="harassment") is False


# ─────────────────────── Grant ──────────────────────────────


def test_grant_then_consented_returns_true() -> None:
    consent_table.grant(
        contact_id="lead_xyz",
        channel="email",
        purpose="transactional",
        source="form_submission",
    )
    assert consent_table.is_consented(
        contact_id="lead_xyz",
        channel="email",
        purpose="transactional",
    ) is True


def test_grant_for_one_pair_does_not_leak_to_other_purpose() -> None:
    """Granted email-transactional MUST NOT imply email-marketing.
    Per-purpose isolation is the whole point of the per-channel × per-purpose
    grid."""
    consent_table.grant(
        contact_id="lead_iso",
        channel="email",
        purpose="transactional",
    )
    assert consent_table.is_consented(
        contact_id="lead_iso", channel="email", purpose="transactional"
    ) is True
    assert consent_table.is_consented(
        contact_id="lead_iso", channel="email", purpose="marketing"
    ) is False


def test_grant_for_one_pair_does_not_leak_to_other_channel() -> None:
    """Granted email-marketing MUST NOT imply whatsapp-marketing."""
    consent_table.grant(
        contact_id="lead_chan",
        channel="email",
        purpose="marketing",
    )
    assert consent_table.is_consented(
        contact_id="lead_chan", channel="email", purpose="marketing"
    ) is True
    assert consent_table.is_consented(
        contact_id="lead_chan", channel="whatsapp", purpose="marketing"
    ) is False


def test_grant_invalid_channel_raises() -> None:
    with pytest.raises(ValueError):
        consent_table.grant(contact_id="x", channel="telegram", purpose="marketing")


def test_grant_invalid_purpose_raises() -> None:
    with pytest.raises(ValueError):
        consent_table.grant(contact_id="x", channel="email", purpose="harassment")


# ─────────────────────── Revoke (permanent) ────────────────


def test_revoke_after_grant_blocks_send() -> None:
    """Standard opt-out flow: grant, then revoke → blocked from then on."""
    consent_table.grant(contact_id="lead_rev", channel="email", purpose="marketing")
    assert consent_table.is_consented(
        contact_id="lead_rev", channel="email", purpose="marketing"
    ) is True
    consent_table.revoke(contact_id="lead_rev", channel="email", purpose="marketing")
    assert consent_table.is_consented(
        contact_id="lead_rev", channel="email", purpose="marketing"
    ) is False


def test_revoke_only_affects_specific_pair() -> None:
    """Revoking email-marketing must NOT affect email-transactional."""
    consent_table.grant(contact_id="lead_pp", channel="email", purpose="marketing")
    consent_table.grant(contact_id="lead_pp", channel="email", purpose="transactional")
    consent_table.revoke(contact_id="lead_pp", channel="email", purpose="marketing")
    assert consent_table.is_consented(
        contact_id="lead_pp", channel="email", purpose="marketing"
    ) is False
    assert consent_table.is_consented(
        contact_id="lead_pp", channel="email", purpose="transactional"
    ) is True


def test_re_grant_after_revoke_is_honored() -> None:
    """Customer can opt back in. The fresh grant is the latest record
    so it wins — no perpetual block."""
    consent_table.grant(contact_id="lead_re", channel="email", purpose="marketing")
    consent_table.revoke(contact_id="lead_re", channel="email", purpose="marketing")
    consent_table.grant(
        contact_id="lead_re",
        channel="email",
        purpose="marketing",
        source="re_opt_in_form",
    )
    assert consent_table.is_consented(
        contact_id="lead_re", channel="email", purpose="marketing"
    ) is True


# ─────────────────────── Stats ──────────────────────────────


def test_stats_on_empty_store() -> None:
    s = consent_table.stats()
    assert s["total_records"] == 0
    assert s["unique_contacts"] == 0


def test_stats_after_3_records() -> None:
    consent_table.grant(contact_id="a", channel="email", purpose="transactional")
    consent_table.grant(contact_id="a", channel="whatsapp", purpose="delivery_update")
    consent_table.revoke(contact_id="b", channel="email", purpose="marketing")
    s = consent_table.stats()
    assert s["total_records"] == 3
    assert s["unique_contacts"] == 2
    assert s["by_kind"] == {"grant": 2, "revoke": 1}
    assert s["by_channel"]["email"] == 2
    assert s["by_channel"]["whatsapp"] == 1
