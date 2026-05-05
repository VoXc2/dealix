"""Build a ProofPlan anchored to the existing ProofEventType enum.

The plan lists which proof events the founder should expect to record
as the pilot progresses. It is NOT a ledger write — it's a planning
artifact that the founder reviews before activation.
"""
from __future__ import annotations

from auto_client_acquisition.diagnostic_workflow.schemas import (
    IntakeRecord,
    ProofPlan,
)
from auto_client_acquisition.proof_ledger import ProofEventType


# Anchored to ProofEventType so a typo here breaks the test, not prod.
_DEFAULT_EXPECTED_EVENTS: tuple[ProofEventType, ...] = (
    ProofEventType.LEAD_INTAKE,
    ProofEventType.DIAGNOSTIC_DELIVERED,
    ProofEventType.PILOT_OFFERED,
    ProofEventType.INVOICE_PREPARED,
    ProofEventType.DELIVERY_STARTED,
    ProofEventType.DELIVERY_TASK_COMPLETED,
    ProofEventType.PROOF_PACK_ASSEMBLED,
)


def build_proof_plan(record: IntakeRecord, recommended_bundle_id: str) -> ProofPlan:
    """Compose the proof plan for the pilot of ``recommended_bundle_id``."""
    expected = [evt.value for evt in _DEFAULT_EXPECTED_EVENTS]
    summary_ar = (
        f"خطّة الأدلّة لباقة {recommended_bundle_id}: نسجّل {len(expected)} حدث "
        "إثبات على طول الـ Pilot. لا يُنشَر أيّ شيء بدون موافقة العميل."
    )
    summary_en = (
        f"Proof plan for bundle {recommended_bundle_id}: {len(expected)} "
        "proof events recorded across the pilot. Nothing is published "
        "without explicit customer consent."
    )
    return ProofPlan(
        company=record.company,
        expected_proof_events=expected,
        publishable_with_consent=False,
        summary_ar=summary_ar,
        summary_en=summary_en,
    )
