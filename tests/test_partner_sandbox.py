"""Partner sandbox."""

from __future__ import annotations

from auto_client_acquisition.sandbox_os.partner_tenant import provision_partner_sandbox


def test_provision() -> None:
    sb = provision_partner_sandbox("acme")
    assert sb.isolated is True
    assert sb.tenant_id.startswith("sbx_")
