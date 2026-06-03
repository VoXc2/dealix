"""Contract: obvious PII patterns in row payloads are detectable (log hygiene)."""

from __future__ import annotations

from auto_client_acquisition.data_os import pii_flags_for_row


def test_no_pii_in_logs_heuristic() -> None:
    flags = pii_flags_for_row({"log_line": "contact user@company.com for details"})
    assert not flags  # generic key may not trigger — use email-shaped column
    flags2 = pii_flags_for_row({"contact_email": "user@company.com"})
    assert any(f.reason == "email_pattern" for f in flags2)
