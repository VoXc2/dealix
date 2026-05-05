"""PDPL — default-deny on unknown handles.

Wraps the existing consent + contactability surfaces:
  - auto_client_acquisition.compliance_os.contactability.check_contactability
  - auto_client_acquisition.compliance_os.consent_ledger.{record_consent, record_opt_out}
  - auto_client_acquisition.v3.compliance_os.assess_contactability

Hard rule asserted: an unknown handle (no consent record) MUST NOT be
contactable. Inbound consent or explicit grant is the only way to flip
to safe. This test never weakens existing assertions in
tests/unit/test_compliance_os.py.
"""

from __future__ import annotations

from auto_client_acquisition.compliance_os.consent_ledger import (
    LawfulBasis,
    record_consent,
    record_opt_out,
)
from auto_client_acquisition.compliance_os.contactability import check_contactability
from auto_client_acquisition.v3.compliance_os import (
    ContactPolicyInput,
    assess_contactability,
)


def test_unknown_handle_is_not_contactable() -> None:
    """No consent record on file → can_contact is False, reason is no_consent."""
    status = check_contactability(contact_id="unknown-handle-x", consent_records=[])
    assert status.can_contact is False
    assert status.reason_code == "no_consent"


def test_explicit_grant_flips_to_safe() -> None:
    """Recording an explicit consent for the same handle flips to safe."""
    rec = record_consent(
        customer_id="c",
        contact_id="handle-x",
        lawful_basis=LawfulBasis.CONSENT,
        purpose="b2b_outreach",
    )
    status = check_contactability(contact_id="handle-x", consent_records=[rec])
    assert status.can_contact is True
    assert status.reason_code == "safe"


def test_opt_out_after_consent_blocks() -> None:
    """Opt-out is permanent and overrides earlier consent."""
    grant = record_consent(
        customer_id="c",
        contact_id="handle-y",
        lawful_basis=LawfulBasis.CONSENT,
        purpose="b2b_outreach",
    )
    out = record_opt_out(customer_id="c", contact_id="handle-y")
    status = check_contactability(contact_id="handle-y", consent_records=[grant, out])
    assert status.can_contact is False
    assert status.reason_code == "opted_out"


def test_v3_cold_whatsapp_without_opt_in_is_blocked() -> None:
    """v3 assess_contactability blocks cold WhatsApp by policy.

    Documents that a cold channel without prior relationship returns BLOCKED;
    this is the hard rule mirrored in tests/unit/test_compliance_os.py.
    """
    out = assess_contactability(
        ContactPolicyInput(
            channel="whatsapp",
            has_opt_in=False,
            has_prior_relationship=False,
        )
    )
    assert out["status"] == "blocked"
    assert any("WhatsApp" in r or "whatsapp" in r.lower() for r in out["reasons"])
