"""Payment Ops orchestrator — wires existing revops modules into a
single state-machine flow:

  invoice_intent → manual_evidence → payment_confirmed → delivery_kickoff

Hard rules (Article 8 / NO_FAKE_REVENUE):
  invoice_intent          ≠ revenue
  payment_evidence_uploaded → possible revenue
  payment_confirmed       = revenue
"""
from auto_client_acquisition.payment_ops.orchestrator import (
    confirm_payment,
    create_invoice_intent,
    get_payment_state,
    kickoff_delivery,
    upload_manual_evidence,
)

__all__ = [
    "confirm_payment",
    "create_invoice_intent",
    "get_payment_state",
    "kickoff_delivery",
    "upload_manual_evidence",
]
