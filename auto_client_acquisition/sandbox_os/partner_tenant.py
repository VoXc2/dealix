"""Partner sandbox tenant provisioning (initiative 161)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class PartnerSandbox:
    tenant_id: str
    partner_code: str
    isolated: bool = True


def provision_partner_sandbox(partner_code: str) -> PartnerSandbox:
    code = partner_code.strip().upper() or "PARTNER"
    return PartnerSandbox(tenant_id=f"sbx_{code}_{uuid4().hex[:8]}", partner_code=code)
