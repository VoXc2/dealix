"""Governed Revenue Ops Diagnostic — create + register the entry engagement.

Creating a diagnostic records `commercial.prepared` (CEL2) via the
`CommercialEngine`: the diagnostic is staged work, not a send. Nothing leaves
the building without a later founder-confirmed `commercial.sent`.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from auto_client_acquisition.commercial_os.engine import CommercialEngine

# The diagnostic's commercial subject lives on the account timeline.
_SUBJECT_TYPE = "account"


@dataclass(frozen=True)
class Diagnostic:
    """A created Governed Revenue Ops Diagnostic engagement."""

    diagnostic_id: str
    customer_id: str
    account_id: str
    service_id: str
    cel: str
    commercial_state: str
    notes: str = ""
    inputs: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "diagnostic_id": self.diagnostic_id,
            "customer_id": self.customer_id,
            "account_id": self.account_id,
            "service_id": self.service_id,
            "cel": self.cel,
            "commercial_state": self.commercial_state,
            "notes": self.notes,
            "inputs": dict(self.inputs),
        }


def create_diagnostic(
    *,
    customer_id: str,
    account_id: str,
    engine: CommercialEngine,
    notes: str = "",
    inputs: dict[str, object] | None = None,
    actor: str = "system",
) -> Diagnostic:
    """Create a diagnostic and record `commercial.prepared` (CEL2).

    Args:
        customer_id: the Dealix customer the diagnostic belongs to.
        account_id: the account being diagnosed (the commercial subject).
        engine: the `CommercialEngine` that records the CEL transition.
        notes: optional free-text notes (no PII expected here).
        inputs: optional structured inputs captured at creation.
        actor: who created the diagnostic.

    Returns:
        A `Diagnostic` at CEL2 / `prepared_not_sent`.
    """
    diagnostic_id = f"diag_{uuid.uuid4().hex[:20]}"
    recorded = engine.record_transition(
        customer_id=customer_id,
        subject_type=_SUBJECT_TYPE,
        subject_id=account_id,
        next_state="prepared_not_sent",
        actor=actor,
        payload={
            "diagnostic_id": diagnostic_id,
            "service_id": "governed_revenue_ops_diagnostic",
        },
    )
    return Diagnostic(
        diagnostic_id=diagnostic_id,
        customer_id=customer_id,
        account_id=account_id,
        service_id="governed_revenue_ops_diagnostic",
        cel=recorded.cel,
        commercial_state=recorded.state,
        notes=notes,
        inputs=dict(inputs or {}),
    )
